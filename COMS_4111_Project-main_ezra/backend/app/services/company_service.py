from app.extensions import db
from app.models.company_model import Company 

def get_all_companies():
    """
    Fetches all companies from the database.

    Returns:
        List[dict]: List of dictionaries, where each dictionary represents a company
    """
    companies_query = db.session.query(Company).all()
    return [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "location": company.Location,
            "subsidiary": company.Subsidiary
        } 
        for company in companies_query
    ]

def get_company_by_id(company_id):
    """
    Fetches a specific company by its ID from the database.

    Args:
        company_id (int): The ID of the company to fetch

    Returns:
        dict: A dictionary representing the company if found, None otherwise
    """
    company_query = db.session.query(Company).filter_by(CompanyID=company_id).first()
    if company_query:
        return {
            "id": company_query.CompanyID,
            "name": company_query.CompanyName,
            "location": company_query.Location,
            "subsidiary": company_query.Subsidiary
        }
    return None
