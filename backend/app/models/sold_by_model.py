from app.extensions import db
from sqlalchemy import CheckConstraint

class SoldBy(db.Model):
    __tablename__ = 'soldby'

    # Column names should be in lowercase to match PostgreSQL's default behavior.
    materialid = db.Column(db.Integer, db.ForeignKey('material.materialid'), primary_key=True, nullable=False)
    companyid = db.Column(db.Integer, db.ForeignKey('company.companyid'), primary_key=True, nullable=False)
    baseprice = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        CheckConstraint(baseprice >= 0, name='ck_soldby_baseprice_positive'),
    )

    def __init__(self, materialid, companyid, baseprice, currency):
        self.materialid = materialid
        self.companyid = companyid
        self.baseprice = baseprice
        self.currency = currency

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'materialid': self.materialid,
            'companyid': self.companyid,
            'baseprice': self.baseprice,
            'currency': self.currency
        }

    def __repr__(self):
        return f"<SoldBy MaterialID={self.materialid}, CompanyID={self.companyid}>"
