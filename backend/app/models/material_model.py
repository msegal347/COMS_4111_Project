from app.extensions import db
from sqlalchemy import ForeignKey, CheckConstraint

class Material(db.Model):
    __tablename__ = 'material' 

    materialid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materialname = db.Column(db.String(255), nullable=False, unique=True)
    generalcategoryid = db.Column(db.Integer, ForeignKey('generalcategories.generalcategoryid'))
    createdat = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updatedat = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    elementalcomposition = db.Column(db.Text)
    molecularweight = db.Column(db.Float, CheckConstraint('molecularweight > 0'))
    tensilestrength = db.Column(db.Float, CheckConstraint('tensilestrength >= 0'))
    ductility = db.Column(db.Float, CheckConstraint('ductility >= 0 AND ductility <= 100'))
    hardness = db.Column(db.Float, CheckConstraint('hardness >= 0'))
    thermalconductivity = db.Column(db.Float, CheckConstraint('thermalconductivity >= 0'))
    heatcapacity = db.Column(db.Float, CheckConstraint('heatcapacity >= 0'))
    meltingpoint = db.Column(db.Float, CheckConstraint('meltingpoint >= 0'))
    refractiveindex = db.Column(db.Float, CheckConstraint('refractiveindex > 0'))
    absorbance = db.Column(db.Float, CheckConstraint('absorbance >= 0 AND absorbance <= 1'))
    conductivity = db.Column(db.Float, CheckConstraint('conductivity >= 0'))
    resistivity = db.Column(db.Float, CheckConstraint('resistivity >= 0'))

    sold_by_relation = db.relationship('SoldBy', backref='material', lazy=True)
    environmental_impacts = db.relationship('EnvironmentalImpact', secondary='haseffectonenvironment', back_populates='materials')
    general_category = db.relationship('GeneralCategory', backref='materials')

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'materialid': self.materialid,
            'materialname': self.materialname,
            'generalcategoryid': self.generalcategoryid,
            'createdat': self.createdat.isoformat() if self.createdat else None,
            'updatedat': self.updatedat.isoformat() if self.updatedat else None,
            'elementalcomposition': self.elementalcomposition,
            'molecularweight': self.molecularweight,
            'tensilestrength': self.tensilestrength,
            'ductility': self.ductility,
            'hardness': self.hardness,
            'thermalconductivity': self.thermalconductivity,
            'heatcapacity': self.heatcapacity,
            'meltingpoint': self.meltingpoint,
            'refractiveindex': self.refractiveindex,
            'absorbance': self.absorbance,
            'conductivity': self.conductivity,
            'resistivity': self.resistivity
        }

    def __repr__(self):
        return f'<Material {self.materialid}: {self.materialname}, Category: {self.generalcategoryid}>'