"""This file can help find the best parameter for the ponderation"""

import inoutfilereader as io
import pathsearch as ps
import visualise as vs
import random
import concurrent.futures as cf


def monteCarlo(nbIteration, maxWorkers=32, log=False) :
    """
    Perform a Monte Carlo simulation to optimize parameters for a given number of iterations.

    This function adjusts the parameters `VALUE_IMPORTANCE`, `MASS_IMPORTANCE`, and `TIME_IMPORTANCE`
    randomly within specified ranges and evaluates the performance of these parameters using a set of maps.
    The performance is measured by estimating points for the path generated by the best order of cylinders.
    This use multithreading to accelerate the process.

    Args:
        nbIteration (int): The number of iterations to run the Monte Carlo simulation.
        maxWorkers (int, optional): The maximum number of workers to use for multithreading. Defaults to 10.
        log (bool, optional): Whether to log the results of each iteration. Defaults to False.

    Returns:
        tuple: A tuple containing two lists:
            - triedParams (list of tuples): Each tuple contains the parameters 
                (VALUE_IMPORTANCE, MASS_IMPORTANCE, DISTANCE_IMPORTANCE) used in each iteration.
            - result (list of float): The average points estimated for each set of parameters.
    """
    # To store the results and the tested parameters
    triedParams, result = [], []
    # We load all the maps
    maps = [io.loadCylinders(f'examples/maps-eval/donnees-map-{i}.txt') for i in range(1, 11)]
    # We start the a multithreaded executor to accelerate the process
    with cf.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        # For each iteration, we run the simulation with random parameters
        futures = {executor.submit(testRandomParameters, (0, 1), (0, 1), maps): iteration for iteration in range(nbIteration)}
        # We check for completed processes
        for completedFutures in cf.as_completed(futures):
            iteration = futures[completedFutures]
            # We try to get the result
            try:
                avg, triedParam = completedFutures.result()
            # If an exception is raised, we print it
            except Exception as exc:
                print(f"[{iteration}/{nbIteration}] /!\\ Exception: {exc}")
            # If everything is fine, we append the average points and the parameters
            else:
                result.append(avg)
                triedParams.append(triedParam)
                if log :
                    print(f"[{iteration}/{nbIteration}] Parameters: {triedParam}, Average points: {avg}")
    # Return all the results
    return triedParams, result


def testRandomParameters(minMaxTimeMass, minMaxValue, maps):
    """
    Set random values for the parameters and run the simulation for each map.

    Parameters:
    minMaxTimeMass (tuple): A tuple containing the minimum and maximum values for time and mass importance.
    minMaxValue (tuple): A tuple containing the minimum and maximum values for value importance.

    Returns:
    tuple: A tuple containing the average points from the simulations and the randomly set parameters 
           (TIME_IMPORTANCE, MASS_IMPORTANCE, VALUE_IMPORTANCE).
    """
    # Set randomly the values of the parameters
    ps.TIME_IMPORTANCE = random.uniform(0,1)
    ps.MASS_IMPORTANCE = 1 - ps.TIME_IMPORTANCE
    ps.VALUE_IMPORTANCE = random.uniform(0,1)
    # For each map, rum the simulation and return the points and parameters
    return getAverageOnMaps(maps), (ps.TIME_IMPORTANCE, ps.MASS_IMPORTANCE, ps.VALUE_IMPORTANCE)


def getAverageOnMaps(maps):
    """
    Calculates the average points from cylinder data across multiple maps.

    This function iterates through a predefined range of map IDs, loads cylinder data for each map,
    determines an initial order of exploration for the cylinders, improves this order using a 2-opt
    algorithm, and generates a path based on the improved order. The average points from all maps
    are then calculated and stored.

    Returns:
        float: The average points estimated for the given maps.
    """
    points = []
    for cylinders in maps:
        # Find a dumb of exploration of cylinders
        dumbOrder = ps.dumbOrderOfCylinders(cylinders, (0, 0))
        # Improve it wit 2-opt
        improvedOrder = ps.improveWith2Opt(cylinders, dumbOrder)
        # Generate the path from the best order
        path = ps.pathFromCylindersOrder(cylinders, improvedOrder, (0, 0))
        # Estimate the points
        points.append(vs.justEstimatePoints(path, cylinders))
    # Return the average
    return sum(points)/len(points)



if __name__ == "__main__":
    triedParams, result = monteCarlo(10000, log=True)
    maxResult = max(result)
    print(f"Best parameters: {triedParams[result.index(maxResult)]}, Best average points: {maxResult}")