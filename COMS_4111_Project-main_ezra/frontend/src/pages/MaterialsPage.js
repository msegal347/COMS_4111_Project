import React, { useState, useEffect } from 'react';
import axios from 'axios';
import useMaterials from '../hooks/useMaterials';
import MaterialsFilter from './MaterialsFilter';
import MaterialsTable from './MaterialsTable';

const MaterialsPage = () => {
  const { materials, fetchMaterials, fetchAllMaterials, loading, error } = useMaterials();
  const [generalCategories, setGeneralCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const generalResponse = await axios.get('http://localhost:5000/api/general_categories');
        setGeneralCategories(generalResponse.data);
        fetchAllMaterials();
      } catch (err) {
        console.error('Failed to fetch data:', err);
      }
    };

    fetchData();
  }, [fetchAllMaterials]);

  const handleCategoryChange = event => {
    setSelectedCategory(event.target.value);
  };

  const handleFilterSubmit = async event => {
    event.preventDefault();
    const categoryObject = generalCategories.find(
      cat => cat.generalcategoryid.toString() === selectedCategory
    );
    const categoryName = categoryObject ? categoryObject.categoryname : ''; // Make sure this is a string
    console.log('Selected category object:', categoryObject);
    console.log('Category name:', categoryName);

    await fetchMaterials(categoryName); // Now this should pass a string, not an object
  };

  const handleShowAllMaterials = async () => {
    setSelectedCategory('');
    await fetchAllMaterials();
  };

  return (
    <div>
      <MaterialsFilter
        categories={generalCategories}
        selectedCategory={selectedCategory}
        onCategoryChange={handleCategoryChange}
        onFilterSubmit={handleFilterSubmit}
      />
      <button onClick={handleShowAllMaterials}>Show All Materials</button>
      <MaterialsTable materials={materials} />
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
    </div>
  );
};

export default MaterialsPage;
