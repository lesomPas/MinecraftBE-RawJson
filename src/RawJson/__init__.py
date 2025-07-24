from .main import process, load
from .classes import Text, Score, Selector, Translate, Rawtext

__all__ = ["process", "load", "Text", "Score", "Selector", "Translate", "Rawtext"]
__version__ = "1.0.1"
__author__ = "lesomras"

Rawtext.process = staticmethod(process)
