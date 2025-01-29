"""Script that handle the all the logic for pathsearching."""
from simulation import Robot, Cylinder
import math
#import matplotlib.pyplot as plt

# Ponderation of the fuel cost and the time cost
FUEL_IMPORTANCE = 0.5
TIME_IMPORTANCE = 0.5


# Distance at wich the robot is too close to a cylinder
TOO_CLOSE_CYLINDER = Cylinder.touchingRadius + 0.05
AVOID_DISTANCE = Cylinder.touchingRadius + 0.15


def costOfTravel(distance, mass):
    """
    Returns the cost of traveling a certain distance with a given mass.
    This use a linear combination of fuel cost and time cost, with the specified weights.

    Parameters:
    distance (float): The distance to travel.
    mass (float): The mass of the object traveling the distance.

    Returns:
    float: The cost of traveling the distance with the given mass.
    """
    return FUEL_IMPORTANCE * Robot.fuelCost(distance, mass) + TIME_IMPORTANCE * Robot.timeCost(distance, mass)


def bestOrderOfCylinders(cylinders, initialPosition):
    """
    Returns the best order of cylinders to pick up based on the cost of traveling between them.
    This function uses a brute-force approach to calculate the best order of cylinders to pick up based on the cost of traveling between them. The function calculates the cost of traveling between all possible combinations of cylinders and returns the order that minimizes the total cost.

    Parameters:
    cylinders (list): A list of cylinder objects.
    initialPosition (float): The initial position of the robot.

    Returns:
    list: A list of cylinder objects representing the best order to pick up the cylinders.
    """
    
    # We save the position and the not explored cylinders
    remainingCylindersId = [i for i in range(len(cylinders))]
    currentPosition = initialPosition
    currentMass = 0
    order = []
    
    # Get best order
    for _ in range(len(cylinders)):
        leastCost, leastCostCylinderId = None, None
        for cylinderId in remainingCylindersId:
            # We calculate the cost of traveling between the current position and the cylinder
            cost = costOfTravel(distance(currentPosition, cylinders[cylinderId].getPosition()), currentMass)
            leastCostCylinderId, leastCost = (cylinderId, cost) if leastCost is None or cost < leastCost else (leastCostCylinderId, leastCost)
        remainingCylindersId.remove(leastCostCylinderId)
        order.append(leastCostCylinderId)
        currentMass += cylinders[leastCostCylinderId].getMass()
        currentPosition = cylinders[leastCostCylinderId].getPosition()
        
    return order
            
            
def pathFromCylindersOrder(cylinders, order, initialPosition):
    """
    Generates a path based on the given order of cylinders and an initial position.

    Args:
        cylinders (list): A list of cylinder objects, each having a getPosition() method.
        order (list): A list of indices representing the order in which to visit the cylinders.
        initialPosition (tuple): The starting position as a tuple (x, y).

    Returns:
        list: A list of positions (tuples) representing the path from the initial position through the ordered cylinders.
    """
    # Deciding the first path and keep track of the visited cylinders
    visitedCylinders = [0]
    path = avoidCylinder(cylinders, initialPosition, cylinders[0].getPosition(), visitedCylinders)
    # Adding the other paths
    for i in range(1, len(order)):
        visitedCylinders.append(order[i])
        path += avoidCylinder(cylinders, cylinders[order[i-1]].getPosition(), cylinders[order[i]].getPosition(), visitedCylinders)[1:]
    # Return the decided path
    return path


def distanceBetweenCylindersWithAvoidance(cylinders, idCylinder1, idCylinder2):
    """
    Returns the distance between two cylinders.
    If there is an obstacle between the two cylinders, an avoidance path is calculated and this distance is being calculated.

    Parameters:
    cylinder1 (tuple): The first cylinder.
    cylinder2 (tuple): The second cylinder.

    Returns:
    float: The distance between the two cylinders.
    """
    return distanceOfPath(avoidCylinder(cylinders, cylinders[idCylinder1].getPosition(), cylinders[idCylinder2].getPosition(), [idCylinder1, idCylinder2]))


