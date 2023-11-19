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

        # Define the relationships
    sold_by_relation = db.relationship('SoldBy', backref='material', lazy=True)
    environmental_impact = db.relationship('EnvironmentalImpact', backref='material', uselist=False)
    general_category = db.relationship('GeneralCategory', backref='materials')

    def __init__(self, materialname, generalcategoryid, elementalcomposition=None, 
                 molecularweight=None, tensilestrength=None, ductility=None, hardness=None,
                 thermalconductivity=None, heatcapacity=None, meltingpoint=None, refractiveindex=None,
                 absorbance=None, conductivity=None, resistivity=None):
        self.materialname = materialname
        self.generalcategoryid = generalcategoryid
        self.elementalcomposition = elementalcomposition
        self.molecularweight = molecularweight
        self.tensilestrength = tensilestrength
        self.ductility = ductility
        self.hardness = hardness
        self.thermalconductivity = thermalconductivity
        self.heatcapacity = heatcapacity
        self.meltingpoint = meltingpoint
        self.refractiveindex = refractiveindex
        self.absorbance = absorbance
        self.conductivity = conductivity
        self.resistivity = resistivity

    def __repr__(self):
        return f'<Material {self.materialid}: {self.materialname}, Category: {self.generalcategoryid}>'