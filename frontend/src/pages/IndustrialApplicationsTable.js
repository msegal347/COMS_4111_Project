import React from 'react';

const IndustrialApplicationsTable = ({ applications }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Material Name</th>
          <th>Application Name</th>
          <th>Industry</th>
        </tr>
      </thead>
      <tbody>
        {applications.map(app => (
          <tr key={app.id}>
            <td>{app.material_name}</td>
            <td>{app.application_name}</td>
            <td>{app.industry}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default IndustrialApplicationsTable;
