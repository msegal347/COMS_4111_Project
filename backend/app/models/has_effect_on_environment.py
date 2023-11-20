from app.extensions import db
from sqlalchemy import ForeignKey, CheckConstraint

class HasEffectOnEnvironment(db.Model):
    __tablename__ = 'haseffectonenvironment'

    materialid = db.Column(db.Integer, db.ForeignKey('material.materialid'), primary_key=True)
    impactid = db.Column(db.Integer, db.ForeignKey('environmentalimpact.impactid'), primary_key=True)
