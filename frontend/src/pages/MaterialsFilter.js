import React from 'react';

const MaterialFilter = ({ onFilterChange }) => {
  // Temporary hardcoded categories
  const categories = [
    { id: '1', name: 'Category 1' },
    { id: '2', name: 'Category 2' },
    { id: '3', name: 'Category 3' },
  ];

  return (
    <div>
      <input
        type="text"
        placeholder="Material Name"
        onChange={e => onFilterChange('materialname', e.target.value)}
      />
      <select onChange={e => onFilterChange('generalcategoryid', e.target.value)} defaultValue="">
        <option value="" disabled>
          Select Category
        </option>
        {categories.map(category => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
      {/* ... other input fields */}
    </div>
  );
};

export default MaterialFilter;
