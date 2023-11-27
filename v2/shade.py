
from ipdb import set_trace as idebug

from . import transforms as tf


__doc__ = """
A Shader decides how bright a facet should be based on its location,
orientation, distance from the camera, etc. 

This module is a stub, and needs work. 

Things I might want to shade on

* Ambient light 
* Illumination from
    * Single source at infinite distance
    * Single source at finite distance 
    * Multiple sources
    * Take shadows into account. 
        * For each polygon/light source pair
        * Calculate if any other object blocks the light.
        * This might get expensive
    * Haze (objects further away should be greyer


This is a sketch of a source and shader implementation. The idea is that
you can write 

```
shade = .5 * Ambient() + .25 * InfinitePointSource(vec1) + .25 * LocalPointSource(vec)
clr = shade.shade(th, pix_coords, normals, idx)
```

Ideally each light source could have a colour as well as a brightness

```
class Source:
    def __init__(self):
        self.strenght = 1 

    def shade(self, th, pix_coords, normals, idx):
        return #a 1d array of floats between 0 and 1

    def __mul__(self, frac):
        self.strength = frac 

    def __rmul__(self, frac):
        self.strength = frac 

    def __add__(self, obj):
        return Shader(self, obj)

class Shader:
    def __add__(self, obj):
        if isinstance(obj, Source):
            slist = self.source_list + [obj]
            
            return Shader(slist)
        
        elif isinstance(obj, Shader):
            slist = self.source_list + obj.source_list
            return Shader(slist) 
        else:
            raise TypeError 
        
    def paint(self, th, pix_coords, normals, idx):
        brightness = np.ones(np.sum(idx))
        for s in self.source_list:
            brightness *= s.shade(th, pix_coords, normals, idx)
        
        clrs = th.colours[idx].copy()
        clrs *= brightness
```
"""

from .thing import Thing 
import numpy as np 

class AbstractShader:
    def shade(self, th:Thing, pix_coords:np.ndarray, normals:np.ndarray, idx:np.ndarray):
        """
        Compute shade for each facet in the thing. 

        Inputs
        ----------
        `n` is the number of vertices in a thing, and `m` is the number of facets 

        * th
            * The thing to shade 
        * pix_coords
            * An `n x 3` numpy array of coordinates of the vertices in pixel space 
        * normals 
            * An `m x 3` numpy array of the normal vectors of the facets of the Thing 
        * idx 
            * A 1d boolean numpy array of length `m`. Shades are only computed for
            facet[j] if idx[j] is True 

        Returns 
        ------------
        A 1d numpy array of colours of facets. The length of the return array 
        is equal to the number of true values of `idx`
        """


class AmbientLightShader(AbstractShader):
    """A completely diffuse lightsource that illuminates equally in all directions.

    Similar to the light you get on a misty day, except that you can see forever
    """

    def shade(self, th, pix_coords, normals, idx):
        return th.colours[idx]
    


