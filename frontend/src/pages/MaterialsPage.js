import React, { useEffect } from 'react';
import useMaterials from '../hooks/useMaterials';
import MaterialsTable from './MaterialsTable';

const MaterialsPage = () => {
  const { materials, fetchAllMaterials, loading, error } = useMaterials();

  useEffect(() => {
    fetchAllMaterials();
  }, [fetchAllMaterials]);

  return (
    <div>
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
      <MaterialsTable materials={materials} />
    </div>
  );
};

export default MaterialsPage;
