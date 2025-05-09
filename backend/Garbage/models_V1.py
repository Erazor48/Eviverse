from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil

from app.core.database import get_db
from app.models.model3d import Model3D as Model3DDB
from app.models.user import User as UserDB
from app.models.chat import ChatSession, ChatMessage
from app.schemas.model3d import Model3D as Model3DSchema
from app.services.auth import get_current_user


router = APIRouter(
    prefix="/models",
    tags=["models"]
)

UPLOAD_3D_DIR = "uploads/models"
UPLOAD_IMG_DIR = "uploads/images"
os.makedirs(UPLOAD_3D_DIR, exist_ok=True)
os.makedirs(UPLOAD_IMG_DIR, exist_ok=True)

# Juste après les imports existants
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_3D_EXTENSIONS = {".obj", ".glb", ".fbx", ".stl"}

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions


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

    #-------------------------------#
    #           Validation          #
    #-------------------------------#

    # ✅ Validation : au moins un champ doit être présent
    if not prompt and not images and not files_3d:
        raise HTTPException(status_code=400, detail="Remplissez au moins un champ (prompt, image, fichier 3D).")
    
    for img in images or []:
        if not is_allowed_file(img.filename, ALLOWED_IMAGE_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Format image non autorisé : {img.filename}")

    for file in files_3d or []:
        if not is_allowed_file(file.filename, ALLOWED_3D_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Format 3D non autorisé : {file.filename}")

    MAX_FILE_SIZE_MB = 20

    if file.spool_max_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux")


    #-------------------------------#
    #           Traitement          #
    #-------------------------------#

    # Sauvegarde des fichiers
    saved_3d_paths, saved_img_paths = [], []
    
    # Sauvegarde des fichiers 3D
    for file in files_3d:
        path = os.path.join(UPLOAD_3D_DIR, f"{datetime.now().timestamp()}_{file.filename}")
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_3d_paths.append(path)

    # Sauvegarde des images
    for img in images:
        path = os.path.join(UPLOAD_IMG_DIR, f"{datetime.now().timestamp()}_{img.filename}")
        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        saved_img_paths.append(path)
    
    metadata = {
        "prompt": prompt,
        "images": saved_img_paths,
        "files_3d": saved_3d_paths,
        "source_type": "user_input"
    }

    model = Model3DDB(
        name=name,
        description="Créé à partir d'une soumission utilisateur.",
        is_public=is_public,
        metadata_info=str(metadata),
        file_path=saved_3d_paths[0] if saved_3d_paths else None,
        thumbnail_path=None,
        owner_id=current_user.id,
    )
    db.add(model)
    db.commit()
    db.refresh(model)

    # === 🔁 Créer ou récupérer une session de chat ===
    session = db.query(ChatSession).filter_by(
        user_id=current_user.id,
        model3d_id=model.id,
        is_active=True
    ).first()

    if not session:
        session = ChatSession(
            user_id=current_user.id,
            model3d_id=model.id,
            is_active=True
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # === 💬 Enregistrer le message utilisateur ===
    if prompt:
        user_message = ChatMessage(
            session_id=session.id,
            content=prompt,
            is_user=True
        )
        db.add(user_message)
        db.commit()

    return model

@router.get("/", response_model=List[Model3DSchema])
def read_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
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
    model = db.query(Model3DDB).filter(Model3DDB.id == model3d_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    if model.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Supprimer les fichiers
    if os.path.exists(model.file_path):
        os.remove(model.file_path)
    if model.thumbnail_path and os.path.exists(model.thumbnail_path):
        os.remove(model.thumbnail_path)
    
    db.delete(model)
    db.commit()
    return {"message": "Modèle supprimé avec succès"}
