import React, { useState, useEffect } from 'react';
import useUpdateDatabase from '../hooks/useUpdateDatabase';
import { getGeneralCategories } from '../services/api';
import '../styles/UpdateDatabasePage.css';

const UpdateDatabasePage = () => {
  const { updateDatabase, loading, error, success } = useUpdateDatabase();
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [formData, setFormData] = useState({
    materialName: '',
    elementalComposition: '',
    molecularWeight: 0,
    tensileStrength: 0,
    ductility: 0,
    hardness: 0,
    thermalConductivity: 0,
    heatCapacity: 0,
    meltingPoint: 0,
    refractiveIndex: 0,
    absorbance: 0,
    conductivity: 0,
    resistivity: 0,
  });

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await getGeneralCategories();
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  const handleChange = e => {
    const { name, value, type } = e.target;
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: type === 'number' ? parseFloat(value) : value,
    }));
  };

  const handleCategoryChange = e => {
    setSelectedCategory(e.target.value);
  };

  const handleSubmit = async event => {
    event.preventDefault();
    const category = categories.find(c => c.categoryname === selectedCategory);
    const categoryID = category ? category.generalcategoryid : null;
    if (categoryID) {
      await updateDatabase({ ...formData, generalCategoryID: categoryID });
    } else {
      console.error('Category ID not found');
    }
  };

  return (
    <div className="update-database-page">
      <h1>Update Database</h1>
      {loading && <p>Updating...</p>}
      {error && <p>Error: {error}</p>}
      {success && <p>Update successful!</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="materialName">Material Name</label>
        <input
          name="materialName"
          value={formData.materialName}
          onChange={handleChange}
          placeholder="Material Name"
          required
        />
        <label htmlFor="elementalComposition">Elemental Composition</label>
        <input
          name="elementalComposition"
          value={formData.elementalComposition}
          onChange={handleChange}
          placeholder="Elemental Composition"
          required
        />
        <label htmlFor="molecularWeight">Molecular Weight</label>
        <input
          type="number"
          name="molecularWeight"
          value={formData.molecularWeight}
          onChange={handleChange}
          placeholder="Molecular Weight"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="tensileStrength">Tensile Strength</label>
        <input
          type="number"
          name="tensileStrength"
          value={formData.tensileStrength}
          onChange={handleChange}
          placeholder="Tensile Strength"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="ductility">Ductility</label>
        <input
          type="number"
          name="ductility"
          value={formData.ductility}
          onChange={handleChange}
          placeholder="Ductility"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="hardness">Hardness</label>
        <input
          type="number"
          name="hardness"
          value={formData.hardness}
          onChange={handleChange}
          placeholder="Hardness"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="thermalConductivity">Thermal Conductivity</label>
        <input
          type="number"
          name="thermalConductivity"
          value={formData.thermalConductivity}
          onChange={handleChange}
          placeholder="Thermal Conductivity"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="heatCapacity">Heat Capacity</label>
        <input
          type="number"
          name="heatCapacity"
          value={formData.heatCapacity}
          onChange={handleChange}
          placeholder="Heat Capacity"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="meltingPoint">Melting Point</label>
        <input
          type="number"
          name="meltingPoint"
          value={formData.meltingPoint}
          onChange={handleChange}
          placeholder="Melting Point"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="refractiveIndex">Refractive Index</label>
        <input
          type="number"
          name="refractiveIndex"
          value={formData.refractiveIndex}
          onChange={handleChange}
          placeholder="Refractive Index"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="absorbance">Absorbance</label>
        <input
          type="number"
          name="absorbance"
          value={formData.absorbance}
          onChange={handleChange}
          placeholder="Absorbance"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="conductivity">Conductivity</label>
        <input
          type="number"
          name="conductivity"
          value={formData.conductivity}
          onChange={handleChange}
          placeholder="Conductivity"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="resistivity">Resistivity</label>
        <input
          type="number"
          name="resistivity"
          value={formData.resistivity}
          onChange={handleChange}
          placeholder="Resistivity"
          min="0"
          step="0.01"
          required
        />
        <label htmlFor="generalCategoryID">General Category ID</label>
        <select
          name="generalCategory"
          value={selectedCategory}
          onChange={handleCategoryChange}
          required
        >
          <option value="">Select a Category</option>
          {categories.map(category => (
            <option key={category.generalcategoryid} value={category.categoryname}>
              {category.categoryname}
            </option>
          ))}
        </select>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default UpdateDatabasePage;
