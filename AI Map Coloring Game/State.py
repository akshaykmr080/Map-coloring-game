class State():
    def __init__(self,name,adjacentStates=None,domain=None,colorAssigned=None,playerAssigned=None):
        #state name
        self.name = name
        
        #state domain
        self.domain = domain
        
        #colored assigned to the state
        self.colorAssigned = colorAssigned
        
        #player who assigned the color
        self.playerAssigned = playerAssigned
        
        #adjacent states for this state
        self.adjacentStates = adjacentStates
        
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name
    
    def getDomain(self):
        return self.domain
    
    def setDomain(self, domain):
        self.domain = domain
        
    def addToDomain(self,color):
        self.domain.append(color)
        
    def getPlayerAssigned(self):
        return self.playerAssigned
    
    def setPlayerAssigned(self,player):
        self.playerAssigned = player
        
    def removeFromDomain(self,color):
        self.domain.remove(color)
        
    def getColorAssigned(self):
        return self.colorAssigned
    
    def setColorAssigned(self,color):
        self.colorAssigned = color
        
    def setAdjacentStates(self, states):
        self.adjacentStates = states
        
    def getAdjacentStates(self):
        return self.adjacentStates
    
    def __eq__(self, other):
      myName = self.name
      hisName = other.getName()
      if myName == hisName:
        return True
      else:
        return False
    
        
    def __hash__(self):
        return hash(self.name)