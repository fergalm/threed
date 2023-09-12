from ipdb import set_trace as idebug
import numpy as np

#Tip, make this an even number
POINTS_PER_CIRCLE = 48

class Circle():
    def __init__(self, z0, radius):
        self.points = self.makePoints(z0, radius)
        self.facets = self.makeFacets(self.points)
        self.colours = ['grey', 'grey'] * int(len(self.facets)/2)
        self.colours += ['grey']
        assert len(self.colours) == len(self.facets)

    def getConnectingPoints(self):
        return self.points 
        
    def makeFacets(self, points):
        nump = len(points)
        facet = np.zeros((len(points)-2, 3), dtype=int)
        for i in range(0, len(points)-2):
            facet[i] = [nump-1, i, i+1]
        return facet

    def makePoints(self, z0, radius):
        out = np.zeros( (1 + POINTS_PER_CIRCLE, 4))

        rad = np.linspace(0, 2*np.pi, POINTS_PER_CIRCLE)
        idx = np.arange(0, POINTS_PER_CIRCLE)
        out[idx, 0] = radius * np.cos(rad)
        out[idx, 1] = radius * np.sin(rad)
        out[idx, 2] = z0 
        out[idx, 3] = 1
        out[-1] = [0, 0, z0, 1]

        return out

class TruncCone():
    def __init__(self, circle, radius2, height, bottom=False):
        lowerRing = self.makePoints(circle, radius2, height)
        self.points = np.concatenate([circle.points, lowerRing])
        self.bottom = bottom

        facets = self.makeFacets(circle, lowerRing)
        self.facets = np.concatenate([circle.facets, facets])
        clr = ['grey', 'grey'] * int(len(self.facets)/2)
        self.colours = circle.colours + clr 

    def getConnectingPoints(self):
        num = POINTS_PER_CIRCLE + 1
        return self.points[-num:,:]

    def makePoints(self, circle, radius2, height):
        z0 = circle.getConnectingPoints()[0][2]

        out = np.zeros( (1 + POINTS_PER_CIRCLE, 4))
        rad = np.linspace(0, 2*np.pi, POINTS_PER_CIRCLE)
        idx = np.arange(0, POINTS_PER_CIRCLE)
        out[idx, 0] = radius2 * np.cos(rad)
        out[idx, 1] = radius2 * np.sin(rad)
        out[idx, 2] = z0  - height
        out[idx, 3] = 1

        out[-1] = [0, 0, z0-height, 1]
        return out

    def makeFacets(self, circle, points):

        offset = len(circle.points)
        offset2 = offset - len(circle.getConnectingPoints()) - 1
        nump = len(points)

        #The curves sides
        # offset += nump
        curve = np.zeros((2*(nump)+1, 3), dtype=int)
        for i in range(nump-1):
        # for i in range(8):
            curve[2*i] = [offset2 + i, offset + i, offset + i + 1] 
            curve[2*i+1] = [offset2 + i, offset2 + i+1, offset + i + 1]

        if self.bottom:
            #The base of the cone
            disc = np.zeros((nump-2, 3), dtype=int)
            for i in range(0, len(points)-2):
                disc[i] = [offset + nump-1, offset+ i, offset + i+1]
            curve = np.concatenate([disc, curve])
        
        return curve


def makeModel():
    circle = Circle(0, 5)
    cone = TruncCone(circle, 15, 15)
    cycl = TruncCone(cone, 15, 40)

    connector = TruncCone(cycl, 2, 0)
    bell = TruncCone(connector, 8, 10, bottom=True)
    bell.points[:,2] += 30

    # idebug()
    pos = np.array([400, 7, 0])
    attitude = [0, np.radians(10), 0]
    obj  = Apollo(pos, attitude, bell)
    return obj


from sprite import Sprite

class Apollo(Sprite):

    def __init__(self, pos, attitude, shape):
        self.pos = pos 
        self.attitude = attitude
        self.points = shape.points 
        self.facets = shape.facets
        self.colours = shape.colours


import matplotlib.pyplot as plt
from backend import MplBackend
from engine import Engine
from camera import Camera
import time

def main():
    camera = Camera(100)
    backend = MplBackend(800, 600)
    engine = Engine(camera, backend)
    obj = makeModel()

    plt.clf()
    # plt.axis([-8000, 800, -5000, 10_000])
    i = 0
    while True:
        t1 = time.time()
        plt.cla()
        plt.axis([0, 800, 0, 600])
        obj.setAttitude_rad([-np.radians(30), 4 *i *np.radians(1), 0])
        engine.renderSingleSprite(obj)
        t2 = time.time()
        print(1 / (t2-t1) )
        plt.pause(.1)
        i += 1
