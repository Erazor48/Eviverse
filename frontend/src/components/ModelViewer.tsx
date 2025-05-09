import React from 'react';

const ModelViewer: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Visualiseur de Modèles</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="text-gray-600">Sélectionnez un modèle à visualiser.</p>
      </div>
    </div>
  );
};

export default ModelViewer; 