from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.models.user import User as UserDB
from app.models.model3d import Model3D as Model3DDB
from app.models.analysis import ModelAnalysis as ModelAnalysisDB
from app.models.chat import ChatSession, ChatMessage
from app.schemas.user import UserCreate, User as UserSchema
from app.services.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # 1. Supprimer tous les messages liés aux sessions de l'utilisateur
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).all()
    for session in sessions:
        db.query(ChatMessage).filter(ChatMessage.session_id == session.id).delete()

    # 2. Supprimer les sessions
    db.query(ChatSession).filter(ChatSession.user_id == current_user.id).delete()

    # 3. Supprimer les analyses liées à ses modèles
    model_ids = [model.id for model in db.query(Model3DDB).filter(Model3DDB.owner_id == current_user.id).all()]
    db.query(ModelAnalysisDB).filter(ModelAnalysisDB.model3d_id.in_(model_ids)).delete()

    # 4. Supprimer les modèles 3D
    db.query(Model3DDB).filter(Model3DDB.owner_id == current_user.id).delete()

    # 5. Supprimer l'utilisateur lui-même
    db.delete(current_user)
    db.commit()

    return

"""@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Optionnel : vérifier que c’est le bon utilisateur ou un admin
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    user = db.query(UserDB).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Supprimer les analyses liées à ses modèles
    for model in user.models_3d:
        for analysis in model.analyses:
            db.delete(analysis)

    # Supprimer les modèles
    for model in user.models_3d:
        db.delete(model)

    # Supprimer les sessions et messages
    for session in user.chat_sessions:
        for message in session.messages:
            db.delete(message)
        db.delete(session)

    # Enfin, supprimer l’utilisateur
    db.delete(user)
    db.commit()
"""
