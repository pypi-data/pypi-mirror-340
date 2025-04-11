import numpy as np
import matplotlib.pyplot as plt
import os


def setMultiple(object, parameters, values):
    """
    setMultiple sets multiple parameters of an object to the specified values.

    :param object: Lumerical simulation object
    :param parameters: list of parameter names to set
    :param values: list of values to set for the parameters
    :return: None
    """
    for i in range(len(parameters)):
        object.set(parameters[i],values[i])

def setGeometryByCenter(object, values):
    """
    setGeometryByCenter sets the geometry of an object based on its center coordinates and spans.

    :param object: Lumerical simulation object
    :param values: list of values for the center coordinates and spans
    :return: None

    """
    params=["x","y","z","x span","y span","z span"]
    setMultiple(object,params,values)

def setGeometryByLimit(object, values):
    """
    setGeometryByLimit sets the geometry of an object based on its minimum and maximum coordinates.
    
    :param object: Lumerical simulation object
    :param values: list of values for the minimum and maximum coordinates
    :return: None
    
    """
    params=["x min","x max","y min","y max","z min","z max"]
    setMultiple(object,params,values)   


