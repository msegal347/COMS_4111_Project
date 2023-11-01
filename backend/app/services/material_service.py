from app.extensions import db
from app.models.material_model import Material
import logging

logger = logging.getLogger(__name__)

def get_all_materials():
    """
    Fetches all materials from the database.

    Returns:
        List[dict]: List of dictionaries, where each dictionary represents a material
    """
    materials_query = db.session.query(Material).all()
    return [
        {
            "id": material.MaterialID,
            "name": material.MaterialName,
            "general_category_id": material.GeneralCategoryID,
            "created_at": material.CreatedAt,
            "updated_at": material.UpdatedAt,
            "elemental_composition": material.ElementalComposition,
            "molecular_weight": material.MolecularWeight,
            "tensile_strength": material.TensileStrength,
            "ductility": material.Ductility,
            "hardness": material.Hardness,
            "thermal_conductivity": material.ThermalConductivity,
            "heat_capacity": material.HeatCapacity,
            "melting_point": material.MeltingPoint,
            "refractive_index": material.RefractiveIndex,
            "absorbance": material.Absorbance,
            "conductivity": material.Conductivity,
            "resistivity": material.Resistivity
        }
        for material in materials_query
    ]

def get_material_by_id(material_id):
    """
    Fetches a specific material by its ID from the database.

    Args:
        material_id (int): The ID of the material to fetch

    Returns:
        dict: A dictionary representing the material if found, None otherwise
    """
    material_query = db.session.query(Material).filter_by(MaterialID=material_id).first()
    if material_query:
        return {
            "id": material_query.MaterialID,
            "name": material_query.MaterialName,
            "general_category_id": material_query.GeneralCategoryID,
            "created_at": material_query.CreatedAt,
            "updated_at": material_query.UpdatedAt,
            "elemental_composition": material_query.ElementalComposition,
            "molecular_weight": material_query.MolecularWeight,
            "tensile_strength": material_query.TensileStrength,
            "ductility": material_query.Ductility,
            "hardness": material_query.Hardness,
            "thermal_conductivity": material_query.ThermalConductivity,
            "heat_capacity": material_query.HeatCapacity,
            "melting_point": material_query.MeltingPoint,
            "refractive_index": material_query.RefractiveIndex,
            "absorbance": material_query.Absorbance,
            "conductivity": material_query.Conductivity,
            "resistivity": material_query.Resistivity
        }
    return None
