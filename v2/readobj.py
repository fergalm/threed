from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import numpy as np 

from thing import Thing 

def read_points(fn):
    """This only works on the xwing file 'til I figure out 
    the full format
    """

    points = []
    edges = []
    normals = []
    with open(fn) as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            if line[:2] == 'v ':
                words = line.split()
                values = list(map(float, words[1:]))
                points.append(values)
            if line[:2] == 'f ':
                words = line.split()
                values = list(map(lambda x: float(x.split('/')[0]), words[1:]))

                if len(values) == 3:
                    values.append(values[0])
                edges.append(values)
            if line[:2] == 'vn':
                words = line.split()
                values = list(map(float, words[1:]))
                normals.append(values)                

    points = np.array(points)
    edges = np.array(edges) - 1
    normals = np.array(normals)
    out = np.zeros((len(points), 4))
    
    #Transpose so x-wing points toward +x
    out[:,0] = -points[:,2]
    out[:,1] = points[:,0]
    out[:,2] = points[:,1]
    out[:,3] = 1

    # idebug()
    clrs = np.zeros((len(edges), 3))
    ch = np.random.rand(len(edges))*.9
    clrs[:,0] = ch
    clrs[:,1] = (1 - ch) / 2. 
    clrs[:,2] = (1 - ch) / 2. 
    # clrs[:,2] = ch
    # for i in range(3):
    #     # clrs[:,i] = np.linspace(0, .9, len(edges))[::-1]
    #     clrs[:,i] = ch
    #     # clrs[:,i] = np.random.rand(len(edges))*.9

    # clrs = np.array(['r'] * len(edges))
    th = Thing(out, edges, clrs)
    # th.norms = normals 
    return th 


