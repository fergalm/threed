
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