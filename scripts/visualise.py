"""Script to handle the visualisation of the cylinder decision and dicided path with Matplotlib."""
import matplotlib.pyplot as plt
from pathsearch import distance, TOO_CLOSE_CYLINDER
from simulation import Cylinder


def traceMap(ax, cylinders, initialPosition, visitedCylindersId = []):
    """
    Plots a scatter plot of cylinders on a map using matplotlib.
    Use the `show()` function to display the plot.

    Args:
        cylinders (list): List of cylinders.
    """
    # We plot all the cylinders
    for cylinderId in range(len(cylinders)):
        cylinder = cylinders[cylinderId]
        color = 'red' if cylinder.cat == 1 else 'green' if cylinder.cat == 2 else 'blue'
        ax.add_patch(plt.Circle((cylinder.x, cylinder.y), radius=Cylinder.touchingRadius, color='gray', alpha=0.05 if cylinderId in visitedCylindersId else 0.2))
        ax.add_patch(plt.Circle((cylinder.x, cylinder.y), radius=Cylinder.radius, color=color, alpha=0.3 if cylinderId in visitedCylindersId else 1))
    # We plot the initial position
    plt.plot(initialPosition[0], initialPosition[1], marker='x', color='black', markersize=10)

def tracePath(path) :
    """
    Plots the given path on a graph with a black dotted line and pauses briefly to visualize the drawing process.
    Use the `show()` function to display the plot.

    Parameters:
    path (list of tuples): A list of (x, y) coordinates representing the path to be plotted.
    """
    # And plot with an added point
    plt.plot([p[0] for p in path], [p[1] for p in path], color='black', linestyle=':', linewidth=2)


def showSimulation(cylinders, initialPosition, chosenPath):
    """
    Visualizes the simulation by seeing the path being drawn and the cylinder get recolted.

    Parameters:
    cylinders (list): A list of cylinder objects, each with a getPosition() method.
    initialPosition (tuple): The initial position (x, y) of the starting point.
    chosenPath (list): A list of points (tuples) representing the path to be visualized.

    The function animates the path being drawn step-by-step, showing the progression
    and marking the cylinders that have been visited. The plot is updated in real-time
    with a pause between each step to visualize the drawing process.
    """
    # New figure
    _, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    # The already visited cylinders will be put in a list
    alreadyVisitedCylinders = []
    cylinderPosition = [cylinder.getPosition() for cylinder in cylinders]
    # We plot the path by slowinglely adding the line one by one
    for point in range(1, len(chosenPath)+1):
        # We clear the plot to avoid superposition
        plt.cla()
        # If the cylinder is in the path, we add it to the list of visited cylinders
        # This just check if the final point is close to a cylinder, not if the line goes trough it (can be improved)
        distanceFromCylinders = [distance(chosenPath[point-1], cylinder) for cylinder in cylinderPosition]
        alreadyVisitedCylinders += [cylinderId for cylinderId in range(len(cylinderPosition)) if distanceFromCylinders[cylinderId] < TOO_CLOSE_CYLINDER]
        #alreadyVisitedCylinders.append(cylinders.index(chosenPath[i-1]))
        # Plot the cylinders and exclude already visited ones
        traceMap(ax ,cylinders, initialPosition, alreadyVisitedCylinders)
        # Plot the path
        tracePath(chosenPath[:point])
        # We set a pause between each plot so that we can see the path being drawn
        plt.pause(0.3)
    # We show the final plot
    plt.show()