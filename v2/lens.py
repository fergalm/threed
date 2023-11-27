
import numpy as np 

class BaseLens:
    """Converts Relative to View coords.

    View coordinates are in units of radians 

    The base class does a simple geometric transform, but more complicated
    lens, like telephoto or fisheye, are also possible.
    """

    def getAngularCoords_rad(self, vertices):
        """Get the angular coordinates of the vertices 

        Inputs
        ---------
        * vertices
            * A `n x 3` numpy array. Each row represents a single point.
            The columns are x, y, z, and w (which is always set to 1)


        Returns 
        --------
        An `n x 4` numpy array, The columns are 
        horizontal angle, vertical angle, distance, and w
        An angle of (0,0,*,1) represnts a point that is projected onto
        the centre of the image axis. 


        ```
            | y
            |
            |
            |________ x  ----> Lens central axis
           /
          / z
        ```

        Is converted to an image with +z in the horizontal direction and
        -y in the vertical direction.
          
        ```
             ________ z         
            |
            |
            |
            | y
        ```

        Points with smaller +ve values of x are projected in front of points with
        larger values of x. -ve values of x correspond to objects behind the lens,
        which should not ordinarly be display. 
        """
        out = np.empty((len(vertices), 3), dtype=vertices.dtype)

        horz = vertices[:,0] / vertices[:,2]
        out[:,0] = np.arctan(horz)

        vert = vertices[:,1] / vertices[:,2]
        out[:,1] = np.arctan(vert)
        out[:,2] = vertices[:,2]
        return out 
