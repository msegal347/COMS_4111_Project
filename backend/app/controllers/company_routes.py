from flask import Blueprint, jsonify, abort
from app import db  # Assuming db is initialized in your app/__init__.py
from app.models.company_model import Company  # Adjust the import path according to your project structure

company_bp = Blueprint("company", __name__, url_prefix="/api/company")

@company_bp.route("/", methods=["GET"])
def get_companies():
    try:
        companies_query = db.session.query(Company).all()
        companies = [{"id": company.CompanyID, "name": company.CompanyName, "location": company.Location, "subsidiary": company.Subsidiary} for company in companies_query]
        return jsonify(companies), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")

@company_bp.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    try:
        company_query = db.session.query(Company).filter_by(CompanyID=company_id).first()
        if company_query:
            company = {"id": company_query.CompanyID, "name": company_query.CompanyName, "location": company_query.Location, "subsidiary": company_query.Subsidiary}
            return jsonify(company), 200
        else:
            abort(404, description="Company Not Found")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")
