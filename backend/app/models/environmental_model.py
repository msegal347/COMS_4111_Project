from app.extensions import db
from sqlalchemy import CheckConstraint

class EnvironmentalImpact(db.Model):
    __tablename__ = 'environmentalimpact'

    impactid = db.Column(db.Integer, primary_key=True)
    materialid = db.Column(db.Integer, db.ForeignKey('material.materialid'), nullable=False)
    toxicitylevel = db.Column(db.Float, nullable=False, default=0.0)
    recyclability = db.Column(db.Boolean, nullable=False)
    carbonfootprint = db.Column(db.Float, nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint('toxicitylevel >= 0 AND toxicitylevel <= 10'),
        CheckConstraint('carbonfootprint >= 0'),
    )

    def __init__(self, materialid, toxicitylevel, recyclability, carbonfootprint):
        assert 0 <= toxicitylevel <= 10, "ToxicityLevel must be between 0 and 10."
        assert carbonfootprint >= 0, "CarbonFootprint must be non-negative."
        
        self.materialid = materialid
        self.toxicitylevel = toxicitylevel
        self.recyclability = recyclability
        self.carbonfootprint = carbonfootprint

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'impactid': self.impactid,
            'materialid': self.materialid,
            'toxicitylevel': self.toxicitylevel,
            'recyclability': self.recyclability,
            'carbonfootprint': self.carbonfootprint
        }

    def __repr__(self):
        return f'<EnvironmentalImpact {self.impactid}: MaterialID {self.materialid}>'
