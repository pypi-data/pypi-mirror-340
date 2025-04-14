"""
:authors: zaithevalex
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2025 zaithevalex
"""

from .lib.curves import (betaTransferCurve, betaTransferCurveShifted, linearCurve, squareCurve)
from .lib.operators import (AddConst, ConvertDataSetToLinearFunction, ConvertFunctionToDataSet, L1Norm, MinimizeL1Norm, MinPlusConvolution, MinPlusDeconvolution, SubAddClosure)
from .tests.operators_test import *

__author__ = 'zaithevalex'
__version__ = '1.0.0'
__email__ = 'zaithevalex@gmail.com'