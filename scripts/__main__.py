"""The file to run the program"""

import inoutfilereader as io 
import visualise as vs

cylinders = io.loadCylinders('examples\donnees-map.txt')

vs.tracer_point(cylinders=cylinders)
vs.show()