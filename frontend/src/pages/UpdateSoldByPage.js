import React, { useState, useEffect } from 'react';
import { getMaterials, getCompanies, addSoldBy } from '../services/api';
import '../styles/UpdateSoldByPage.css';

const UpdateSoldByPage = () => {
  const [materials, setMaterials] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedMaterial, setSelectedMaterial] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [basePrice, setBasePrice] = useState('');
  const [currency, setCurrency] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDropdownData = async () => {
      setLoading(true);
      try {
        const [materialsRes, companiesRes] = await Promise.all([getMaterials(), getCompanies()]);
        setMaterials(materialsRes.data);
        setCompanies(companiesRes.data);
      } catch (err) {
        setError('Failed to fetch data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDropdownData();
  }, []);

  const handleMaterialChange = e => {
    setSelectedMaterial(e.target.value);
  };

  const handleCompanyChange = e => {
    setSelectedCompany(e.target.value);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Log the current state before submitting
    console.log('Submitting with:', {
      selectedMaterial,
      selectedCompany,
      basePrice,
      currency,
    });

    const material = materials.find(m => m.material_name === selectedMaterial);
    const company = companies.find(c => c.name === selectedCompany);

    if (material && company) {
      try {
        const response = await addSoldBy({
          materialid: material.id,
          companyid: company.id,
          basePrice,
          currency,
        });
        console.log('Update successful:', response);
        alert('Update successful!');
      } catch (err) {
        setError('Failed to update');
        console.error('Update failed:', err);
      }
    } else {
      setError('Please select valid material and company');
    }

    setLoading(false);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="update-sold-by-page">
      <h1>Update Sold By Information</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="material">Material:</label>
        <select id="material" value={selectedMaterial} onChange={handleMaterialChange}>
          <option value="">Select a Material</option>
          {materials.map(material => (
            <option key={material.materialid} value={material.material_name}>
              {material.material_name}
            </option>
          ))}
        </select>

        <label htmlFor="company">Company:</label>
        <select id="company" value={selectedCompany} onChange={handleCompanyChange}>
          <option value="">Select a Company</option>
          {companies.map(company => (
            <option key={company.companyid} value={company.name}>
              {company.name}
            </option>
          ))}
        </select>

        <label htmlFor="basePrice">Base Price:</label>
        <input
          type="number"
          id="basePrice"
          value={basePrice}
          onChange={e => setBasePrice(e.target.value)}
          min="0"
          required
        />

        <label htmlFor="currency">Currency:</label>
        <input
          type="text"
          id="currency"
          value={currency}
          onChange={e => setCurrency(e.target.value)}
          maxLength="3"
          required
        />

        <button type="submit" disabled={loading}>
          Update Sold By
        </button>
      </form>
    </div>
  );
};

export default UpdateSoldByPage;
