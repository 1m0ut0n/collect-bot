"""The file to run the program"""

import inoutfilereader as io
import pathsearch as ps
import visualise as vs



def runSimulation(filename, outDir, outFilename, show=True):
    """
    Run the simulation for a given map file.

    This function loads the cylinder data from the specified file, finds the best order of cylinders,
    and visualizes the path generated by the best order.

    Args:
        path (str): The file path to load the cylinder data from.
    """
    # Load cylinder data from the file
    cylinders = io.loadCylinders(filename)
    # Find a dumb of exploration of cylinders
    dumbOrder = ps.dumbOrderOfCylinders(cylinders, (0, 0))
    # Improve it wit 2-opt
    improvedOrder = ps.improveWith2Opt(cylinders, dumbOrder)
    # Generate the path from the best order
    path = ps.pathFromCylindersOrder(cylinders, improvedOrder, (0, 0))
    # Generate the movements for the robot
    movements = ps.generateMouvement(path)
    # Save the movements to a file
    io.saveMovements(movements, outFilename, outDir)
    # Visualize the path
    if show:
        return vs.showSimulation(cylinders, (0, 0), path)
    else:
        return vs.justEstimatePoints(path, cylinders)


if __name__ == "__main__":
    points = []
    for mapId in range(1,11):
        points.append(runSimulation(f'examples\maps-eval\donnees-map-{mapId}.txt', 'dist', f'script-{mapId}.txt', show=False))
    print(points)
    print(sum(points)/len(points))