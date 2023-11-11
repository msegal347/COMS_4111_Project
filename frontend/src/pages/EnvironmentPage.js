import React from 'react';
import useEnvironmentalImpacts from '../hooks/useEnvironmentalImpacts'; // You need to create this hook
import EnvironmentFilter from './EnvironmentFilter';
import EnvironmentTable from './EnvironmentTable';

const EnvironmentPage = () => {
  const { environmentalImpacts, filters, setFilters, loading, error } = useEnvironmentalImpacts(); // You need to implement this hook

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
