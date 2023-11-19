import React from 'react';
import useSoldBy from '../hooks/useSoldBy';
import SoldByTable from './SoldByTable';

const SoldByPage = () => {
  const { soldByRelations, loading, error } = useSoldBy();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <SoldByTable soldByRelations={soldByRelations} />
    </div>
  );
};

export default SoldByPage;
