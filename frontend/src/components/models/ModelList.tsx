import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Grid,
  CircularProgress,
} from '@mui/material';
import { modelService } from '../../services/models';
import { Model } from '../../services/models';

export const ModelList: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await modelService.getModels();
        setModels(data);
      } catch (err) {
        setError('Erreur lors du chargement des modèles');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Grid container spacing={3}>
      {models.map((model) => (
        <Grid item xs={12} sm={6} md={4} key={model.id}>
          <Card>
            <CardMedia
              component="img"
              height="200"
              image={model.thumbnail_path}
              alt={model.name}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                {model.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {model.description}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
                onClick={() => {
                  // TODO: Naviguer vers la page de visualisation
                }}
              >
                Voir le modèle
              </Button>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}; 