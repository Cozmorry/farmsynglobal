//backend/core/models_registry.py
from backend.core.database import Base

# Import all models from every module here (only once!)
from backend.modules.agronomy.models import *
from backend.modules.aquaculture.models import *
from backend.modules.crop_management.models import *
from backend.modules.farms.models import *
from backend.modules.finance.models import *
from backend.modules.hr.models import *
from backend.modules.livestock.models import *
from backend.modules.poultry.models import *
from backend.modules.store_inventory.models import *
from backend.modules.users.models import *
from backend.modules.veterinary.models import *
from backend.modules.weather.models import *
from backend.modules.audit.models import *