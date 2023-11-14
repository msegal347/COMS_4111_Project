import React from 'react';
import useEnvironmentalImpacts from '../hooks/useEnvironmentalImpacts';
import EnvironmentFilter from './EnvironmentFilter';
import EnvironmentTable from './EnvironmentTable';

const EnvironmentPage = () => {
  const { environmentalImpacts, setFilters, loading, error } = useEnvironmentalImpacts();

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
      <EnvironmentFilter onFilterChange={handleFilterChange} />
      <EnvironmentTable environmentalImpacts={environmentalImpacts} />
    </div>
  );
};

export default EnvironmentPage;
