@router.delete("/cleanup-old-models/{model_id}")
def cleanup_old_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Endpoint spécial pour supprimer un ancien modèle qui a metadata_info null.
    """
    # Récupérer le modèle
    model = db.query(Model3DDB).filter(Model3DDB.id == model_id).first()
    
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    if model.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    try:
        # Supprimer les sessions de chat et messages associés
        sessions = db.query(ChatSession).filter_by(model3d_id=model.id).all()
        for session in sessions:
            db.query(ChatMessage).filter_by(session_id=session.id).delete()
            db.delete(session)
        
        # Supprimer le fichier principal s'il existe, avec gestion des erreurs
        if model.file_path and os.path.exists(model.file_path):
            try:
                os.remove(model.file_path)
            except Exception as e:
                # Log l'erreur mais continue
                print(f"Erreur lors de la suppression du fichier {model.file_path}: {e}")
        
        # Supprimer la vignette si elle existe
        if model.thumbnail_path and os.path.exists(model.thumbnail_path):
            try:
                os.remove(model.thumbnail_path)
            except Exception as e:
                print(f"Erreur lors de la suppression de la vignette {model.thumbnail_path}: {e}")
        
        # Supprimer le modèle de la base de données
        db.delete(model)
        db.commit()
        
        return {"message": f"Modèle {model_id} supprimé avec succès"}
        
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la suppression du modèle {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression du modèle: {str(e)}")