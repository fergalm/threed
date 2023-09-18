import numpy as np 

class Screen:
    def __init__():
        self.buffer = None 
        self.zbuffer= None 

    def blit(self):
        ... 



class BBox:
    ...

    @property 
    def height(self):
        return self.y2 - self.y1 
    
    @property 
    def width(self):
        return self.x2 - self.x1 
    
    @property 
    def area(self):
        return self.height * self.width 
    

class World:
    def __init__(self, render, thinglist, cameraList, screen):
        self.thinglist = thinglist 
        self.cameraList = cameraList
        self.screen = screen 
        self.render = render


    def advance(self, dt):
        for t in self.thingList:
            t.advance(dt)

        for c in self.cameraList:
            worldToScreen = c.getWorldToRelMat()
            cVec = c.getCameraVec() 
            lens = c.getLens()

            for t in self.thingList:
                localToWorld = t.getLocalToWorldMat()

                
                mat = np.dot(localToWorld, worldToScreen)
                pix_coords = np.dot(t.vertices, mat)

                zMin = np.min(pix_coords[:,2])
                if zMin < 1:
                    continue 

                zMax = np.max(pix_coords[:,2])
                if zMax > self.zMax:
                    continue 

                #Are we all the way off screen?
                cmin, cmax = pix_coords[:,0].min(), pix_coords[:,1].max()
                rmin, rmax = pix_coords[:,0].min(), pix_coords[:,1].max()

                if cmax < 0 or cmin > c.ncols:
                    continue

                if rmax < 0 or rmin > c.nrow:
                    continue

                self.render.paint(t, pix_coords)




        #         #If we've gotten this far, start worrying about individ
        #         #polygons


        #         #Filter to just the polygons point toward the camera
        #         costheta = np.dot(cVec, t.norms)
        #         idx = costheta < 0
        #         edges = t.edges[idx]
        #         colours = t.color[idx]

        #         screenCoords = lens.relToScreenCoords(relVertices, edges)
        #         for clr, e in zip(colours, edges):
        #             sc= screenCoords[e] 
        #             assert sc.shape == (1, 3)

        #             #When I add lighting, this will be the place
        #             #to modify the colour on a per polygon basis

        #             bbox = getBBox(screenCoords[e])

        #             #Check for very small polygons. We don' need to render those
        #             if bbox.area < 2:
        #                 continue  

        #             isOnScreen = testIsOnScreen(bbox, self.screen)
        #             if isOnScreen == "OUTSIDE":
        #                 #No need to plot this polygon
        #                 continue 
        #             elif isOnScreen == "INSIDE":
        #                 polyList = [sc] 
        #             else:
        #                 #Clip the polygon, possibly making two polygons 
        #                 polyList = clipPolygon(sc, self.screen)


        #             #Call a render to either render wireframes or polygons
        #             #the code below is for polygons
        #             for p in polyList:
        #                 renderPolygons(p, bbox, clr, self.screen)

        # screen.blit()

def renderWireframe(poly, bbox, clr, screen):
    h, w= bbox.height, bbox.width
    r0, c0 = bbox.y0, bbox.x0 

    #For edge in polygon 
        #draw a line with clr 


def renderPolygons(poly, bbox, clr, screen):

    h, w= bbox.height, bbox.width
    r0, c0 = bbox.y0, bbox.x0 

    slr, slc = slice(r0, r0+h), slice(c0, c0+w) 
    #Bit of the image to update
    sprite = screen.buffer[slr, slc] 

    #Zbuffer tracks distance from camera of objects that paint each pixel 
    zbuffer = screen[slr, slc] 

    mask = isInside(poly, sprite) 
    zmask = computeZmask(poly, sprite) 

    #Select only pixels inside the polygon and in front of everything thus drawn
    idx = mask & (zmask < zbuffer)

    #Draw the polygon 
    sprite[idx] = clr 

    #Update zbuffer with locations of things drawn thus far 
    zbuffer[idx] = zmask[idx]