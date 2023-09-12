from ipdb import set_trace as idebug
import matplotlib.pyplot as plt
import numpy as np 

from sprite import Sprite
import transforms as tf

class Camera():
    def __init__(self):
        self.pos = np.array([-5,0,0,1])

    def renderEnvelope(self, obj:Sprite):
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

    def renderShape(self, obj:Sprite):
        points = obj.getPoints()
        loc = obj.getPosition()
        ang = obj.getAttitude_rad()
        tpoints = self.transform(points, loc, ang)
        ang = self.project(tpoints)

        ax = plt.gca()
        facets = obj.facets 
        centroid = np.sum(tpoints[facets, :], axis=1) / 3

        # print(obj.colours)
        # print(tpoints)
        # print(centroid)
        # print(ang)
        # idebug()        
        #The way it should be computed
        #dist = np.sum((centroid - self.pos)**2, axis=1)
        #Consistent with my dummy projection
        dist = (centroid - self.pos)[:,2]
        srt = np.argsort(dist)[::-1]

        for i in range(len(facets)):
            j = srt[i] 
            fac = facets[j]
            corners = ang[fac]
            clr = obj.colours[j]
            # wireframe(corners, clr)
            patch(corners, clr)

            cent = centroid[j]
            cent = self.project(cent.reshape(1, 4))
            # plt.plot(cent[0,0], cent[0,1], 'k.')
            # plt.text(cent[0,0], cent[0,1], " %s %.4f" %(clr, dist[j]))
        plt.plot(ang[-1,0], ang[-1,1], 'mo')


    def transformEnvelope(self, obj):
        """Rotate and move"""
        points = obj.getEnvelope()
        pos = obj.getPosition()
        ang = obj.getAttitude_rad()

        return self.transform(points, pos, ang)

    def transform(self, points, pos, ang):
        """
        TODO
        
        * Am I rotating my angles correctly?
        * Account for moving camera (requires an update to projection method)
        """
        t1 = tf.translateMat(pos)  
        t2 = tf.translateMat(-self.pos)

        #TODO, use Euler angles!
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
        #Project onto xy plane
        return points[:, 0:2]
        # return points[:, 1:3]


def wireframe(points, clr):
    for i in range(len(points)):
        x = points[ [0,1,2,0], 0]
        y = points[ [0,1,2,0], 1]
        plt.plot( x, y, '-', color=clr )


def patch(corners, clr):
    patch = plt.Polygon(corners, color=clr, ec='k')
    plt.gca().add_patch(patch)
