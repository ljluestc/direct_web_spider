# Re-export Paginater base class from parent module
import os
import importlib.util

_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'paginater.py')
_spec = importlib.util.spec_from_file_location("_paginater_base", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

Paginater = _module.Paginater

# Import and export specific paginater implementations
from .dangdang_paginater import DangdangPaginater
from .jingdong_paginater import JingdongPaginater
from .tmall_paginater import TmallPaginater
from .newegg_paginater import NeweggPaginater
from .suning_paginater import SuningPaginater
from .gome_paginater import GomePaginater

del _module_path, _spec, _module
