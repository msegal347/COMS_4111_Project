import React from 'react';

const CompanyTable = ({ companies }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Subsidiary</th>
        </tr>
      </thead>
      <tbody>
        {companies.map(company => (
          <tr key={company.id}>
            <td>{company.id}</td>
            <td>{company.name}</td>
            <td>{company.location}</td>
            <td>{company.subsidiary}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CompanyTable;
