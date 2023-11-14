import React from 'react';
import useIndustrialApplications from '../hooks/useIndustrialApplications';
import IndustrialApplicationsFilter from './IndustrialApplicationsFilter';
import IndustrialApplicationsTable from './IndustrialApplicationsTable';

const IndustrialApplicationsPage = () => {
  const { applications, setFilters, loading, error } = useIndustrialApplications();

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
      <IndustrialApplicationsFilter onFilterChange={handleFilterChange} />
      <IndustrialApplicationsTable applications={applications} />
    </div>
  );
};

export default IndustrialApplicationsPage;
