// app.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MaterialsPage from './pages/MaterialsPage';
// Other imports

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/materials" element={<MaterialsPage />} />
        <Route path="/" element={<MaterialsPage />} /> {/* Add this line */}
        {/* Other routes */}
      </Routes>
    </Router>
  );
}

export default App;
