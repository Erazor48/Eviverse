from pydantic import BaseModel, Field
from datetime import datetime

class ChatSessionBase(BaseModel):
    model3d_id: int
    is_active: bool = True

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    is_user: bool

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True