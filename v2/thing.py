from ipdb import set_trace as idebug
import transforms as tf
import numpy as np 

"""
A thing (the word object is reserved) is composed
of

1. A series a vertices, an array of 4d points
   representing the corners of the polygons.

   The vertices are coordinates the local coordinate frame, i.e relative
   to some central point in the Thing. The convention is that x-axis
   points "forward", the z-axis points "up", and the y-axis points
   to the "left" of someone inside the object looking forward. 
   x,y, and z obey the right hand rule

2. A series of edges, an array of 4 indices
   into the vertex array. Each pair of
   elements in a given row (edge[i, 0] and edge[i,1],  or edge[i,1] and 
   edge[i,2]) represents and edge of the polygon that connects
   two vertices. In a `Thing`, all polygons are triangles, and the
   last vertex is also the zeroth vertex.
   The edges should move anti-clockwise around the figure as seen
   by someone looking at the front face 

3. An array of colours as 3 elements per colour (e.g RGB, or HSV).
   The colour system isn't specified. The length of colours is the
   same as edges, as there is one colour per triangle

4. A state vector with elements [x, y, z, rho, theta, phi]
   rho is the rotation about the x axis (or roll)
   theta is rotation about the y axis (pitch)
   phi is rotation around the z axis (yaw)

5. A velocity vector, or d(state)/dt
"""

class Thing:
    def __init__(self, vertices, edges, colours):
        assert vertices.ndim == 2 
        assert vertices.shape[1] == 4
        self.vertices = vertices.astype(float)
        self.numVertices = len(vertices)

        assert edges.ndim == 2 
        # assert edges.shape[1] == 3
        self.edges = edges.astype(int)
        self.numEdges = len(edges)

        self.norms = self._computeNorms()

        #state is x, y, z, rho, theta, phi (roll, tilt, pan)
        self.state = np.array([0,0,0, 0, 0 ,0], dtype=float)
        self.velocity = np.array([0,0,0, 0, 0 ,0], dtype=float)

        #TODO: For debugging I'm allowing strings for colours
        assert len(colours) == len(edges)
        self.colours = colours

    def advance(self, dt):
        self.state += self.velocity * dt 

    def getPolygons(self):
        #I love that this is so easy to express
        #It's not very useful because typically you want the 
        #transformed polygons, not the ones in local space
        return self.vertices[self.edges]
    
    # def getNormInWorldCoords(self):
    #     mat = self.getLocalToWorldMat()
    #     return np.dot(self.norms, mat[:3, :3])
    
    def _computeNorms(self):
        """Used during init only"""
        v0 = self.vertices[self.edges[:,0]]
        v1 = self.vertices[self.edges[:,1]]
        v2 = self.vertices[self.edges[:,2]]

        assert v0.shape == (self.numEdges,4)
        vec1 = (v1 - v0)[:,:3]  #Drop the dummy dimension for cross product
        vec2 = (v2 - v0)[:,:3] 
        norm = np.cross(vec1, vec2)
        assert norm.shape == (len(self.edges), 3)
        
        #Normalise
        #TODO Speed me
        length = np.sqrt(norm[:,0]**2 + norm[:,1]**2 + norm[:,2]**2)
        norm /= length.reshape(self.numEdges, 1)
        return norm 


    def getLocalToWorldMat(self):
        """Return a matrix that will convert local coordinates
        to world coordinates 

        ```
        mat = Thing.getLocalToWorldMat()
        worldCoords = np.dot(Thing.vertices, mat)
        ```
        """

        rho, theta, phi = self.state[3:]
        # print(rho, theta, phi)

        zmat = tf.rotateAboutZ(phi)
        ymat = tf.rotateAboutY(theta)
        xmat = tf.rotateAboutX(rho)
        tmat = tf.translateMat(self.state[:3])
        mat = np.eye(4)
        # mat = np.dot(mat, zmat)
        # mat = np.dot(mat, ymat)
        # mat = np.dot(mat, xmat)
        # mat = np.dot(mat, tmat)
        mat = np.dot(mat, xmat)
        mat = np.dot(mat, ymat)
        mat = np.dot(mat, zmat)
        mat = np.dot(mat, tmat)
        return mat 
    


def make_example_thing():
    pp = np.sqrt(3)/2
    vertices = np.array([
        [-pp, -.5, -pp, 1],
        [+pp, -.5, -pp, 1],
        [0,     1, -pp, 1],
        [0,     0, 2.23, 1]
    ])

    edges = np.array(
        [
            [0,2,1],
            [0,1,3],
            [1,2,3],
            [0,3,2],
        ],
        dtype=np.int16
    )

    colours = np.array('r g b c'.split())    

    obj = Thing(vertices, edges, colours)
    obj.state = [0,0,0, 0, 0 ,0]
    return obj
