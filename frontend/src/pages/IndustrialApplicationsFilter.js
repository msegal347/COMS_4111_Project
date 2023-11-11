import React from 'react';

const IndustrialApplicationsFilter = ({ onFilterChange }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Industry Name"
        onChange={e => onFilterChange('industry', e.target.value)}
      />
      {/* Add more filters as needed */}
    </div>
  );
};

export default IndustrialApplicationsFilter;
