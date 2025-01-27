import matplotlib.pyplot as plt

def tracer_point(cylinders):
    for i in cylinders: 
        plt.scatter(i.get('x'),i.get('y'),color=('red' if i.get('cat')==1 else 'blue' if i.get('cat')==2 else 'green' ),s = 100)
        plt.pause(0.1)
    return ()

def tracer_chemin(path) :
    plt.plot(path)
    plt.pause(0.05)

def show():
    plt.plot(0,0,marker = 'x')
    plt.show()