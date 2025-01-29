"""The file to run the program"""

import inoutfilereader as io
import pathsearch as ps
import visualise as vs

# for mapId in range(11):
#     cylinders = io.loadCylinders(f'examples\maps-test\donnees-map-{mapId}.txt')
#     bestOrder = ps.bestOrderOfCylinders(cylinders, (0, 0))
#     path = ps.pathFromCylindersOrder(cylinders, bestOrder, (0, 0))
#     vs.showSimulation(cylinders, (0, 0), path)

cylinders = io.loadCylinders('examples\maps-test\donnees-map-0.txt')
bestOrder = ps.bestOrderOfCylinders(cylinders, (0, 0))
path = ps.pathFromCylindersOrder(cylinders, bestOrder, (0, 0))
vs.showSimulation(cylinders, (0, 0), path)