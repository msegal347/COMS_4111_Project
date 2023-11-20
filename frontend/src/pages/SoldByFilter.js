import React from 'react';

const SoldByFilter = ({ onFilterChange }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Filter by Material ID"
        onChange={e => onFilterChange('materialId', e.target.value)}
      />
      <input
        type="text"
        placeholder="Filter by Company ID"
        onChange={e => onFilterChange('companyId', e.target.value)}
      />
    </div>
  );
};

export default SoldByFilter;
