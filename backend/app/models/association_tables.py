from app.extensions import db

# Association table for Materials and EnvironmentalImpacts
HasEffectOnEnvironment = db.Table('haseffectonenvironment',
    db.Column('materialid', db.Integer, db.ForeignKey('material.materialid'), primary_key=True),
    db.Column('impactid', db.Integer, db.ForeignKey('environmentalimpact.impactid'), primary_key=True)
)
