from app.extensions import db 

class Company(db.Model):
    __tablename__ = 'company'

    companyid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyname = db.Column(db.String(255), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    subsidiary = db.Column(db.String(255))

    def __init__(self, companyname, location, subsidiary=None):
        self.companyname = companyname
        self.location = location
        self.subsidiary = subsidiary

    def to_dict(self):
        """
        Serializes the object to a dictionary.
        """
        return {
            'companyid': self.companyid,
            'companyname': self.companyname,
            'location': self.location,
            'subsidiary': self.subsidiary
        }

    def __repr__(self):
        return f'<Company {self.companyid}: {self.companyname}, {self.location}, {self.subsidiary}>'
