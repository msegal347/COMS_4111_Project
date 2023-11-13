import React from 'react';

const MaterialsTable = ({ materials }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Category ID</th>
          <th>Created At</th>
          <th>Updated At</th>
          <th>Elemental Composition</th>
          <th>Molecular Weight</th>
          <th>Tensile Strength</th>
          <th>Ductility</th>
          <th>Hardness</th>
          <th>Thermal Conductivity</th>
          <th>Heat Capacity</th>
          <th>Melting Point</th>
          <th>Refractive Index</th>
          <th>Absorbance</th>
          <th>Conductivity</th>
          <th>Resistivity</th>
        </tr>
      </thead>
      <tbody>
        {materials.map(material => (
          <tr key={material.materialid}>
            <td>{material.materialid}</td>
            <td>{material.materialname}</td>
            <td>{material.generalcategoryid}</td>
            <td>{material.createdat}</td>
            <td>{material.updatedat}</td>
            <td>{material.elementalcomposition}</td>
            <td>{material.molecularweight}</td>
            <td>{material.tensilestrength}</td>
            <td>{material.ductility}</td>
            <td>{material.hardness}</td>
            <td>{material.thermalconductivity}</td>
            <td>{material.heatcapacity}</td>
            <td>{material.meltingpoint}</td>
            <td>{material.refractiveindex}</td>
            <td>{material.absorbance}</td>
            <td>{material.conductivity}</td>
            <td>{material.resistivity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default MaterialsTable;
