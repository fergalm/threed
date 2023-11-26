
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import transforms as tf
import numpy as np 



"""
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
"""

class AmbientLightShader:
    def shade(self, th, pix_coords, normals, idx):
        return th.colours[idx]
    


"""
This is a sketch of a source and shader implementation. The idea is that
you can write 

```
shade = .5 * Ambient() + .25 * InfinitePointSource(vec1) + .25 * LocalPointSource(vec)
clr = shade.shade(th, pix_coords, normals, idx)
```

Ideally each light source could have a colour as well as a brightness


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
"""