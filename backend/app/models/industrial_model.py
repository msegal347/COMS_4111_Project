from app.extensions import db
from sqlalchemy import CheckConstraint

class IndustrialApplication(db.Model):
    __tablename__ = 'IndustrialApplications'

    ApplicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaterialID = db.Column(db.Integer, db.ForeignKey('Material.MaterialID'), nullable=True)
    ApplicationName = db.Column(db.String(255), nullable=False)
    Industry = db.Column(db.String(255), nullable=False)

    __table_args__ = (CheckConstraint("ApplicationName != ''", name='check_application_name_nonempty'),)

    def __init__(self, MaterialID, ApplicationName, Industry):
        self.MaterialID = MaterialID
        self.ApplicationName = ApplicationName
        self.Industry = Industry

    def to_dict(self):
        return {
            'application_id': self.ApplicationID,
            'material_id': self.MaterialID,
            'application_name': self.ApplicationName,
            'industry': self.Industry
        }

    def __repr__(self):
        return f"<IndustrialApplication {self.ApplicationID}: {self.ApplicationName} in {self.Industry}>"
