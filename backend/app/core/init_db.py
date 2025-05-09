from app.core.database import engine, Base

# Importer explicitement tous les modèles pour les enregistrer
from app.models.user import User
from app.models.model3d import Model3D
from app.models.analysis import ModelAnalysis
from app.models.chat import ChatSession, ChatMessage

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Création des tables de la base de données...")
    init_db()
    print("Tables créées avec succès !") 