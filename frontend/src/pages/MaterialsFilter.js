import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MaterialFilter = ({ onFilterChange }) => {
  const [categories, setCategories] = useState([]);
  const [materialName, setMaterialName] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/general_categories');
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
        // Handle errors as needed
      }
    };

    fetchCategories();
  }, []);

  const handleMaterialNameChange = event => {
    const value = event.target.value;
    setMaterialName(value);
    onFilterChange('materialname', value);
  };

  const handleCategoryChange = event => {
    const value = event.target.value;
    onFilterChange('generalcategoryid', value);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Material Name"
        value={materialName}
        onChange={handleMaterialNameChange}
      />
      <select onChange={handleCategoryChange} defaultValue="">
        <option value="" disabled>
          Select Category
        </option>
        {categories.map(category => (
          <option key={category.generalcategoryid} value={category.generalcategoryid}>
            {category.categoryname}
          </option>
        ))}
      </select>
    </div>
  );
};

export default MaterialFilter;
