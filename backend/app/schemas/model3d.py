from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Model3DBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    metadata_info: Optional[str] = None

class Model3DCreate(Model3DBase):
    pass

class Model3D(Model3DBase):
    id: int
    owner_id: int
    file_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
