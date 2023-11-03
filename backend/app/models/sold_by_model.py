from app.extensions import db
from sqlalchemy import CheckConstraint

class SoldBy(db.Model):
    __tablename__ = 'SoldBy'

    MaterialID = db.Column(db.Integer, db.ForeignKey('Material.MaterialID'), primary_key=True, nullable=False)
    CompanyID = db.Column(db.Integer, db.ForeignKey('Company.CompanyID'), primary_key=True, nullable=False)
    BasePrice = db.Column(db.Float, nullable=False)
    Currency = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        CheckConstraint(BasePrice >= 0, name='ck_soldby_baseprice_positive'),
    )

    def __init__(self, MaterialID, CompanyID, BasePrice, Currency):
        self.MaterialID = MaterialID
        self.CompanyID = CompanyID
        self.BasePrice = BasePrice
        self.Currency = Currency

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'material_id': self.MaterialID,
            'company_id': self.CompanyID,
            'base_price': self.BasePrice,
            'currency': self.Currency
        }
