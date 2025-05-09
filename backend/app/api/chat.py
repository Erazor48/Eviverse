from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.chat import ChatSession as ChatSessionDB, ChatMessage as ChatMessageDB
from app.models.user import User as UserDB
from app.models.model3d import Model3D as Model3DDB
from app.schemas.chat import ChatSession as ChatSessionSchema, ChatMessage as ChatMessageSchema, ChatSessionCreate, ChatMessageCreate
from app.core.database import get_db
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.post("/sessions", response_model=ChatSessionSchema)
def create_session(
    session: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Vérifier que le modèle existe et appartient à l'utilisateur
    model = db.query(Model3DDB).filter(Model3DDB.id == session.model3d_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    if model.owner_id != current_user.id and not model.is_public:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    db_session = ChatSessionDB(
        **session.dict(),
        user_id=current_user.id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageSchema)
def post_message(
    session_id: int,
    message: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Vérif session
    session = db.query(ChatSessionDB).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    # Crée et enregistre le message
    db_message = ChatMessageDB(
        session_id=session_id,
        content=message.content,
        is_user=message.is_user
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/sessions", response_model=List[ChatSessionSchema])
def read_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    sessions = db.query(ChatSessionDB).filter(
        ChatSessionDB.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return sessions

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageSchema])
def read_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    session = db.query(ChatSessionDB).filter(ChatSessionDB.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    messages = db.query(ChatMessageDB).filter(
        ChatMessageDB.session_id == session_id
    ).offset(skip).limit(limit).all()
    return messages

@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    session = db.query(ChatSessionDB).filter_by(id=session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    db.delete(session)
    db.commit()
    return

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    db: Session = Depends(get_db)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Créer le message dans la base de données
            db_message = ChatMessageDB(
                session_id=session_id,
                content=message_data["content"],
                is_user=message_data["is_user"]
            )
            db.add(db_message)
            db.commit()
            
            # Simuler une réponse de l'IA
            if message_data["is_user"]:
                ai_response = {
                    "content": "Je suis une IA et je réponds à votre message.",
                    "is_user": False
                }
                await manager.send_message(json.dumps(ai_response), websocket)
                
                # Sauvegarder la réponse de l'IA
                db_ai_message = ChatMessageDB(
                    session_id=session_id,
                    content=ai_response["content"],
                    is_user=ai_response["is_user"]
                )
                db.add(db_ai_message)
                db.commit()
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)