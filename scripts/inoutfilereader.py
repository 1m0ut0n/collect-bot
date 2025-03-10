import numpy as np
from simulation import Cylinder
from os import makedirs


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
    return [Cylinder(float(cylinder[0]), float(cylinder[1]), int(cylinder[2])) for cylinder in cylinderArray]


def saveMovements(movements, filename, dirs):
    """
    Save a list of movements to a file.
    Args:
        movements (list of str): A list of movements to save.
        path (str): The file path to save the movements to.
    """
    makedirs(dirs, exist_ok=True)
    with open(dirs + '/' + filename , 'w') as f:
        for movement in movements:
            f.write(f"{movement}\n")