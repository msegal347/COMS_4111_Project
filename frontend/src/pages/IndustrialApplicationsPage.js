import React from 'react';
import useIndustrialApplications from '../hooks/useIndustrialApplications';
import IndustrialApplicationsTable from './IndustrialApplicationsTable';

const IndustrialApplicationsPage = () => {
  const { applications, loading, error } = useIndustrialApplications();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <IndustrialApplicationsTable applications={applications} />
    </div>
  );
};

export default IndustrialApplicationsPage;
