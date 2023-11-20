from app.extensions import db
from sqlalchemy import CheckConstraint

class EnvironmentalImpact(db.Model):
    __tablename__ = 'environmentalimpact'

    impactid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    toxicitylevel = db.Column(db.Float, CheckConstraint('toxicitylevel >= 0 AND toxicitylevel <= 10'), nullable=False)
    recyclability = db.Column(db.Boolean, nullable=False)
    carbonfootprint = db.Column(db.Float, CheckConstraint('carbonfootprint >= 0'), nullable=False)

    materials = db.relationship('Material', secondary='haseffectonenvironment', back_populates='environmental_impacts')

    def __init__(self, toxicitylevel, recyclability, carbonfootprint):
        self.toxicitylevel = toxicitylevel
        self.recyclability = recyclability
        self.carbonfootprint = carbonfootprint

    def to_dict(self):
        return {
            'impactid': self.impactid,
            'toxicitylevel': self.toxicitylevel,
            'recyclability': self.recyclability,
            'carbonfootprint': self.carbonfootprint
        }

    def __repr__(self):
        return f'<EnvironmentalImpact {self.impactid}>'
