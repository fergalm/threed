import numpy as np

__doc__ = """
A module of functions to create matrices to transform coordinates between
coordinate systems by means of translations and rotations. 

Other transformations such as stretch and shear are not implemented yet.

The language to descript rotations depends on the context used. Navigation
uses roll, pitch, and yaw, while cinematography uses roll, tilt, and pan.

For an aeroplane, or a camera, roll mean to rotate around the axis pointing
"straight ahead". The objects in front of you, or in scene, remain in front of you,
but objects that were previously at the top of the screen are now on the left of 
the screen.

Pitch, or tilt means to rotate the camera up or down. A plane pitching up starts
to gain altitude, a camera pitching up can now view things higher than itself.


Yaw, or pan means to rotate right or left. A plane yaws to change its compass direction,
a camera pans to look at objects to either side of it.

"""

def translateMat(pos: np.ndarray) -> np.ndarray:
    """Create a transformation matrix that moves some points without rotation

    Inputs
    ------------
    pos
        `[dx, dy, dz]` Increase the `x` value to `x + dx`, etc. 


    Returns
    -----------
    A `4 x 4` matrix as an np.ndarray
    """

    mat = np.eye(4,4)
    mat[3,0] = pos[0]
    mat[3,1] = pos[1]
    mat[3,2] = pos[2]
    return mat


def rotateAboutX(rad:float) -> np.ndarray:
    """Roll the coordinates around the x-axis.

    Inputs
    ------------
    * rad
        * Angle to rotate, in radians 

    Returns
    -----------
    A `4 x 4` matrix as an np.ndarray


    Example
    -----------
    ```python
    p = [0, 0, 1, 1]  #A unit z-vector
    M = rotateAboutX( np.pi/2)
    assert np.allclose( p @ M, [0, -1, 0, 1])
    ```

    """

    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[1,1] = ct
    mat[1,2] = st

    mat[2,1] = -st 
    mat[2,2] = ct
    return mat

def rotateAboutY(rad:float) -> np.ndarray:
    """Pitch, or tilt,  the coordinates around the y-axis.

    Inputs
    ------------
    * rad
        * Angle to rotate, in radians 


    Returns
    -----------
    A `4 x 4` matrix as an np.ndarray


    Example
    -----------
    ```python
    p = [1, 0, 0, 1]  #A unit x-vector
    M = rotateAboutY( np.pi/2)
    assert np.allclose( p @ M, [0, 0, 1, 1])
    ```

    """

    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[0,0] = ct
    mat[0,2] = -st

    mat[2,0] = st 
    mat[2,2] = ct
    return mat

def rotateAboutZ(rad:float) -> np.ndarray:
    """Yaw, or pan,  the coordinates around the y-axis.

    Inputs
    ------------
    * rad
        * Angle to rotate, in radians 


    Returns
    -----------
    A `4 x 4` matrix as an np.ndarray


    Example
    -----------
    ```python
    p = [1, 0, 0, 1]  #A unit x-vector
    M = rotateAboutZ( np.pi/2)
    assert np.allclose( p @ M, [0, 1, 0, 1])
    ```

    """

    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[0,0] = ct
    mat[0,1] = st

    mat[1,0] = -st 
    mat[1,1] = ct
    return mat

