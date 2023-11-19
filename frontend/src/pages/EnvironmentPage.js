import React from 'react';
import useEnvironmentalImpacts from '../hooks/useEnvironmentalImpacts';
import EnvironmentTable from './EnvironmentTable';

const EnvironmentPage = () => {
  const { environmentalImpacts, loading, error } = useEnvironmentalImpacts();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <EnvironmentTable environmentalImpacts={environmentalImpacts} />
    </div>
  );
};

export default EnvironmentPage;
