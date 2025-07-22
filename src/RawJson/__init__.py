from .main import process
from .classes import RawText, RawScore, RawSelector, RawTranslate, Rawtext

__all__ = ["process", "RawText", "RawScore", "RawSelector", "RawTranslate", "Rawtext"]
__version__ = "1.0.0"
__author__ = "lesomras"

Rawtext.process = staticmethod(process)