from app.extensions import db

# Association table for Materials and EnvironmentalImpacts
HasEffectOnEnvironment = db.Table('HasEffectOnEnvironment',
    db.Column('MaterialID', db.Integer, db.ForeignKey('Material.MaterialID'), primary_key=True),
    db.Column('ImpactID', db.Integer, db.ForeignKey('EnvironmentalImpact.ImpactID'), primary_key=True)
)
