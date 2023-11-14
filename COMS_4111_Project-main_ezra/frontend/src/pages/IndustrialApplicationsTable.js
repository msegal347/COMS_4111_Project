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
          <tr key={app.applicationid}>
            <td>{app.applicationid}</td>
            <td>{app.materialid}</td>
            <td>{app.applicationname}</td>
            <td>{app.industry}</td>
            {/* Add more cells as needed */}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default IndustrialApplicationsTable;
