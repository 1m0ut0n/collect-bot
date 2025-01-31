"""Script to handle the visualisation of the cylinder decision and dicided path with Matplotlib."""
import matplotlib.pyplot as plt
from pathsearch import distance, TOO_CLOSE_CYLINDER
import simulation as sim


def traceMap(ax, cylinders, initialPosition, visitedCylindersId = []):
    """
    Plots a scatter plot of cylinders on a map using matplotlib.
    Use the `show()` function to display the plot.

    Args:
        ax (matplotlib.axes.Axes): The axes on which to plot the cylinders.
        cylinders (list): List of cylinder objects.
        initialPosition (tuple): The initial position to be marked on the plot, given as (x, y).
        visitedCylindersId (list, optional): List of cylinder IDs that have been visited. Defaults to an empty list.
    """
    # We plot all the cylinders
    for cylinderId in range(len(cylinders)):
        cylinder = cylinders[cylinderId]
        color = 'red' if cylinder.cat == 1 else 'green' if cylinder.cat == 2 else 'blue'
        ax.add_patch(plt.Circle((cylinder.x, cylinder.y), radius=sim.Cylinder.touchingRadius, color='gray', alpha=0.05 if cylinderId in visitedCylindersId else 0.2))
        ax.add_patch(plt.Circle((cylinder.x, cylinder.y), radius=sim.Cylinder.radius, color=color, alpha=0.3 if cylinderId in visitedCylindersId else 1))
    # We plot the initial position
    plt.plot(initialPosition[0], initialPosition[1], marker='x', color='black', markersize=10)

def tracePath(path, noMoreFuelPointId = None, noMoreTimePointId = None):
    """
    Plots the given path on a graph with a black dotted line and pauses briefly to visualize the drawing process.
    Use the `show()` function to display the plot.

    Parameters:
    path (list of tuples): A list of (x, y) coordinates representing the path to be plotted.
    """
    # We set a finish point when there are no more fuel or time
    noMoreFuelPointId = noMoreFuelPointId if noMoreFuelPointId is not None else len(path)
    noMoreTimePointId = noMoreTimePointId if noMoreTimePointId is not None else len(path)
    finishPointId = min(noMoreFuelPointId, noMoreTimePointId)
    # We plot the path in dark before the finish point and in gray after
    plt.plot([p[0] for p in path[:finishPointId+1]], [p[1] for p in path[:finishPointId+1]], color='black', linestyle=':', linewidth=2)
    plt.plot([p[0] for p in path[finishPointId:]], [p[1] for p in path[finishPointId:]], color='gray', linestyle=':', linewidth=2)


def displayStats(ax, remainingTime, remainingFuel, mass, points, massWithoutLimits, pointsWithoutLimits):
    """
    Display the remaining time, fuel, mass and points on the plot.

    Args:
        ax (matplotlib.axes.Axes): The axes on which to plot the text.
        remainingTime (float): The remaining time.
        remainingFuel (float): The remaining fuel.
        mass (float): The mass of the robot.
        points (float): The points collected.
    """
    ax.text(1.02, 0.95, f"Mass: {mass:.2f} kg", transform=ax.transAxes)
    ax.text(1.02, 0.9, f"Points: {points}", transform=ax.transAxes)
    ax.text(1.02, 0.85, f"Time: {remainingTime:.2f} s", transform=ax.transAxes, color='gray' if remainingTime < 0 else 'black')
    ax.text(1.02, 0.8, f"Fuel: {remainingFuel:.2f} L", transform=ax.transAxes, color='gray' if remainingFuel < 0 else 'black')
    if remainingTime < 0 or remainingFuel < 0:
        ax.text(1.02, 0.75, f"Mass: {massWithoutLimits:.2f} kg", transform=ax.transAxes, color='gray')
        ax.text(1.02, 0.7, f"Points: {pointsWithoutLimits}", transform=ax.transAxes, color='gray')
    
    


