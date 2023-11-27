class Bbox:
    """A utility class for representing bounding boxes in two dimensions
    """

    def __init__(self, hoffset, woffset, height, width):
        """
        Inputs
        -----------
        * hoffset, woffset
            * Offset of the bottom left hand corner of the bounding box from
            the origin of the coordinate system 

        * height, width
            * Height and width of the bounding box in the units of the space's 
            coordinate system
        """
        self.hoffset = hoffset 
        self.woffset = woffset 
        self.height = height 
        self.width = width 

    @classmethod
    def from_coords(col1, col2, row1, row2):
        """
        Alternative way of creating a bounding box from coords of the corners

        Inputs
        --------
        * col1, col2
            * Column coordinates of extreme left and right of the box 
        * row1, row2
            * Row coordinates of the extreme bottom and top of the box 
        """
        hoffset = col1 
        woffset = row1
        height = row2 - row1 
        width = col2 - col1 
        return Bbox(hoffset, woffset, height, width)

    def get_coords(self):
        """Get the box boundaries 

        Returns 
        ---------
        `[left, right, bottom, top]`
        """

        c1 = self.hoffset 
        r1 = self.woffset 
        c2 = c1 + self.width 
        r2 = r1 + self.height 
        return c1, c2, r1, r2
    
    @property 
    def area(self):
        return self.height * self.width 

