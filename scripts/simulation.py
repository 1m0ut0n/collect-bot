"""File that contains the simulation parameters and some helpful functions to calculate some states during simulation."""
import math


class Robot:
    
    # Comsumption parameters (to calculate the fuel consumption)
    comsumptionParams = {
        'b': 3,# l/m 
        'b0': 100# l/m.kg
    }
    initialFuelQuantity = 10000# l

    # Speed parameters (to calculate the speed of the robot)
    speedParams = {
        'alpha': 0.0698,
        'V0': 1.0# m/s
    }


    def speed(mass):
        """
        Calculate the speed of the robot based on its mass.

        This function uses an exponential decay formula to determine the speed of the robot
        given its mass. The speed is calculated using the initial speed (V0) and a decay 
        constant (alpha) from the Robot's speed parameters.

        Args:
            mass (float): The mass of the robot.

        Returns:
            float: The calculated speed of the robot.
        """
        return Robot.speedParams['V0'] * math.exp(-Robot.speedParams['alpha'] * mass)

    def consumption(mass):
        """
        Calculate the consumption based on the given mass.
        
        This function calculates the consumption based on the mass of the robot using a linear formula.

        Args:
            mass (float): The mass for which to calculate the consumption.

        Returns:
            float: The calculated consumption based on the mass.
        """
        return Robot.comsumptionParams['b'] * mass + Robot.comsumptionParams['b0']


    def fuelCost(distance, mass):
        """
        Calculate the fuel cost for a robot to travel a given distance with a specified mass.

        Args:
            distance (float): The distance the robot needs to travel.
            mass (float): The mass of the object being transported.

        Returns:
            float: The fuel required for the robot to travel the given distance.
        """
        return Robot.consumption(mass) * distance

    def timeCost(distance, mass):
        """
        Calculate the time cost for a robot to travel a given distance with a specified mass.

        Args:
            distance (float): The distance the robot needs to travel.
            mass (float): The mass of the object being transported.

        Returns:
            float: The time required for the robot to travel the given distance.
        """
        return distance / Robot.speed(mass)



class Cylinder:
    """
    A class used to represent a Cylinder.
    Attributes:
        categories (dict): A dictionary containing mass and value for each category.
    Methods:
        __init__(x, y, cat):
            Initializes a new instance of the Cylinder class.
        getPosition():
            Returns the current position of the cylinder as a tuple.
        getMass():
            Returns the mass of the cylinder based on its category.
        getValue():
            Returns the value of the cylinder based on its category.
    """
    
    # Cylinder mass and values for each category
    categories = {
        1: {
            'mass': 1.0,
            'value': 1.0,
        },
        2: {
            'mass': 2.0,
            'value': 2.0,
        },
        3: {
            'mass': 2.0,
            'value': 3.0,
        },
    }
    
    # Cylinder radius
    radius = 0.5# m
    touchingRadius = 1.6# m
    
    def __init__(self, x, y, cat):
        """
        Initializes a new instance of the class.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            cat (int): The category.
        """
        self.x = x
        self.y = y
        self.cat = int(cat)
    
    def getPosition(self):     
        """
        Get the current position of the object.

        Returns:
            tuple: A tuple containing the x and y coordinates of the object's position.
        """
        return (self.x, self.y)
    
    def getMass(self):
        """
        Retrieve the mass of the cylinder based on its category.

        Returns:
            float: The mass of the cylinder.
        """
        return Cylinder.categories[self.cat]['mass']
    
    def getValue(self):
        """
        Retrieves the value of the cylinder.

        Returns:
            float: The value of the cylinder.
        """
        return Cylinder.categories[self.cat]['value']
