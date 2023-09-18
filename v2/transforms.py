import numpy as np

def translateMat(pos: np.ndarray):
    mat = np.eye(4,4)
    mat[3,0] = pos[0]
    mat[3,1] = pos[1]
    mat[3,2] = pos[2]
    return mat


def rotateAboutX(rad):
    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[1,1] = ct
    mat[1,2] = st

    mat[2,1] = -st 
    mat[2,2] = ct
    return mat

def rotateAboutY(rad):
    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[0,0] = ct
    mat[0,2] = -st

    mat[2,0] = st 
    mat[2,2] = ct
    return mat

def rotateAboutZ(rad):
    mat = np.eye(4,4)
    ct = np.cos(rad)
    st = np.sin(rad)

    mat[0,0] = ct
    mat[0,1] = st

    mat[1,0] = -st 
    mat[1,1] = ct
    return mat

