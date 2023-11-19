import React from 'react';

const IndustrialApplicationsFilter = ({ onFilterChange }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Industry Name"
        onChange={e => onFilterChange('industry', e.target.value)}
      />
    </div>
  );
};

export default IndustrialApplicationsFilter;
