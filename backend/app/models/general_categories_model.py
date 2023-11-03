from app.extensions import db

class GeneralCategory(db.Model):
    __tablename__ = 'GeneralCategories'

    GeneralCategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(255), nullable=False, unique=True)

    __table_args__ = (
        db.CheckConstraint('CategoryName <> \'\'', name='check_category_name_not_empty'),
    )

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'general_category_id': self.GeneralCategoryID,
            'category_name': self.CategoryName,
        }

    def __repr__(self):
        return f'<GeneralCategory {self.GeneralCategoryID}: {self.CategoryName}>'
