from lumericpy.layoutMethods import *
from lumericpy.plotting import *
from lumericpy.getModeData import *
from lumericpy.magneto_optics import *
import sys
import importlib.util


def initialize():
    """
    Initializes the LumericPy package by importing necessary modules.
    To start: run lumapi = inialize() and lumapi.MODE()
    
    :return: lumapi module
    """
    sys.path.append("C:\\Program Files\\Lumerical\\v242\\api\\python\\")
    spec_win = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v242\\api\\python\\lumapi.py')
    #Functions that perform the actual loading
    lumapi = importlib.util.module_from_spec(spec_win) #windows
    spec_win.loader.exec_module(lumapi)
    print("LumericPy initialized. Ready to use!")
    return lumapi