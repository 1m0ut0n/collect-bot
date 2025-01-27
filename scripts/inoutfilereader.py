import numpy as np


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
    return [{'x': cylinder[0], 'y': cylinder[1], 'cat': cylinder[2]} for cylinder in cylinderArray]


def give_path(commands_as_array):

    np.savetxt('script', commands_as_array)
