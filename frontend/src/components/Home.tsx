import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-indigo-600">EVIverse</h1>
              </div>
            </div>
            <div className="flex items-center">
              <Link
                to="/login"
                className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Se connecter
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <Link
              to="/model-viewer"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-50"
            >
              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                Visualisation de Modèles
              </h5>
              <p className="font-normal text-gray-700">
                Explorez et analysez vos modèles en 3D avec des outils interactifs avancés.
              </p>
            </Link>

            <Link
              to="/analysis"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-50"
            >
              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                Analyse de Données
              </h5>
              <p className="font-normal text-gray-700">
                Effectuez des analyses approfondies de vos données avec nos outils statistiques.
              </p>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home; 