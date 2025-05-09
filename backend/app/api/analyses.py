from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.analysis import ModelAnalysis as ModelAnalysisDB
from app.models.model3d import Model3D as Model3DDB
from app.models.user import User as UserDB
from app.schemas.analysis import ModelAnalysisCreate, ModelAnalysis as ModelAnalysisSchema
from app.core.database import get_db
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/analyses",
    tags=["analyses"]
)

def process_analysis(analysis_id: int, db: Session):
    # Simuler le traitement de l'analyse
    analysis = db.query(ModelAnalysisDB).filter(ModelAnalysisDB.id == analysis_id).first()
    if analysis:
        # Mettre à jour le statut
        analysis.status = "en_cours"
        db.commit()
        
        # Simuler le traitement
        import time
        time.sleep(5)
        
        # Mettre à jour les résultats
        analysis.results = json.dumps({
            "metrics": {
                "volume": 1000,
                "surface": 500,
                "complexity": "moyenne"
            }
        })
        analysis.status = "terminée"
        db.commit()

@router.post("/", response_model=ModelAnalysisSchema)
def create_analysis(
    analysis: ModelAnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Vérifier que le modèle existe et appartient à l'utilisateur
    model = db.query(Model3DDB).filter(Model3DDB.id == analysis.model3d_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    if model.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    db_analysis = ModelAnalysisDB(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Lancer le traitement en arrière-plan
    background_tasks.add_task(process_analysis, db_analysis.id, db)
    
    return db_analysis

@router.get("/", response_model=List[ModelAnalysisSchema])
def read_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    analyses = db.query(ModelAnalysisDB).join(Model3DDB).filter(
        Model3DDB.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return analyses

@router.get("/{analysis_id}", response_model=ModelAnalysisSchema)
def read_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    analysis = db.query(ModelAnalysisDB).join(Model3DDB).filter(
        ModelAnalysisDB.id == analysis_id,
        Model3DDB.owner_id == current_user.id
    ).first()
    
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    return analysis