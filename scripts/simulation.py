"""File that contains the simulation parameters and some helpful functions to calculate some states during simulation."""
import math

# Cylinder mass and values
cylinders = {
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

# Comsumption parameters
comsumptionParams = {
    'b': 1e-2, 
    'b0': 1e-2
}
initialFuelQuantity = 1e4

# Speed parameters
speedParams = {
    'alpha': 0.0698,
    'V0': 1.0 # m/s
}

# Function to get the speed of the robot for a certain mass
def speed(mass):
    return speedParams.V0 * math.exp(-speedParams.alpha * mass)

# Function to get the consumption of the robot for a certain mass
def consumption(mass):
    return comsumptionParams.b * mass + comsumptionParams.b0


# Function to get the cost in fuel of a certain distance at a certain speed
def cost(distance, mass):
    return consumption(mass) * distance


# Function to get the cost in time of a certain distance at a certain speed
def timeCost(distance, mass):
    return distance / speed(mass)