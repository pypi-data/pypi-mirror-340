"""
Conversions between various magnetic units.

There are two ways to use this program:

1) as a simple command line tool for converting units. In this
   case only single values can be converted (one at a time)

2) import this package into python and then you can pass numpy arrays
   into convert_unit(), making sure to keep the default verbose=False.
   That way many values can be converted at once. The converted
   values are returned as a numpy array for further processing.
   The recommended import is:
       "import convmag as cm"

Pure python.

Requires Python >= 3.6 because f-strings are used
"""

__version__ = "0.1.2"

from convmag.convmag_functions import (
    MU_0,
    MU_B,
    Tesla_to_muB_per_fu,
    calculate_unitcell_volume,
    convert_unit,
    convmag,
    factors,
    muB_per_fu_to_Tesla,
    units,
)

__all__ = [
    MU_0,
    MU_B,
    Tesla_to_muB_per_fu,
    calculate_unitcell_volume,
    convert_unit,
    convmag,
    factors,
    muB_per_fu_to_Tesla,
    units,
]
