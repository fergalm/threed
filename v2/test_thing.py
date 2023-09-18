from ipdb import set_trace as ipdb
import numpy as np
import thing 


def test_world_matrix_smoke():
    th = thing.make_example_thing()

    mat = th.getLocalToWorldMat()
    exp = np.eye(4)
    assert np.allclose(mat, exp), mat

def test_world_matrix_translations():
    th = thing.make_example_thing()

    th.state = [1,0,0, 0,0,0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = th.vertices
    exp[:,0] += 1
    assert np.allclose(world, exp)


    th.state = [0,1,0, 0,0,0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = th.vertices
    exp[:,1] += 1
    assert np.allclose(world, exp)

    th.state = [0,0,1, 0,0,0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = th.vertices
    exp[:,2] += 1
    assert np.allclose(world, exp)    

    th.state = [1,1,1, 0,0,0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = th.vertices + 1
    assert np.allclose(world, exp, rtol=6)


def test_world_matrix_rotations():
    th = makeBoxThing()
    ang90 = np.pi/2

    th.state = [0,0,0, 0,0, ang90]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = np.array([
        [0, 0, 0 ,1],
        [0, 1, 0, 1],
        [-1, 0, 0, 1],
        [0, 0, 1, 1],
    ])
    assert np.allclose(world, exp, rtol=6)


    th.state = [0,0,0, 0,ang90, 0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = np.array([
        [0, 0, 0 ,1],
        [0, 0, -1, 1],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
    ])
    assert np.allclose(world, exp, rtol=6)


    th.state = [0,0,0, ang90, 0, 0]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = np.array([
        [0, 0, 0 ,1],
        [1, 0, 0, 1],
        [0, 0, -1, 1],
        [0, 1, 0, 1],
    ])
    assert np.allclose(world, exp, rtol=6)

def test_two_rotations():
    th = makeBoxThing()
    ang90 = np.pi/2

    th.state = [0,0,0, 0, ang90, ang90]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = np.array([
        [0, 0, 0 ,1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]) 
    print(world)
    print(exp)
    assert np.allclose(world, exp, rtol=6)



def test_rotate_and_translate():
    th = makeBoxThing()
    ang90 = np.pi/2

    th.state = [1,0,0, 0, 0, ang90]
    mat = th.getLocalToWorldMat()
    world = np.dot(th.vertices, mat)
    exp = np.array([
        [0, 0, 0 ,1],
        [0, 1, 0, 1],
        [-1, 0, 0, 1],
        [0, 0, 1, 1],
    ]) 
    exp[:,0] += 1
    assert np.allclose(world, exp, rtol=6)

def test_normals():
    th = makeBoxThing()

    norms = th.norms
    exp = np.array([
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0],
    ]) 

    assert np.allclose(norms, exp, rtol=6)


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