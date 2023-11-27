from ipdb import set_trace as idebug
from . import transforms as tf
import numpy as np 

class Thing:
    """A Thing represents a (possibly moving) object in the world.
     
    Another possible name for this concept is an "object", but that
     word has another meaning in object-oriented languages like Python 

    A Thing is compose of:
    1. A series of `n` vertices, an array of 4d points
    representing the corners of the polygons.

    The vertices are coordinates the local coordinate frame, i.e relative
    to some central point in the Thing. The convention is that x-axis
    points "forward", the z-axis points "up", and the y-axis points
    to the "left" of someone inside the object looking forward. 
    x,y, and z obey the right hand rule

    2. A series of `m` edges. An edge is an array of 4 indices
    into the vertex array. Each pair of
    elements in a given row (`edge[i, 0]` and `edge[i,1]`,  or `edge[i,1]` and 
    `edge[i,2]`) represents an edge of the polygon that connects
    two vertices. In a `Thing`, all polygons are triangles, and the
    last vertex is also the zeroth vertex.
    The edges should move anti-clockwise around the figure as seen
    by someone looking at the front face 

    3. An array of colours as 3 elements per colour (e.g RGB, or HSV).
    The colour system isn't specified. The length of colours is the
    same as edges, as there is one colour per triangle

    4. A state vector with elements [x, y, z, ρ, θ, ɸ ].
    * x, y, z represents the location of the centre of the Thing in the world
    coordinate space
    * ρ (rho) is the rotation about the x axis (or roll)
    * θ (theta) is rotation about the y axis (pitch)
    * ɸ (phi) is rotation around the z axis (yaw)

    5. A velocity vector, or d(state)/dt
    """

    def __init__(self, vertices, edges, colours):
        assert vertices.ndim == 2 
        assert vertices.shape[1] == 4
        self.vertices = vertices.astype(float)
        """A `n x 4` array of the Local coordinates of the vertices"""
        self.numVertices = len(vertices)

        assert edges.ndim == 2 
        # assert edges.shape[1] == 3
        self.edges = edges.astype(int)
        """A `m x 3` array.  Each row represents a triangle, each value is an index into vertices"""
        self.numEdges = len(edges)

        self.norms = self._computeNorms()
        """`m x 3` array of vectors representing the normals to the facets in Local coords"""

        #state is x, y, z, rho, theta, phi (roll, tilt, pan)
        self.state = np.array([0,0,0, 0, 0 ,0], dtype=float)
        """See description above"""
        self.velocity = np.array([0,0,0, 0, 0 ,0], dtype=float)
        """First derivative of `state`"""

        #TODO: For debugging I'm allowing strings for colours
        assert len(colours) == len(edges)
        self.colours = colours

    def advance(self, dt:float) -> None:
        """Change the state of the object because an amount of time `dt` has elapsed"""
        self.state += self.velocity * dt 

    def getPolygons(self):
        """
        Get an `m x 3 x 4` array of the polygons that make up the thing.

        `m` is the number of polygons, each polygon is a triangle with 3 vertices,
        and each vertex is a 4 dimensional point

        This function is not very useful, because typically you want to
        transform the coordinates before generating the polygons, and it's 
        much cheaper to do that transformation before creating the polygons.

        Returns 
        ------------
        An `m x 3 x 4` numpy array of coordinates 
        """
        #I love that this is so easy to express
        return self.vertices[self.edges]
        
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

        Example
        ------------
        ```
        mat = Thing.getLocalToWorldMat()
        worldCoords = Thing.vertices @ mat
        ```

        Returns
        ------------
        A `4 x 4` matrix as a numpy array
        """

        rho, theta, phi = self.state[3:]
        # print(rho, theta, phi)

        zmat = tf.rotateAboutZ(phi)
        ymat = tf.rotateAboutY(theta)
        xmat = tf.rotateAboutX(rho)
        tmat = tf.translateMat(self.state[:3])
        # mat = np.eye(4)
        # mat = np.dot(mat, xmat)
        # mat = np.dot(mat, ymat)
        # mat = np.dot(mat, zmat)
        # mat = np.dot(mat, tmat)
        mat = xmat @ ymat @ zmat @ tmat 
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
