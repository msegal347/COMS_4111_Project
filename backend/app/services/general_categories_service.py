from app.extensions import db
from app.models.general_categories_model import GeneralCategory

def get_all_general_categories():
    return GeneralCategory.query.all()

def get_general_category_by_id(category_id):
    return GeneralCategory.query.get(category_id)

def create_general_category(category_name):
    category = GeneralCategory(CategoryName=category_name)
    db.session.add(category)
    db.session.commit()
    return category

def update_general_category(category_id, category_name):
    category = GeneralCategory.query.get(category_id)
    if category:
        category.CategoryName = category_name
        db.session.commit()
        return category
    return None

def delete_general_category(category_id):
    category = GeneralCategory.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False