def showSimulation(cylinders, initialPosition, chosenPath):
    """
    Visualizes the simulation by seeing the path being drawn and the cylinder get recolted.
    The function animates the path being drawn step-by-step, showing the progression
    and marking the cylinders that have been visited. The plot is updated in real-time
    with a pause between each step to visualize the drawing process.
    This also keep track of the fuel and time remaining and the mass of the robot, and show the path in different colors if the robot run out of fuel or time.

    Parameters:
    cylinders (list): A list of cylinder objects, each with a getPosition() method.
    initialPosition (tuple): The initial position (x, y) of the starting point.
    chosenPath (list): A list of points (tuples) representing the path to be visualized.
    """
    # New figure
    _, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    # The already visited cylinders will be put in a list
    alreadyVisitedCylinders = []
    cylinderPosition = [cylinder.getPosition() for cylinder in cylinders]
    # Keep track of mass, remaining time and remaining fuel
    lastTimePointId = None
    remainingTime = sim.totalTime
    lastFuelPointId = None
    remainingFuel = sim.Robot.initialFuelQuantity
    currentMass = 0
    currentPoints = 0
    currentMassWithNoLimits = 0
    currentPointsWithNoLimits = 0
    # We plot the path by slowinglely adding the line one by one
    for point in range(1, len(chosenPath)+1):
        # We clear the plot to avoid superposition
        plt.cla()
        # If the cylinder is in the path, and the robot have fuel and time, we add it to the list of visited cylinders
        # This just check if the final point is close to a cylinder, not if the line goes trough it (can be improved)
        distanceFromCylinders = [distance(chosenPath[point-1], cylinder) for cylinder in cylinderPosition]
        currentlyVisitedCylinder = [cylinderId for cylinderId in range(len(cylinderPosition)) if distanceFromCylinders[cylinderId] < TOO_CLOSE_CYLINDER]
        if lastFuelPointId is None and lastTimePointId is None:
            alreadyVisitedCylinders += currentlyVisitedCylinder
        # We update the remaining time and fuel
        distanceOfSegment = distance(chosenPath[point-1], chosenPath[point]) if point < len(chosenPath) else 0
        remainingTime -= sim.Robot.timeCost(distanceOfSegment, currentMass)
        remainingFuel -= sim.Robot.fuelCost(distanceOfSegment, currentMass)
        # If we don't have enough fuel or time, we store the point where it happened
        lastTimePointId = lastTimePointId if lastTimePointId is not None else point-1 if remainingTime < 0 else None
        lastFuelPointId = lastFuelPointId if lastFuelPointId is not None else point-1 if remainingFuel < 0 else None
        # We update the mass and points
        currentMassWithNoLimits += sum([cylinders[cylinderId].getMass() for cylinderId in currentlyVisitedCylinder])
        currentPointsWithNoLimits += sum([cylinders[cylinderId].getValue() for cylinderId in currentlyVisitedCylinder])
        currentMass = sum([cylinders[cylinderId].getMass() for cylinderId in alreadyVisitedCylinders])
        currentPoints = sum([cylinders[cylinderId].getValue() for cylinderId in alreadyVisitedCylinders])
        # Plot the cylinders and exclude already visited ones
        traceMap(ax, cylinders, initialPosition, alreadyVisitedCylinders)
        # Plot the path
        tracePath(chosenPath[:point], lastFuelPointId, lastTimePointId)
        # Display stats
        displayStats(ax, remainingTime, remainingFuel, currentMass, currentPoints, currentPointsWithNoLimits, currentMassWithNoLimits)
        # We set a pause between each plot so that we can see the path being drawn
        plt.pause(0.3)
    # We show the final plot
    plt.show()
    # Return the number of points
    return currentPoints


def justEstimatePoints(path, cylinders):
    """
    Just estimate the number of points that will be collected by the robot by following the given path.

    Args:
        path (list): A list of positions (tuples) representing the path from the initial position through the ordered cylinders.
        cylinders (list): A list of cylinder objects.

    Returns:
        float: The estimated number of points that will be collected by the robot.
    """
    points = 0
    mass = 0
    remainingTime, remainingFuel = sim.totalTime, sim.Robot.initialFuelQuantity
    for point in range(1, len(path)):
        distanceOfSegment = distance(path[point-1], path[point])
        for cylinder in cylinders:
            if distance(path[point], cylinder.getPosition()) < TOO_CLOSE_CYLINDER:
                points += cylinder.getValue()
                mass += cylinder.getMass()
        remainingTime -= sim.Robot.timeCost(distanceOfSegment, mass)
        remainingFuel -= sim.Robot.fuelCost(distanceOfSegment, mass)
        if remainingTime < 0 or remainingFuel < 0:
            break
    return points