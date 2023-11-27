# Threed

A toy graphics engine for a flight simulator.


### Coordinate systems 
A 3D graphics engine converts to coordinates of objects in the world into pixel coordinates. 

Each object has it's own internal, or **local** coordinate system. We use the right hand rule to define coordinates

```
      ^ y
      |
      |
      |
      |_______>  x
     /
    /
    z
```

As the object moves and rotates through space, it's local coordinates map to **world**
coordinates in the world in which it moves. It is viewed by a camera, which
sees the object at **relative** coordinates. The lens projects the relative coordinates 
to view coordinates (in units of angles), which are then projected onto a screen,
with units of pixels 


* **Local** Coordinates of vertices relative to centre of object 
* **World** Coords of vertices relative to centre of the universe 
* **Relative**   Coords in the world relative to the camera's position 
* **View**  Coords relative to the viewing plane of the camera.
* **Screen** Coords on the screen. Units are pixels. (0,0) at top left
        of screen. col increases to the right, row increases down.
        dist increases for objects further in the background


### Coordinates and transformations 

#### Matrix multiplication
The code uses the `@` notation throughout for matrix multiplication

```
A @ B == np.dot(A, B)
```

Matrix multiplication fails unless 
```
A.ndim == 2
B.ndim == 3
A.shape[1] = B.shape[0]
```

(This is not quite true, 3d arrays can be multiplied, but that case isn't used in this code)

Matrix multiplication is associative but not communicative 

```
new_mat = mat1 @ mat2 @ mat3  #OK

assert mat1 @ mat2 == mat2 @ mat1  #Usually False
```


#### Coordinates
A coordinate of a single point in space is stored as a 1x4 array of coordinates `[x, y, z, 1]`
(the last coordinate is always set to 1, and simplifies translating the point in space. A polygon with n vertices is stored as an nx4 array

```
x1 y1 z1 1
x2 y2 z2 1
...
xn yn zn 1
```

Coordinates for a single object, are stored in a `v2.thing.Thing` class.

Polygons are mapped between coordinates systems using transformation matrices. See `v2.transforms`. Coordinate arrays are post-multiplied by transformation matrices using the @ notation

```
transformed_coordinates = original_coords @ transform_matrix
```

Note that because matrix multiplication is not commutative, pre-multiplying by a transform matrix will not give you the result you expect 

```
transform_matrix @ original_coords #  DON'T DO THIS!
```


### Developing
* Using numpy to do coordinate transformations 
* Ultimately will use pygame as the 2d graphics engine, getting by just fine with matplotlib so far.
* Using pytest for units tests
* Use `pdoc` to build documentation. `pdoc v2 -o html`