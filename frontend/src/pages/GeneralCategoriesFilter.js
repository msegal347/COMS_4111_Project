import React from 'react';

const GeneralCategoriesFilter = ({ onFilterChange }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Category Name"
        onChange={e => onFilterChange('categoryName', e.target.value)}
      />
      {/* Add more filters as needed */}
    </div>
  );
};

export default GeneralCategoriesFilter;