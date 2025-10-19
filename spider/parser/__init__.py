# Re-export Parser base class from parent module
import os
import importlib.util

_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'parser.py')
_spec = importlib.util.spec_from_file_location("_parser_base", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

Parser = _module.Parser

# Import and export specific parser implementations
from .dangdang_parser import DangdangParser
from .jingdong_parser import JingdongParser
from .tmall_parser import TmallParser
from .newegg_parser import NeweggParser
from .suning_parser import SuningParser
from .gome_parser import GomeParser

del _module_path, _spec, _module
