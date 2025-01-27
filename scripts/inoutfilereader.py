import numpy as np
from simulation import Cylinder


def loadCylinders(path):
    """
    Load cylinder data from a file and return a list of cylinder objects.
    Args:
        path (str): The file path to load the cylinder data from.
    Returns:
        list of dict: A list of dictionaries, each containing 'x', 'y', and 'cat' keys 
                      representing the cylinder's x-coordinate, y-coordinate, and category, respectively.
    Raises:
        IOError: If the file cannot be opened or read.
        ValueError: If the file content cannot be converted to a numpy array.
    """
    
    # We load file content as a numpy array
    cylinderArray = np.loadtxt(path)
    
    # We fill a list with some cylinder objects
    return [Cylinder(cylinder[0], cylinder[1], cylinder[3]) for cylinder in cylinderArray]
