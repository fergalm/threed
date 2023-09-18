from ipdb import set_trace as idebug
from thing import Thing 
import numpy as np 
import transforms as tf 

"""
Local Coordinates of vertices relative to centre of object 
World Coords of vertices relative to centre of the universe 
Rel   Coords in the world relative to the camera's position 
View  Coords relative to the viewing plane of the camera.
Screen Coords on the screen. Units are pixels. (0,0) at top left
        of screen. col increases to the right, row increases down.
        dist increases for objects further in the background

"""

class Camera:
    def __init__(self, lens, ncols, nrows, horz_fov_degrees):
        self.lens = lens 
        
        #TODO
        #nols, nrows is probably going to be set equal to the
        #screen size. If the screen size changes, these
        #should update
        self.ncols = ncols 
        self.nrows = nrows 
        self.horizontal_fov_rad = np.radians(horz_fov_degrees)
        # self.vertical_fov_rad = self.horizontal_fov_rad * nrows / ncols 
        self.plate_scale_rad_per_pixel = self.horizontal_fov_rad / float(ncols)

        self.state = np.array([0,0,0, 0,0,0], dtype=float)


    def computePixelCoordsForThing(self, th:Thing):
        localToWorld = th.getLocalToWorldMat()
        worldToView = self.getWorldToViewMat()
        mat = np.dot(localToWorld, worldToView)

        #Compute transformation matrix from local to view coords
        view_coords = np.dot(th.vertices, mat)

        #USe lens to covert view coords to degrees and distance 
        ang_coords_rad = self.lens.getAngularCoords_rad(view_coords)

        screen_coords_pix = self.convertAngularToScreenCoords(ang_coords_rad)
        return screen_coords_pix


    def getWorldToViewMat(self):
        mat1 = self.getWorldToRelMat()
        mat2 = self.getRelToViewCoords()
        return np.dot(mat1, mat2)
    
    def getWorldToRelMat(self):
        """
        The the transformation matrix from world coordinates to
        coordinates relative to the camera. The convention is
        that the camera is looking along the x-axis, with z pointing "up"

        Notes
        ------
        This is the camera view, so we do things opposite 
        to the usual way. If the camera moves to the right,
        the objects relative coordinates move to the left.
        If the camera pitches up, the relative coordinates move down.

        Also, we reverse the order of transformations. Translate
        first, then rotate
        
        Returns
        ---------
        A 4x4 matrix
        """

        x, y, z, rho, theta, phi = -1 * self.state 
            
        zmat = tf.rotateAboutZ(phi)
        ymat = tf.rotateAboutY(theta)
        xmat = tf.rotateAboutX(rho)
        tmat = tf.translateMat([x, y, z])
        # idebug()
        mat = np.eye(4)
        mat = np.dot(mat, tmat)
        mat = np.dot(mat, xmat)
        mat = np.dot(mat, ymat)
        mat = np.dot(mat, zmat)
        return mat 

    def getRelToViewCoords(self):
        """
        Convention is that camera lens points in +x direction with +z
        corresponding to up, and +y to left. This matrix converts
        those coordinates to (horzizontal, vertical, and distance)
        coordinates.

        Horizontal == -y 
        Vertical == +z 
        Distance == +x 
        """

        mat = np.zeros((4,4))
        mat[0, 2] = +1
        mat[1, 0] = -1
        mat[2, 1] = +1
        mat[3, 3] = +1  #Keep the w coord unchanged 
        return mat 

    def convertAngularToScreenCoords(self, ang_coords_rad):
        """Convert coordinates in radians from point of view
        to pixels.

        We convert radians to pixels using the platescale, then offset
        the results so that (0,0) in angular coords corresponds to
        the centre of the screen

        Remember (0,0) in pixel coords is the top left of the screen
        so +ve vertical coords are toward the top of the screen and 
        -ve vertical coords are toward the bottom

        Note that the resulting screen coords need not be on
        the screen. Some additional filtering might be required
        """
        col_pix = ang_coords_rad[:,0] / self.plate_scale_rad_per_pixel
        col_pix += .5 * self.ncols

        row_pix = .5 * self.nrows 
        row_pix -= ang_coords_rad[:,1] / self.plate_scale_rad_per_pixel

        out = np.empty_like(ang_coords_rad)
        out[:,0] = col_pix 
        out[:,1] = row_pix 
        out[:,2] = ang_coords_rad[:,2]
        return out 




class BaseLens:
    """Converts view coords to angular coordinates 
    """

    def getAngularCoords_rad(self, vertices):
        """Convert view coordinates to screen coordinaes in pixels

        The only physical lens I can think of right now.
        
        """
        out = np.empty_like(vertices)

        horz = vertices[:,0] / vertices[:,2]
        out[:,0] = np.arctan(horz)

        vert = vertices[:,1] / vertices[:,2]
        out[:,1] = np.arctan(vert)
        out[:,2] = vertices[:,2]
        return out 
    
