
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
