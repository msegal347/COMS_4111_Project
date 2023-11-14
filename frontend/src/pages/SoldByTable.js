import React from 'react';

const SoldByTable = ({ soldByRelations }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Material ID</th>
          <th>Company ID</th>
          <th>Base Price</th>
          <th>Currency</th>
          {/* Add more columns as needed */}
        </tr>
      </thead>
      <tbody>
        {soldByRelations.map(relation => (
          <tr key={`${relation.materialId}-${relation.companyId}`}>
            <td>{relation.materialid}</td>
            <td>{relation.companyid}</td>
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
