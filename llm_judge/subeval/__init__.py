import warnings
try:
    import torch
except ImportError:
    warnings.warn('torch is not installed. ')   
from .smp import *
from .chat_api import *
