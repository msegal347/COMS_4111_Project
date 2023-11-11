from flask import Blueprint, jsonify, abort
from app.extensions import db  
from app.models.company_model import Company 

company_bp = Blueprint("company", __name__, url_prefix="/api/company")

@company_bp.route("/", methods=["GET"])
def get_companies():
    try:
        companies_query = db.session.query(Company).all()
        # Use lowercase attributes as defined in the model
        companies = [
            {
                "id": company.companyid, 
                "name": company.companyname, 
                "location": company.location, 
                "subsidiary": company.subsidiary
            } for company in companies_query
        ]
        return jsonify(companies), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")

@company_bp.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    try:
        company_query = db.session.query(Company).filter_by(companyid=company_id).first()
        if company_query:
            company = {
                "id": company_query.companyid, 
                "name": company_query.companyname, 
                "location": company_query.location, 
                "subsidiary": company_query.subsidiary
            }
            return jsonify(company), 200
        else:
            abort(404, description="Company Not Found")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")
