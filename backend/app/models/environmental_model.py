from app.extensions import db
from sqlalchemy import CheckConstraint

class EnvironmentalImpact(db.Model):
    __tablename__ = 'Environmental_Impact'

    ImpactID = db.Column(db.Integer, primary_key=True)
    MaterialID = db.Column(db.Integer, db.ForeignKey('Material.MaterialID'), nullable=False)
    ToxicityLevel = db.Column(db.Float, nullable=False, default=0.0)
    Recyclability = db.Column(db.Boolean, nullable=False)
    CarbonFootprint = db.Column(db.Float, nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint('ToxicityLevel >= 0 AND ToxicityLevel <= 10'),
        CheckConstraint('CarbonFootprint >= 0'),
    )

    def __init__(self, MaterialID, ToxicityLevel, Recyclability, CarbonFootprint):
        assert 0 <= ToxicityLevel <= 10, "ToxicityLevel must be between 0 and 10."
        assert CarbonFootprint >= 0, "CarbonFootprint must be non-negative."
        
        self.MaterialID = MaterialID
        self.ToxicityLevel = ToxicityLevel
        self.Recyclability = Recyclability
        self.CarbonFootprint = CarbonFootprint

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'impact_id': self.ImpactID,
            'material_id': self.MaterialID,
            'toxicity_level': self.ToxicityLevel,
            'recyclability': self.Recyclability,
            'carbon_footprint': self.CarbonFootprint
        }

    def __repr__(self):
        return f'<Environmental_Impact {self.ImpactID}: MaterialID {self.MaterialID}>'
