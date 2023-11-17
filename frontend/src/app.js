import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MaterialsPage from './pages/MaterialsPage';
import IndustrialApplicationsPage from './pages/IndustrialApplicationsPage';
import GeneralCategoriesPage from './pages/GeneralCategoriesPage';
import CompaniesPage from './pages/CompanyPage';
import EnvironmentPage from './pages/EnvironmentPage';
import Navigation from './components/Navigation';
import SoldByPage from './pages/SoldByPage';
import QueryPage from './pages/QueryPage';
import './styles/main.css';

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/query" element={<QueryPage />} />
        <Route path="/materials" element={<MaterialsPage />} />
        <Route path="/industrial-applications" element={<IndustrialApplicationsPage />} />
        <Route path="/general-categories" element={<GeneralCategoriesPage />} />
        <Route path="/companies" element={<CompaniesPage />} />
        <Route path="/sold-by" element={<SoldByPage />} />
        <Route path="/environment" element={<EnvironmentPage />} />{' '}
        <Route path="/" element={<QueryPage />} />
      </Routes>
    </Router>
  );
}

export default App;
