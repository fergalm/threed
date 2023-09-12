
class Element():
    def __init__(self, pos, attitude):
        self.pos = pos 
        self.attitude = attitude 

    #TODO: Do away with getters and setters?
    def getPosition(self):
        return self.pos 

    def getAttitude_rad(self):
        return self.attitude

    def setAttitude_rad(self, ang):
        self.attitude = ang

    def move(self, timestep):
        # Moving the camera by function not implemented yet
        pass 

