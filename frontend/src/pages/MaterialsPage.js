import React from 'react';
import useMaterials from '../hooks/useMaterials';
import MaterialsFilter from './MaterialsFilter';
import MaterialsTable from './MaterialsTable';

const MaterialsPage = () => {
  const { materials, setFilters, loading, error } = useMaterials();

  const handleFilterChange = (filterName, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value,
    }));
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <MaterialsFilter onFilterChange={handleFilterChange} />
      <MaterialsTable materials={materials} />
    </div>
  );
};

export default MaterialsPage;
