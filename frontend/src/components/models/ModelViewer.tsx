import React, { useEffect, useRef } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { Model } from '../../services/models';

interface ModelViewerProps {
  model: Model;
}

export const ModelViewer: React.FC<ModelViewerProps> = ({ model }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // TODO: Initialiser le visualiseur 3D (Three.js, etc.)
    // Pour l'instant, on affiche juste une image de la miniature
    const img = document.createElement('img');
    img.src = model.thumbnail_path;
    img.style.width = '100%';
    img.style.height = '100%';
    img.style.objectFit = 'contain';
    containerRef.current.appendChild(img);

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [model]);

  return (
    <Box sx={{ width: '100%', height: '100%', position: 'relative' }}>
      <Box
        ref={containerRef}
        sx={{
          width: '100%',
          height: '100%',
          minHeight: '400px',
          backgroundColor: 'grey.100',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress />
      </Box>
      <Box sx={{ p: 2 }}>
        <Typography variant="h5">{model.name}</Typography>
        <Typography variant="body1" color="text.secondary">
          {model.description}
        </Typography>
      </Box>
    </Box>
  );
}; 