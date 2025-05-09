from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List, Optional, Union, Any
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
import logging

from app.core.database import get_db
from app.models.model3d import Model3D as Model3DDB
from app.models.user import User as UserDB
from app.models.chat import ChatSession, ChatMessage
from app.schemas.model3d import Model3D as Model3DSchema
from app.services.auth import get_current_user

# Configuration du logger
logger = logging.getLogger(__name__)

# Configuration des constantes
UPLOAD_3D_DIR = "uploads/models"
UPLOAD_IMG_DIR = "uploads/images"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_3D_EXTENSIONS = {".obj", ".glb", ".fbx", ".stl"}
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Création des répertoires de stockage
os.makedirs(UPLOAD_3D_DIR, exist_ok=True)
os.makedirs(UPLOAD_IMG_DIR, exist_ok=True)

router = APIRouter(
    prefix="/models",
    tags=["models"]
)

# Fonctions utilitaires
def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Vérifie si l'extension du fichier est autorisée."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

def validate_file_size(file: UploadFile, max_size: int) -> bool:
    """Vérifie si la taille du fichier est dans la limite autorisée."""
    # Note: Cette fonction nécessite que FastAPI mette le fichier en mémoire
    # pour vérifier sa taille, ce qui peut être problématique pour de gros fichiers
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)  # Réinitialiser la position pour une lecture ultérieure
    return file_size <= max_size

def save_uploaded_file(file: UploadFile, directory: str) -> str:
    """Sauvegarde un fichier uploadé et retourne son chemin."""
    timestamp = datetime.now().timestamp()
    path = os.path.join(directory, f"{timestamp}_{file.filename}")
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

