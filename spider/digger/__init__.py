# Re-export Digger base class from parent module
# The digger.py module gets shadowed by this package directory
# so we need to explicitly make it available

import sys
import os
import importlib.util

# Load the base digger module
_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'digger.py')
_spec = importlib.util.spec_from_file_location("_digger_base", _module_path)
_digger_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_digger_module)

# Export the Digger class
Digger = _digger_module.Digger

# Import and export specific digger implementations
from .dangdang_digger import DangdangDigger
from .jingdong_digger import JingdongDigger
from .tmall_digger import TmallDigger
from .newegg_digger import NeweggDigger
from .suning_digger import SuningDigger
from .gome_digger import GomeDigger

# Clean up temporary module reference
del _module_path, _spec, _digger_module
