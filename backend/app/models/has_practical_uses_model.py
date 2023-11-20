from app.extensions import db
from sqlalchemy import ForeignKey, CheckConstraint

class HasPracticalUses(db.Model):
    __tablename__ = 'haspracticaluses'

    materialid = db.Column(db.Integer, db.ForeignKey('material.materialid'), primary_key=True)
    applicationid = db.Column(db.Integer, db.ForeignKey('industrialapplications.applicationid'), primary_key=True)

    material = db.relationship('Material', backref=db.backref('practical_uses', cascade='all, delete-orphan'))
    application = db.relationship('IndustrialApplication', backref=db.backref('used_for', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'materialid': self.materialid,
            'applicationid': self.applicationid
        }

    def __repr__(self):
        return f"<HasPracticalUses material_id={self.materialid}, application_id={self.applicationid}>"
