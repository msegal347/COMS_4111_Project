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
            "id": material.materialid,
            "material_name": material.materialname,
            "general_category_id": material.generalcategoryid,
            "created_at": material.createdat.isoformat() if material.createdat else None,
            "updated_at": material.updatedat.isoformat() if material.updatedat else None,
            "elemental_composition": material.elementalcomposition,
            "molecular_weight": material.molecularweight,
            "tensile_strength": material.tensilestrength,
            "ductility": material.ductility,
            "hardness": material.hardness,
            "thermal_conductivity": material.thermalconductivity,
            "heat_capacity": material.heatcapacity,
            "melting_point": material.meltingpoint,
            "refractive_index": material.refractiveindex,
            "absorbance": material.absorbance,
            "conductivity": material.conductivity,
            "resistivity": material.resistivity
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
    material_query = db.session.query(Material).filter_by(materialid=material_id).first()
    if material_query:
        return {
            "id": material_query.materialid,
            "material_name": material_query.materialname,
            "general_category_id": material_query.generalcategoryid,
            "created_at": material_query.createdat.isoformat() if material_query.createdat else None,
            "updated_at": material_query.updatedat.isoformat() if material_query.updatedat else None,
            "elemental_composition": material_query.elementalcomposition,
            "molecular_weight": material_query.molecularweight,
            "tensile_strength": material_query.tensilestrength,
            "ductility": material_query.ductility,
            "hardness": material_query.hardness,
            "thermal_conductivity": material_query.thermalconductivity,
            "heat_capacity": material_query.heatcapacity,
            "melting_point": material_query.meltingpoint,
            "refractive_index": material_query.refractiveindex,
            "absorbance": material_query.absorbance,
            "conductivity": material_query.conductivity,
            "resistivity": material_query.resistivity
        }
    return None