def create_chat_session(db: Session, user_id: int, model3d_id: int) -> ChatSession:
    """Crée ou récupère une session de chat."""
    session = db.query(ChatSession).filter_by(
        user_id=user_id,
        model3d_id=model3d_id,
        is_active=True
    ).first()

    if not session:
        session = ChatSession(
            user_id=user_id,
            model3d_id=model3d_id,
            is_active=True
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    return session

@router.post("/submit", response_model=Model3DSchema)
def submit_model(
    name: str = Form(..., description="Nom du modèle 3D"),
    prompt: Optional[str] = Form(None, description="Prompt textuel (facultatif)"),
    images: List[UploadFile] = File([], description="Fichiers image (.jpg, .jpeg, .png, .gif)"),
    files_3d: List[UploadFile] = File([], description="Fichiers 3D (.obj, .glb, .fbx, .stl)"),
    is_public: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Endpoint pour soumettre un nouveau modèle 3D avec des fichiers associés.

    ⚠️ Attention : `Swagger UI` ne gère pas correctement l'envoi multiple de fichiers (images ou objets 3D).
    Veuillez utiliser `Postman` ou un outil `curl` pour tester correctement cette route avec plusieurs fichiers.
    """
    # Validation des entrées
    if not prompt and len(images) == 0 and len(files_3d) == 0:
        raise HTTPException(
            status_code=400, 
            detail="Remplissez au moins un champ (prompt, image, fichier 3D)."
        )
    
    # Validation des images
    for img in images:
        if not is_allowed_file(img.filename, ALLOWED_IMAGE_EXTENSIONS):
            raise HTTPException(
                status_code=400, 
                detail=f"Format image non autorisé : {img.filename}"
            )
        # La vérification de taille n'est pas idéale ici car elle charge le fichier en mémoire
        # Considérez l'utilisation d'un middleware pour cela

    # Validation des fichiers 3D
    for file in files_3d:
        if not is_allowed_file(file.filename, ALLOWED_3D_EXTENSIONS):
            raise HTTPException(
                status_code=400, 
                detail=f"Format 3D non autorisé : {file.filename}"
            )
        
        # Note: Ce code peut causer des problèmes avec les gros fichiers
        # Une meilleure approche serait d'utiliser un middleware ou une librairie spécifique
        try:
            if not validate_file_size(file, MAX_FILE_SIZE_BYTES):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Fichier trop volumineux : {file.filename}, limité à {MAX_FILE_SIZE_MB}MB"
                )
        except Exception as e:
            logger.error(f"Erreur lors de la validation de la taille: {e}")
            # Continuez sans vérification de taille si cela échoue
    
    try:
        # Sauvegarde des fichiers
        saved_img_paths = [save_uploaded_file(img, UPLOAD_IMG_DIR) for img in images]
        saved_3d_paths = [save_uploaded_file(file, UPLOAD_3D_DIR) for file in files_3d]
        
        # Création des métadonnées
        metadata = {
            "prompt": prompt,
            "images": saved_img_paths,
            "files_3d": saved_3d_paths,
            "source_type": "user_input"
        }

        # Création du modèle en base de données
        model = Model3DDB(
            name=name,
            description="Créé à partir d'une soumission utilisateur.",
            is_public=is_public,
            metadata_info=str(metadata),
            file_path=saved_3d_paths[0] if saved_3d_paths else None,
            thumbnail_path=saved_img_paths[0] if saved_img_paths else None,  # Utiliser la première image comme thumbnail
            owner_id=current_user.id,
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        
        # Gestion du chat associé
        session = create_chat_session(db, current_user.id, model.id)
        
        # Enregistrement du message utilisateur si un prompt est fourni
        if prompt:
            user_message = ChatMessage(
                session_id=session.id,
                content=prompt,
                is_user=True
            )
            db.add(user_message)
            db.commit()
        print(model)
        return model
        
    except Exception as e:
        # En cas d'erreur, nettoyer les fichiers potentiellement créés
        for path in saved_img_paths + saved_3d_paths:
            if os.path.exists(path):
                os.remove(path)
        logger.error(f"Erreur lors de la soumission du modèle: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création du modèle")

@router.get("/", response_model=List[Model3DSchema])
def read_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Récupère tous les modèles accessibles par l'utilisateur."""
    models = db.query(Model3DDB).filter(
        (Model3DDB.owner_id == current_user.id) | 
        (Model3DDB.is_public == True)
    ).offset(skip).limit(limit).all()
    
    return models

@router.get("/{model3d_id}", response_model=Model3DSchema)
def read_model(
    model3d_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Récupère un modèle spécifique par son ID."""
    model = db.query(Model3DDB).filter(Model3DDB.id == model3d_id).first()
    
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    if model.owner_id != current_user.id and not model.is_public:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    return model

@router.delete("/{model3d_id}")
def delete_model(
    model3d_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Supprime un modèle et ses fichiers associés."""
    model = db.query(Model3DDB).filter(Model3DDB.id == model3d_id).first()
    
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    if model.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    try:
        # Extraction des chemins de fichiers à partir des métadonnées
        metadata = eval(model.metadata_info)
        files_to_delete = []
        
        # Ajout du fichier principal et de la vignette
        if model.file_path and os.path.exists(model.file_path):
            files_to_delete.append(model.file_path)
        
        if model.thumbnail_path and os.path.exists(model.thumbnail_path):
            files_to_delete.append(model.thumbnail_path)
        
        # Ajout des fichiers des métadonnées
        if isinstance(metadata, dict):
            if "images" in metadata and isinstance(metadata["images"], list):
                files_to_delete.extend(metadata["images"])
            
            if "files_3d" in metadata and isinstance(metadata["files_3d"], list):
                files_to_delete.extend(metadata["files_3d"])
        
        # Suppression des fichiers
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Fichier supprimé: {file_path}")
        
        # Suppression des enregistrements associés (messages, sessions)
        sessions = db.query(ChatSession).filter_by(model3d_id=model.id).all()
        for session in sessions:
            db.query(ChatMessage).filter_by(session_id=session.id).delete()
            db.delete(session)
        
        # Suppression du modèle
        db.delete(model)
        db.commit()
        
        return {"message": "Modèle supprimé avec succès"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du modèle: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du modèle")