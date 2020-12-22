#!/usr/bin/python3

"""
jupypft.

PFLOTRAN for python and notebooks and stuff
"""

__version__ = "0.1.0"
__author__ = 'Edwin Saavedra C.'
__credits__ = 'Northwestern University'

from . import model
from . import variable

import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys
import ipywidgets as wd