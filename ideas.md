
1. New Repo  
2. New classes
3. Split off render from transformer
1. Camera can move, tilt, pan, roll
1. Render Scene, not just a single object
1. Culling of facets that don't need to be plotted
    1. Off screen
    2. Pointing away from camera
    3. Hidden by other facets (does this make 2 unecessary?)
4. Draw Apollo service module, TIE fight winger
5. Lightsources


My idea for rendering multiple scenes 
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
    
    for i in rangel(len(facetList):
        plotFacet(facetList[i], propList[i])
            
```

For a subsequent version.
* 
* Create a bounding box for each facet in pixel space
* starting with the most distant object, 
    * Create intersection with edge of screen
    * find all closer objects whose bboxes overlap
    * Create union of those objects
    * Create intersection_complement(obj, union) 
    * Render that complement
