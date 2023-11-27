

class Body to encode and manipulate state 
x A Lens class
    Understand focal length, fisheye lens, telephoto lens etc.
x Camera class should make sure ncols, nrows, fov are always consistent
x Renders
    x PointCloud 
    x WireFrame
    x FillPolygon 

x Lighting 
    x Ambient Light shader 
    o Single infinite source shader
    o A way of combining shaders 

x Read in the xwing file
x 3d model 

o Camera, lens and detector should be separate modules 
o Light source combination. .5*Ambient + .5 * InfinitePointSource(vec)
o A zbuffer
O I have 2 bbox classes. I need to merge them


