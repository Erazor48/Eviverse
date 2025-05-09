import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';
import ModelViewer from './components/ModelViewer';
import Analysis from './components/Analysis';
import Register from './components/auth/Register';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/home" element={<Home />} />
      <Route path="/model/:id" element={<ModelViewer />} />
      <Route path="/analysis" element={<Analysis />} />
    </Routes>
  );
};

export default App; 