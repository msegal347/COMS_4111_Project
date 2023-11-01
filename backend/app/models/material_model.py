from app.extensions import db
from sqlalchemy import ForeignKey, CheckConstraint

class Material(db.Model):
    __tablename__ = 'Material'

    MaterialID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaterialName = db.Column(db.String(255), nullable=False, unique=True)
    GeneralCategoryID = db.Column(db.Integer, ForeignKey('GeneralCategories.GeneralCategoryID'))
    CreatedAt = db.Column(db.TIMESTAMP(timezone=True), server_default='CURRENT_TIMESTAMP')
    UpdatedAt = db.Column(db.TIMESTAMP(timezone=True), server_default='CURRENT_TIMESTAMP')
    ElementalComposition = db.Column(db.Text)
    MolecularWeight = db.Column(db.Float, CheckConstraint('MolecularWeight > 0'))
    TensileStrength = db.Column(db.Float, CheckConstraint('TensileStrength >= 0'))
    Ductility = db.Column(db.Float, CheckConstraint('Ductility >= 0 AND Ductility <= 100'))
    Hardness = db.Column(db.Float, CheckConstraint('Hardness >= 0'))
    ThermalConductivity = db.Column(db.Float, CheckConstraint('ThermalConductivity >= 0'))
    HeatCapacity = db.Column(db.Float, CheckConstraint('HeatCapacity >= 0'))
    MeltingPoint = db.Column(db.Float, CheckConstraint('MeltingPoint >= 0'))
    RefractiveIndex = db.Column(db.Float, CheckConstraint('RefractiveIndex > 0'))
    Absorbance = db.Column(db.Float, CheckConstraint('Absorbance >= 0 AND Absorbance <= 1'))
    Conductivity = db.Column(db.Float, CheckConstraint('Conductivity >= 0'))
    Resistivity = db.Column(db.Float, CheckConstraint('Resistivity >= 0'))

    def __init__(self, MaterialName, GeneralCategoryID, ElementalComposition=None, 
                 MolecularWeight=None, TensileStrength=None, Ductility=None, Hardness=None,
                 ThermalConductivity=None, HeatCapacity=None, MeltingPoint=None, RefractiveIndex=None,
                 Absorbance=None, Conductivity=None, Resistivity=None):
        self.MaterialName = MaterialName
        self.GeneralCategoryID = GeneralCategoryID
        self.ElementalComposition = ElementalComposition
        self.MolecularWeight = MolecularWeight
        self.TensileStrength = TensileStrength
        self.Ductility = Ductility
        self.Hardness = Hardness
        self.ThermalConductivity = ThermalConductivity
        self.HeatCapacity = HeatCapacity
        self.MeltingPoint = MeltingPoint
        self.RefractiveIndex = RefractiveIndex
        self.Absorbance = Absorbance
        self.Conductivity = Conductivity
        self.Resistivity = Resistivity

    def __repr__(self):
        return f'<Material {self.MaterialID}: {self.MaterialName}, Category: {self.GeneralCategoryID}>'
