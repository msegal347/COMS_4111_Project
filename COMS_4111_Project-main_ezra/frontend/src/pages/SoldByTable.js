import React from 'react';

const SoldByTable = ({ soldByRelations }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Material Name</th>
          <th>Company Name</th>
          <th>Base Price</th>
          <th>Currency</th>
          {/* Add more columns as needed */}
        </tr>
      </thead>
      <tbody>
        {soldByRelations.map(relation => (
          <tr key={`${relation.materialId}-${relation.companyId}`}>
            <td>{relation.materialname}</td>
            <td>{relation.companyname}</td>
            <td>{relation.baseprice}</td>
            <td>{relation.currency}</td>
            {/* Add more cells as needed */}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SoldByTable;
