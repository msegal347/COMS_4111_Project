import React from 'react';

const MaterialsFilter = ({ categories, selectedCategory, onCategoryChange, onFilterSubmit }) => {
  return (
    <form onSubmit={onFilterSubmit}>
      <select value={selectedCategory} onChange={onCategoryChange}>
        <option value="">Select Category</option>
        {categories.map(category => (
          <option key={category.generalcategoryid} value={category.generalcategoryid}>
            {category.categoryname}
          </option>
        ))}
      </select>
      <button type="submit">Search</button>
    </form>
  );
};

export default MaterialsFilter;
