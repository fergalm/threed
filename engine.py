from ipdb import set_trace as idebug
import matplotlib.pyplot as plt
import numpy as np 

from sprite import Sprite
import transforms as tf

class Engine():
    def __init__(self, camera, backend):
        self.pos = np.array([0,0,0,1])
        self.backend = backend 
        self.camera = camera 
    def renderEnvelope(self, obj:Sprite):

        raise NotImplementedError("Needs updating")
        loc = self.transformEnvelope(obj)
        ang = self.project(loc)

        # print(loc)
        # print(ang)
        style = dict(
            color='g',
            lw=1,
        )

        style3 = dict(
            color='b',
            lw=1,
        )

        style2 = dict(
            color='r',
            lw=1,
            ls='--',
        )

        for i in range(4):
            pass
            plt.plot(ang[i:i+2,0], ang[i:i+2, 1], **style)
            plt.plot(ang[i+4:i+6,0], ang[i+4:i+6, 1], **style3)

        plt.plot(ang[[3,0],0], ang[[3,0], 1], **style)        
        plt.plot(ang[[7,4],0], ang[[7,4], 1], **style3)        

        for i in range(4):
            plt.plot(ang[[i,i+4],0] , ang[[i,i+4], 1], **style2)        

    def renderSingleSprite(self, obj:Sprite):
        points = obj.getPoints()
        facets = obj.getFacets ()
        loc = obj.getPosition()
        attitude = obj.getAttitude_rad()

        #Zdist acutally distance along x axis
        tpoints = self.transform(points, loc, attitude)
        img_plane_coords = self.project(tpoints)
        zdist = compute_zdist(tpoints, facets)

        srt = np.argsort(zdist)[::-1]
        for i in range(len(facets)):
            if zdist[i] < 1:
                continue 

            j = srt[i] 
            fac = facets[j]
            corners = img_plane_coords[fac]
            clr = obj.colours[j]
            # wireframe(corners, clr)
            self.backend.patch(corners, clr)
            
            # mark_centroids(c2, zdist[j], clr)
            self.backend.mark_centroids(corners, zdist[j], clr)

        #Doesn't belong here, but helpful for debuggin
        ang = img_plane_coords
        plt.plot(ang[-1,0], ang[-1,1], 'mo')

    def renderScene(self, scene:list):
        raise NotImplementedError()

    def transformEnvelope(self, obj):
        """Rotate and move"""
        points = obj.getEnvelope()
        pos = obj.getPosition()
        ang = obj.getAttitude_rad()

        return self.transform(points, pos, ang)

    def transform(self, points, pos, ang):
        """
        TODO
        
        """
        t1 = tf.translateMat(pos)  
        t2 = tf.translateMat(-self.camera.pos)

        #TODO, use Euler angles?
        r1 = tf.rotateAboutZ(ang[2])
        r2 = tf.rotateAboutY(ang[1])
        r3 = tf.rotateAboutX(ang[0])

        #Transformations are listed in reverse order
        #(First operation is listed last)
        transform = np.eye(4,4)

        #Transform to coords relative to camera
        #TODO, account for camera attitude
        transform = np.dot(t2, transform)

        transform = np.dot(t1, transform)
        transform = np.dot(r3, transform)
        transform = np.dot(r2, transform)
        transform = np.dot(r1, transform)

        # print("The transform is")
        # print(transform)
        # idebug()
        #Apply the transform
        points = np.dot(points, transform)
        return points

    def project(self, points):
        """project onto image plane"""

        # # return points[:, 1:3]

        # alpha_rad = points[:,2] / (points[:,0] + 0)
        # beta_rad = points[:,1] / (points[:,0] + 0)


        alpha_rad = np.arctan2(points[:,2], points[:,0])
        beta_rad = np.arctan2(points[:,1], points[:,0]) 

        out = np.vstack([alpha_rad, beta_rad]).transpose()
        # print(points) #[:, 1:3])
        # print(out)
        # print(np.degrees(out))
        # idebug()
        return out

    def transform_to_device_coords(self, ang):
        """Transform angular values to pixel values"""
        return np.dot(ang, np.eye(2)) 




def compute_zdist(tpoints, facets):
    """Compute distance of transformed facets from camera
    in the planar direction.
    
    Somewhat confusingly, the points are transformed
    so the distance in the viewing direction is along
    the x-axis, but the variable name is z-distance.

    Inputs
    ---------
    tpoints
        (n x 4 numpy array) Transformed vertices of the
        object.

    facets
        (n x 3 numpy array of ints) indices of tpoints
        that define each facet.

    """
    centroid = np.sum(tpoints[facets, :], axis=1) / 3
    zdist = centroid[:,0]
    return zdist
