
   
1. Draw Apollo service module, TIE fight winger
1. Render Scene, not just a single object
1. Camera can 
    1. track (yes)
    1. tilt
    1. pan
    1. roll
1. Culling of facets that don't need to be plotted
    1. Off screen
    3. Hidden by other facets 
    2. Pointing away from camera
        1. Still useful to do this even if doing step 3?
    
5. Lightsources


### Keyboard control
wasd  dolly forward back, truck left right, 
WS pedestal up down

Arrows for tilt and pan. Shift [<-], [->] to roll 

Of course, all of these have to be relative to current orientation!

[z], [x] zoom out/in (adjust camera platescale)

### Multiple scenes 

```
renderScene(scene)

    for obj in scene
        pixels = self.bboxForObj(obj)
        
        if isInFrame(bbox):
            pixels = self.pixelsForObj(obj)
            facets = obj.getFacets()
            
            facetList.extend(pixels[facets])
            zdist.extend( .. somehow get zdist ...)
            propList.extent(obj.facetProperties???)

    srt = np.argsort(zdist)[::-1]
    facetList = pixelList[srt]
    propList = propList[srt]
    
    #Culling of facets goes here
    
    for i in rangel(len(facetList):
        plotFacet(facetList[i], propList[i])
            
```

#### Culling 
For a subsequent version.
*
* Create a bounding box for each facet in pixel space
* starting with the most distant object, 
    * Create intersection with edge of screen
    * find all closer objects whose bboxes overlap
    * Create union of those objects
    * If union.contains(facet)
        * remove
