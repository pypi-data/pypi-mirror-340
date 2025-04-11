'''
This is a moudle for python unit calculation
Use this moudle,plese write: 
`Unit()` or other class in this moudle.
If you want to create new unit class,please use: 
```
class A(ABCUnit)
```
'''

from . import units
from advancedlib.math import *

__all__ = [
    "shapes", "fraction", "long", "dint", "SimpleType", "numpy", "matplotlib", 
    "Unit", "Line", "Area", "Volume", "Capacity", "Duration", "Version", "datetime", "operators"
]
