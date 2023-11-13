import React from 'react';

const CompanyFilter = ({ onFilterChange }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Company Name"
        onChange={e => onFilterChange('name', e.target.value)}
      />
      {/* Add more filters as needed */}
    </div>
  );
};

export default CompanyFilter;
