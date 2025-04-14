"""
Validatrix - A Python library for using validatrix emulation hardware
"""

__version__ = "0.1.1"

# Import modules that don't require hardware
from .utils import *

# Hardware-dependent modules are imported only when explicitly requested
# from .DAC_interface import *
# from .can_interface import *
# from .data_collection import *
# from .thermistor_emulation import *

__all__ = [
    'utils',
    'DAC_interface',
    'can_interface',
    'data_collection',
    'thermistor_emulation'
] 