def avoidCylinder(cylinders, beginPosition, endPosition, exludesCylindersId=[]):
    """
    Calculate a path that avoids cylinders between two points.
    This function takes a list of cylinders and two points (beginPosition and endPosition) and calculates a path that avoids any cylinders that may be in the way. If no cylinders are in the way, it returns a straight line between the two points. If a cylinder is in the way, it calculates an avoidance path around the cylinder.
    
    Parameters:
    cylinders (list): A list of cylinder objects.
    beginPosition (tuple): A tuple (x, y) representing the starting point of the path.
    endPosition (tuple): A tuple (x, y) representing the ending point of the path.
    exludesCylindersId (list): A list of the id of the cylinders to exclude from the avoidance path.
    
    Returns:
    list: A list of tuples representing the points of the calculated path, including the start and end points.
    """
    
    # Create a list of all cylinder that could maybe be in the way
    # For that, we take the distance of the line between the two points and we check if the circle is within that distance from the end and begin point

    # We exclude cylinders that are in the exludesCylindersId list
    notExcludedCylinders = [cylinderId for cylinderId in range(len(cylinders)) if cylinderId not in exludesCylindersId]
    
    # Calculate the regular distance between the two points and initalizing the list
    birdFlightDistance = distance(beginPosition, endPosition)
    cylinderIdMaybeInTheWay = []
    
    # For each cylinder, we check if it is in the circle of the bird flight distance diameter and center the middle of the two points
    middlePoint = (
        (beginPosition[0] + endPosition[0]) / 2,
        (beginPosition[1] + endPosition[1]) / 2
    )
    for cylinderId in notExcludedCylinders:
        if distance(middlePoint, cylinders[cylinderId].getPosition()) <= birdFlightDistance/2 + TOO_CLOSE_CYLINDER:
            cylinderIdMaybeInTheWay.append(cylinderId)

    # For each cylinder in the list, we check if it is in the way by checking his distance from the line
    tooCloseCylinderId = None
    for cylinderId in cylinderIdMaybeInTheWay:
        cylinder = cylinders[cylinderId]
        # Parameter of the line between the two points
        a = endPosition[1] - beginPosition[1]
        b = beginPosition[0] - endPosition[0]
        c = endPosition[0]*beginPosition[1] - beginPosition[0]*endPosition[1]
        # The point on the line the closest to the cylinder
        x = (b*(b*cylinder.getPosition()[0] - a*cylinder.getPosition()[1]) - a*c)/(a**2 + b**2)
        y = (a*(-b*cylinder.getPosition()[0] + a*cylinder.getPosition()[1]) - b*c)/(a**2 + b**2)
        # Check if the distance between the point and the cylinder is smaller than the radius of the cylinder and the radius of the robot (to avoid collision)
        distanceWithCylinder = distance(cylinder.getPosition(), (x, y))
        # If we find one, we stop there
        if distanceWithCylinder < TOO_CLOSE_CYLINDER :
            tooCloseCylinderId = cylinderId
            break
    
    # If we didn't find any cylinder in the way, we return the classic way of going : a straight line between the two points
    if tooCloseCylinderId is None:
        return [beginPosition, endPosition]

    # If we find a cylinder in the way, we calculate the avoidance path
    # We calculate the factor at wich we need to extend the point from the line to avoid the cylinder
    factor = AVOID_DISTANCE / distanceWithCylinder
    # We calculate the new point
    avoidanceX = cylinder.getPosition()[0] + factor * (x - cylinder.getPosition()[0])
    avoidanceY = cylinder.getPosition()[1] + factor * (y - cylinder.getPosition()[1])
    #plt.plot([x, avoidanceX], [y, avoidanceY], color='pink', linewidth=2)
    
    # We recursively build the the avoidance path by calling the function on the two new segments
    firstPartOfPath = avoidCylinder(cylinders, beginPosition, (avoidanceX, avoidanceY), exludesCylindersId + [tooCloseCylinderId])
    secondPartOfPath = avoidCylinder(cylinders, (avoidanceX, avoidanceY), endPosition, exludesCylindersId + [tooCloseCylinderId])
    
    # We return the concatenation of the two paths
    return firstPartOfPath + secondPartOfPath[1:]
    

def distance(point1, point2):
    """
    Basically returns the distance between two points.

    Parameters:
    point1 (tuple): The first point.
    point2 (tuple): The second point.

    Returns:
    float: The distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def distanceOfPath(listOfPoint):
    """
    Returns the distance of a path.

    Parameters:
    listOfPoint (list): A list of points.

    Returns:
    float: The distance of the path.
    """
    distance = 0
    for i in range(1, len(listOfPoint)):
        distance += distance(listOfPoint[i - 1], listOfPoint[i])
    return distance