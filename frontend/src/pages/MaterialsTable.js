import React from 'react';

const MaterialsTable = ({ materials }) => {
  if (!materials.length) {
    return <div>No materials found.</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
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
        {materials.map((material, index) => (
          <tr key={material.id || index}>
            <td>{material.material_name}</td>
            <td>{material.elemental_composition}</td>
            <td>{material.molecular_weight}</td>
            <td>{material.tensile_strength}</td>
            <td>{material.ductility}</td>
            <td>{material.hardness}</td>
            <td>{material.thermal_conductivity}</td>
            <td>{material.heat_capacity}</td>
            <td>{material.melting_point}</td>
            <td>{material.refractive_index}</td>
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
