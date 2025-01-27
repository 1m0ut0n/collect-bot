import numpy as np


def get_cylinder(path, object_cylinder):

    cylinder_array = np.loadtxt(path)
    for i in range(len(cylinder_array)):
        object_cylinder[i].x= cylinder_array[i][0]
        object_cylinder[i].y = cylinder_array[i][1]
        object_cylinder[i].cat = cylinder_array[i][2]
    return object_cylinder 


def give_path(commands_as_array):

    np.savetxt('script', commands_as_array)
