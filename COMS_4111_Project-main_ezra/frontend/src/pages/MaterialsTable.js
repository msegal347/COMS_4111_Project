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
          <tr key={material.id}>
            <td>{material.id}</td>
            <td>{material.name}</td>
            <td>{material.general_category_name}</td>
            <td>{material.created_at}</td>
            <td>{material.updated_at}</td>
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
