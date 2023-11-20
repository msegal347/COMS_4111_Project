from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .material_model import Material 
from .company_model import Company
from .environmental_model import EnvironmentalImpact
from .sold_by_model import SoldBy
from .industrial_model import IndustrialApplication
from .general_categories_model import GeneralCategory
from .has_practical_uses_model import HasPracticalUses
from .has_effect_on_environment import HasEffectOnEnvironment
