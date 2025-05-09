from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class ModelAnalysis(Base):
    __tablename__ = "model_analyses"

    id = Column(Integer, primary_key=True, index=True)
    model3d_id = Column(Integer, ForeignKey("models_3d.id"))
    analysis_type = Column(String)
    parameters = Column(Text)
    results = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(String)

    model = relationship("Model3D", back_populates="analyses")
