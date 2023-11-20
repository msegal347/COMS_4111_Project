from app.extensions import db

class GeneralCategory(db.Model):
    __tablename__ = 'generalcategories'

    generalcategoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(255), nullable=False, unique=True)

    __table_args__ = (
        db.CheckConstraint('categoryname <> \'\'', name='check_category_name_not_empty'),
    )

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'generalcategoryid': self.generalcategoryid,
            'categoryname': self.categoryname,
        }

    def __repr__(self):
        return f'<GeneralCategory {self.generalcategoryid}: {self.categoryname}>'
