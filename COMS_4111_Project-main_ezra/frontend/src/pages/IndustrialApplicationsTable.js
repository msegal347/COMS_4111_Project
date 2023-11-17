import React from 'react';

const IndustrialApplicationsTable = ({ applications }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Material ID</th>
          <th>Application Name</th>
          <th>Industry</th>
          {/* Add more columns as needed */}
        </tr>
      </thead>
      <tbody>
        {applications.map(app => (
          <tr key={app.id}>
            <td>{app.id}</td>
            <td>{app.material_name}</td>
            <td>{app.application_name}</td>
            <td>{app.industry}</td>
            {/* Add more cells as needed */}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default IndustrialApplicationsTable;
