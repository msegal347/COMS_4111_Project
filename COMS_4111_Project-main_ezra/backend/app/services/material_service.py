from app.extensions import db
from app.models.material_model import Material
from app.models.general_categories_model import GeneralCategory

import logging

logger = logging.getLogger(__name__)

def get_all_materials():
    """
    Fetches all materials from the database.

    Returns:
        List[dict]: List of dictionaries, where each dictionary represents a material
    """
    
    materials_query = db.session.query(Material,GeneralCategory.categoryname).join(
        GeneralCategory,
        Material.generalcategoryid == GeneralCategory.generalcategoryid
    ).all()
    

    for material in materials_query:
        print(material.categoryname)
    return [
        {
            "id": material.Material.materialid,
            "name": material.Material.materialname,
            "general_category_name": material.categoryname,
            "created_at": material.Material.createdat.isoformat() if material.Material.createdat else None,
            "updated_at": material.Material.updatedat.isoformat() if material.Material.updatedat else None,
            "elemental_composition": material.Material.elementalcomposition,
            "molecular_weight": material.Material.molecularweight,
            "tensile_strength": material.Material.tensilestrength,
            "ductility": material.Material.ductility,
            "hardness": material.Material.hardness,
            "thermal_conductivity": material.Material.thermalconductivity,
            "heat_capacity": material.Material.heatcapacity,
            "melting_point": material.Material.meltingpoint,
            "refractive_index": material.Material.refractiveindex,
            "absorbance": material.Material.absorbance,
            "conductivity": material.Material.conductivity,
            "resistivity": material.Material.resistivity
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
            "name": material_query.materialname,
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
