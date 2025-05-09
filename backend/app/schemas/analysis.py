from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ModelAnalysisBase(BaseModel):
    analysis_type: str
    parameters: str
    status: str

class ModelAnalysisCreate(ModelAnalysisBase):
    model3d_id: int

class ModelAnalysis(ModelAnalysisBase):
    id: int
    model3d_id: int
    results: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
