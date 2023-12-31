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
import ExecuteQueryPage from './pages/ExecuteQueryPage';
import CustomQueryPage from './pages/CustomQueryPage';
import UpdateDatabasePage from './pages/UpdateDatabasePage';
import UpdateSoldByPage from './pages/UpdateSoldByPage';

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
        <Route path="/execute-query" element={<ExecuteQueryPage />} />
        <Route path="/custom-query" element={<CustomQueryPage />} />
        <Route path="/update-database" element={<UpdateDatabasePage />} />
        <Route path="/update-sold-by" element={<UpdateSoldByPage />} />
        <Route path="/" element={<ExecuteQueryPage />} />
      </Routes>
    </Router>
  );
}

export default App;
