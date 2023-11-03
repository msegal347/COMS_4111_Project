from app.extensions import db
from app.models.sold_by_model import SoldBy
import logging

logger = logging.getLogger('sold_by_service')

def get_all_sold_by_relations():
    try:
        return SoldBy.query.all()
    except Exception as e:
        logger.error(f"Error retrieving all sold by relations: {e}")
        raise

def get_sold_by_relation(material_id, company_id):
    try:
        return SoldBy.query.get((material_id, company_id))
    except Exception as e:
        logger.error(f"Error retrieving sold by relation: {e}")
        raise

def create_sold_by_relation(data):
    try:
        new_relation = SoldBy(**data)
        db.session.add(new_relation)
        db.session.commit()
        return new_relation
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating sold by relation: {e}")
        raise

def update_sold_by_relation(material_id, company_id, data):
    try:
        relation = SoldBy.query.get((material_id, company_id))
        if relation:
            for key, value in data.items():
                setattr(relation, key, value)
            db.session.commit()
            return relation
        else:
            return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating sold by relation: {e}")
        raise

def delete_sold_by_relation(material_id, company_id):
    try:
        relation = SoldBy.query.get((material_id, company_id))
        if relation:
            db.session.delete(relation)
            db.session.commit()
        else:
            logger.warning(f"No sold by relation found to delete.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting sold by relation: {e}")
        raise
