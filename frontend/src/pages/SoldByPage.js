import React from 'react';
import useSoldBy from '../hooks/useSoldBy';
import SoldByFilter from './SoldByFilter';
import SoldByTable from './SoldByTable';

const SoldByPage = () => {
  const { soldByRelations, loading, error } = useSoldBy();

  const handleFilterChange = (filterName, value) => {
    console.log(filterName, value);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <SoldByFilter onFilterChange={handleFilterChange} />
      <SoldByTable soldByRelations={soldByRelations} />
    </div>
  );
};

export default SoldByPage;
