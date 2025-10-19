# Re-export Downloader base class from parent module
import os
import importlib.util

_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloader.py')
_spec = importlib.util.spec_from_file_location("_downloader_base", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

Downloader = _module.Downloader

# Import and export specific downloader implementations
from .normal_downloader import NormalDownloader
from .em_downloader import EmDownloader
from .ty_downloader import TyDownloader

del _module_path, _spec, _module
