
import numpy as np
import camera
import thing 

class DummyScreen:
    pass 

class DummyLens:
    pass 


def test_camera_smoke():
    th = makeBoxThing()
    th.state[1] = 10

    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0,0,0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    assert mat.shape == (4,4)
    rel = np.dot(th.vertices, mat)
    print(rel)

def test_track_camera_inout():
    """Compute relative coordinates.

    This tests an implementation detail in the Camera that's tricky to
    get right
    """

    th = makeBoxThing()

    th.state[0] = 10  #Put the thing 10 points in front of camera

    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0,0,0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    relcoords = np.dot(th.vertices, mat)

    diff = relcoords - th.vertices 
    assert np.allclose(diff[:,0], 10)
    assert np.allclose(diff[:,1:], 0)


def test_track_camera_leftright():
    """Compute relative coordinates.

    This tests an implementation detail in the Camera that's tricky to
    get right
    """
    
    th = makeBoxThing()
    th.state[1] = 10  #Put the thing 10 points in front of camera

    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0,0,0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    relcoords = np.dot(th.vertices, mat)

    diff = relcoords - th.vertices 
    assert np.allclose(diff[:,1], 10)
    assert np.allclose(diff[:,0], 0)
    assert np.allclose(diff[:,2:], 0)


def test_track_camera_updown():
    """Compute relative coordinates.

    This tests an implementation detail in the Camera that's tricky to
    get right
    """
    
    th = makeBoxThing()

    th.state[2] = 10  #Put the thing 10 points in front of camera

    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0,0,0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    relcoords = np.dot(th.vertices, mat)

    diff = relcoords - th.vertices 
    assert np.allclose(diff[:,2], 10)
    assert np.allclose(diff[:,3:], 0)
    assert np.allclose(diff[:,:2], 0)


def test_camera_pan():
    th = makeBoxThing()

    ang = np.radians(60)
    th.state[0] = 10
    
    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0, 0,ang])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    # mat = np.dot(localToWorld, worldToRel)
    # relcoords = np.dot(th.vertices, mat)
    mat = localToWorld @ worldToRel
    relcoords = th.vertices @ mat

    #In relcoords
    #X value decrease
    #y values go negative 
    #z values untouched
    assert np.all((relcoords[:,0] >= 5) & (relcoords[:,0] < 6)), relcoords[:,0]
    assert np.all(relcoords[:,1] < -8)
    assert np.allclose(relcoords[:,2], th.vertices[:,2] )


def test_camera_tilt():
    th = makeBoxThing()

    ang10 = np.radians(10)
    th.state[0] = 10
    
    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0, ang10, 0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    
    worldCoords = np.dot(th.vertices, localToWorld)
    relcoords = np.dot(th.vertices, mat)
    print(mat)
    print(relcoords)

    assert np.all(relcoords[:,0] < worldCoords[:,0])
    assert np.allclose(relcoords[:,1],  worldCoords[:,1])
    assert np.all(relcoords[:,2] > worldCoords[:,2])


def test_camera_roll():
    th = makeBoxThing()

    ang10 = np.radians(60)
    th.state[0] = 10
    
    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, ang10, 0, 0])

    localToWorld = th.getLocalToWorldMat()
    worldToRel = cam.getWorldToRelMat()
    mat = np.dot(localToWorld, worldToRel)
    
    worldCoords = np.dot(th.vertices, localToWorld)
    relcoords = np.dot(th.vertices, mat)
    print(worldCoords)
    print(relcoords)

    expected = [
        [10.,         0.,         0.,         1.       ],
        [11.,         0.,         0.,         1.       ],
        [10. ,        0.5,       -0.8660254,  1.       ],
        [10.,         0.8660254,  0.5,        1.       ],
    ]
    assert np.allclose(relcoords, expected)



def test_world_to_view_coords():
    th = makeBoxThing()
    th.state[0] = 10  #Put the thing 10 points in front of camera

    cam =  camera.Camera() 
    cam.state = np.array([0,0,0, 0,0,0])  #Camera at origin

    mat1 = th.getLocalToWorldMat()
    mat2 = cam.getWorldToViewMat()
    mat = mat1 @ mat2

    print(th.vertices)
    print(np.dot(th.vertices, mat1))
    print(np.dot(th.vertices, mat))

    view_coords = np.dot(th.vertices, mat)

    expected = [
        [ 0.,  0., 10.,  1.],
        [ 0.,  0., 11.,  1.],
        [-1.,  0., 10.,  1.],
        [ 0.,  1., 10.,  1.],
    ]
    assert np.allclose(view_coords, expected)


def makeBoxThing():
    vertices = np.array([
        [0, 0, 0, 1],
        [1, 0, 0 ,1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
    ])

    edges = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
    ])

    th = thing.Thing(vertices, edges, ['r', 'g', 'b'])
    return th 