from app.extensions import db
from sqlalchemy import CheckConstraint

class IndustrialApplication(db.Model):
    __tablename__ = 'industrialapplications'

    applicationid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    applicationname = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)

    __table_args__ = (CheckConstraint("applicationname != ''", name='check_application_name_nonempty'),)

    def __init__(self, applicationname, industry):
        self.applicationname = applicationname
        self.industry = industry

    def to_dict(self):
        return {
            'applicationid': self.applicationid,
            'applicationname': self.applicationname,
            'industry': self.industry
        }

    def __repr__(self):
        return f"<IndustrialApplication {self.applicationid}: {self.applicationname} in {self.industry}>"
