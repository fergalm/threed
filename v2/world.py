from ipdb import set_trace as idebug
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
    def __init__(self, renderer, shader, thinglist, cameraList):
        self.thingList = thinglist 
        self.cameraList = cameraList
        self.renderer = renderer
        self.shader = shader


    def advance(self, dt):
        for t in self.thingList:
            t.advance(dt)

        for cam in self.cameraList:
            for th in self.thingList:
                #Compute relevant coordinates for thing for this camera
                pix_coords = cam.computePixelCoordsForThing(th)
                edges = th.edges
                normals = cam.computeNormalsForThing(th)  #in camera's coord system
                # print("Normals")
                # print(normals)
                # print("\n")
                # print(th.state[:3] - cam.state[:3])
                # print("\n")
                polys = pix_coords[edges]

                # #Filter polygons to just the ones we want to render
                idx = np.ones(len(polys), dtype=bool)
                # idx &= cam.filterPolyForOnScreen(polys)
                idx &= polyFacesCamera(cam, th)
                # idx &= polyIsLargeEnoughToRender(polys)
                # if np.sum(idx) == 0:
                #     continue 
                
                #Display the displayable polygons
                colours = self.shader.shade(th, pix_coords, normals, idx)
                self.renderer.paint(polys[idx], colours)


def polyFacesCamera(cam, th):
    """This is wrong. I want to dot normals with \vec{p} - \vec{c}"""
    normals = cam.computeNormalsForThing(th)
    pos = th.state - cam.state 
    pos = pos[:3]  #The position part of the state only
    # pos = np.array([0,0,1])

    costheta = np.dot(normals, pos)
    # print(f"costheta = {costheta}")
    return costheta < 0


def polyIsLargeEnoughToRender(pix_coords):
    cmin = pix_coords[:, :, 0].min(axis=1)
    cmax = pix_coords[:, :, 0].max(axis=1)
    rmin = pix_coords[:, :, 0].min(axis=1)
    rmax = pix_coords[:, :, 0].max(axis=1)

    minAreaToRender_pix = 2  #TODO: make this an argument?
    area = (cmax - cmin) * (rmax - rmin)
    return area > minAreaToRender_pix



#         #         #If we've gotten this far, start worrying about individ
#         #         #polygons


#         #         #Filter to just the polygons point toward the camera
#         #         costheta = np.dot(cVec, t.norms)
#         #         idx = costheta < 0
#         #         edges = t.edges[idx]
#         #         colours = t.color[idx]

#         #         screenCoords = lens.relToScreenCoords(relVertices, edges)
#         #         for clr, e in zip(colours, edges):
#         #             sc= screenCoords[e] 
#         #             assert sc.shape == (1, 3)

#         #             #When I add lighting, this will be the place
#         #             #to modify the colour on a per polygon basis

#         #             bbox = getBBox(screenCoords[e])

#         #             #Check for very small polygons. We don' need to render those
#         #             if bbox.area < 2:
#         #                 continue  

#         #             isOnScreen = testIsOnScreen(bbox, self.screen)
#         #             if isOnScreen == "OUTSIDE":
#         #                 #No need to plot this polygon
#         #                 continue 
#         #             elif isOnScreen == "INSIDE":
#         #                 polyList = [sc] 
#         #             else:
#         #                 #Clip the polygon, possibly making two polygons 
#         #                 polyList = clipPolygon(sc, self.screen)


#         #             #Call a render to either render wireframes or polygons
#         #             #the code below is for polygons
#         #             for p in polyList:
#         #                 renderPolygons(p, bbox, clr, self.screen)

#         # screen.blit()

# def renderWireframe(poly, bbox, clr, screen):
#     h, w= bbox.height, bbox.width
#     r0, c0 = bbox.y0, bbox.x0 

#     #For edge in polygon 
#         #draw a line with clr 


# def renderPolygons(poly, bbox, clr, screen):

#     h, w= bbox.height, bbox.width
#     r0, c0 = bbox.y0, bbox.x0 

#     slr, slc = slice(r0, r0+h), slice(c0, c0+w) 
#     #Bit of the image to update
#     sprite = screen.buffer[slr, slc] 

#     #Zbuffer tracks distance from camera of objects that paint each pixel 
#     zbuffer = screen[slr, slc] 

#     mask = isInside(poly, sprite) 
#     zmask = computeZmask(poly, sprite) 

#     #Select only pixels inside the polygon and in front of everything thus drawn
#     idx = mask & (zmask < zbuffer)

#     #Draw the polygon 
#     sprite[idx] = clr 

#     #Update zbuffer with locations of things drawn thus far 
#     zbuffer[idx] = zmask[idx]