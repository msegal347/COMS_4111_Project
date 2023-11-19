import React from 'react';

const EnvironmentTable = ({ environmentalImpacts }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Material Name</th>
          <th>Toxicity Level</th>
          <th>Recyclability</th>
          <th>Carbon Footprint</th>
        </tr>
      </thead>
      <tbody>
        {environmentalImpacts.map(impact => (
          <tr key={impact.impact_id}>
            <td>{impact.material_name}</td>
            <td>{impact.toxicity_level}</td>
            <td>{impact.recyclability ? 'Yes' : 'No'}</td>
            <td>{impact.carbon_footprint}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default EnvironmentTable;
