from app.extensions import db
from sqlalchemy import CheckConstraint

class IndustrialApplication(db.Model):
    __tablename__ = 'industrialapplications'

    # Column names should be in lowercase to match PostgreSQL's default behavior.
    applicationid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materialid = db.Column(db.Integer, db.ForeignKey('material.materialid'), nullable=True)
    applicationname = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)

    __table_args__ = (CheckConstraint("applicationname != ''", name='check_application_name_nonempty'),)

    def __init__(self, materialid, applicationname, industry):
        self.materialid = materialid
        self.applicationname = applicationname
        self.industry = industry

    def to_dict(self):
        return {
            'applicationid': self.applicationid,
            'materialid': self.materialid,
            'applicationname': self.applicationname,
            'industry': self.industry
        }

    def __repr__(self):
        return f"<IndustrialApplication {self.applicationid}: {self.applicationname} in {self.industry}>"
