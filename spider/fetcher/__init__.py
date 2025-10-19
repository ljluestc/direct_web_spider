# Re-export Fetcher base class from parent module
import os
import importlib.util

_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fetcher.py')
_spec = importlib.util.spec_from_file_location("_fetcher_base", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

Fetcher = _module.Fetcher

# Import and export specific fetcher implementations
from .dangdang_fetcher import DangdangFetcher
from .jingdong_fetcher import JingdongFetcher
from .tmall_fetcher import TmallFetcher
from .newegg_fetcher import NeweggFetcher
from .suning_fetcher import SuningFetcher
from .gome_fetcher import GomeFetcher

del _module_path, _spec, _module
