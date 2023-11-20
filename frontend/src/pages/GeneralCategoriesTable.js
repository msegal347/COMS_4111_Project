import React from 'react';

const GeneralCategoriesTable = ({ categories }) => {
  if (!categories || categories.length === 0) {
    return <p>No categories available.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Category Name</th>
        </tr>
      </thead>
      <tbody>
        {categories.map(category => (
          <tr key={category.generalcategoryid}>
            <td>{category.generalcategoryid}</td>
            <td>{category.categoryname}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default GeneralCategoriesTable;
