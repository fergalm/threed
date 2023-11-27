
#Draw two different views of the same object.
#Is it like watching a 3d movie?

from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import numpy as np 
from . import readobj 
from . import world 
from . import camera
from . import shade
from . import thing 
from . import render 


class Mover: 
    def __init__(self, wrld: world.World):
        self.world = wrld 
        self.camera = wrld.cameraList[0]
        self.thing = wrld.thingList[0]


        self.fig1 = plt.gcf() 
        self.updateEvent = 'key_press_event'
        self.fig1.canvas.mpl_disconnect(self.updateEvent)
        self.fig1.canvas.mpl_connect(self.updateEvent, self)

        plt.figure(self.fig1.number)
        plt.clf()
        self.world.advance(1)

    # def __del__(self):
        # self.disconnect()

    def __call__(self, event):
        key = event.key 

        ang = np.radians(10)

        if key == '3':
            self.thing.state[0] += 5 
        elif key == 'w':
            self.thing.state[1] += 5 
        elif key == 'e':
            self.thing.state[0] -= 5 
        elif key == 'r':
            self.thing.state[1] -= 5 
        elif key == 't':
            self.thing.state[2] -= 5
        elif key == 'g':
            self.thing.state[2] += 5
        if key == 'i':
            self.thing.state[4] += ang
        elif key == 'j':
            self.thing.state[5] += ang
        elif key == 'k':
            self.thing.state[4] -= ang 
        elif key == 'l':
            self.thing.state[5] -= ang
        elif key == 'p':
            self.thing.state[3] -= ang
        elif key == ';':
            self.thing.state[3] += ang


        print(self.thing.state)
        self.world.advance(1) 
        plt.axis(self.camera.getFrame())
        plt.pause(.01)


    def disconnect(self):
        # self.fig1.canvas.mpl_disconnect(self.updateEvent)
        pass 

def main():
    fn = "../data/models_resources/Xwing_0_0.obj"
    th = readobj.read_points(fn)
    # th = thing.make_example_thing()
    # th = makeFlatSquare()
    th.state[0] = 5

    # th.state = np.array([100,0,0,0,0,np.pi/2], dtype=float)
    # th.state = np.array([15., 0., 0., -22.34021443,   5.41052068, 2.96705973 ])
    # th.state = np.array([5., 0., 0., -22.34021443,  5.41052068, -1.04719755])
    # th.state = np.array([  5., 0., 0., -19.3731547, 5.41052068,  -1.04719755])
    bbox1 = camera.Bbox(0, 0, 400, 400)
    cam1 = camera.Camera(camera.BaseLens(), bbox1, 40)

# [ 15.           0.           0.         -22.34021443   5.41052068
#    2.96705973]

    shader = shade.AmbientLightShader()
    renderer = render.PolygonMplRender() 
    # renderer = render.NumberedPolygonRender()
    # renderer = render.DebugPolygonRender()
    wrld = world.World(renderer, shader, [th], [cam1])


    plt.clf()
    plt.gcf().set_size_inches((4,4))
    plt.axis([0, 400, 0, 800])
    m = Mover(wrld)
    # m(None)
    return m


from thing import Thing
def makeFlatSquare():
    pp = np.sqrt(3)/2
    vertices = np.array([
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [0, 1, 1, 1],
    ])

    edges = np.array(
        [
            [0,1,2],  #Points away at the start red
            [1,2,3],  #Points toward at start   green
            # [0,2,1],   #Back plane of 0th triangle  magenta
            # [1,3,2],    #Back plane of 1th triangle  cyan
        ],
        dtype=np.int16
    )

    colours = np.array('r g m c'.split())    
    colours = np.array('r g'.split())    

    obj = Thing(vertices, edges, colours)
    obj.state = [0,0,0, 0, 0 ,0]
    return obj


if __name__ == "__main__":
    main()