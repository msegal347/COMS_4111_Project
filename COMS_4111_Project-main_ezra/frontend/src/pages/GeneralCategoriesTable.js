import React from 'react';

const GeneralCategoriesTable = ({ categories }) => {
  // Check if categories array is available and has length before rendering the table
  if (!categories || categories.length === 0) {
    return <p>No categories available.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Category Name</th>
          {/* Add more columns as needed */}
        </tr>
      </thead>
      <tbody>
        {categories.map(category => (
          <tr key={category.generalcategoryid}>
            <td>{category.generalcategoryid}</td>
            <td>{category.categoryname}</td>
            {/* Add more cells as needed */}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default GeneralCategoriesTable;
