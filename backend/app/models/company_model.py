from app.extensions import db 

class Company(db.Model):
    __tablename__ = 'Company'

    CompanyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CompanyName = db.Column(db.String(255), nullable=False, unique=True)
    Location = db.Column(db.String(255), nullable=False)
    Subsidiary = db.Column(db.String(255))

    def __init__(self, CompanyName, Location, Subsidiary=None):
        self.CompanyName = CompanyName
        self.Location = Location
        self.Subsidiary = Subsidiary

    def __repr__(self):
        return f'<Company {self.CompanyID}: {self.CompanyName}, {self.Location}, {self.Subsidiary}>'
