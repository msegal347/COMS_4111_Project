import React from 'react';

const EnvironmentFilter = ({ onFilterChange }) => {
  return (
    <div className="environment-filter">
      <input
        type="text"
        placeholder="Filter by Material ID"
        onChange={e => onFilterChange('material_id', e.target.value)}
      />
    </div>
  );
};

export default EnvironmentFilter;
