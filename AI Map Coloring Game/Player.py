class Player():
    
    def __init__(self,typeData,name, colorPref=None,statesAssigned=None, totalValueGained=0):
        #hols max or min
        self.typeData = typeData 
        
        #name of the player
        self.name = name
        
        #states colored by the player so far
        self.statesAssigned = []
        
        #players color preference
        self.colorPref = {}
        
        #total value gained by the player so far
        self.totalValueGained = totalValueGained
        
    #to check if 2 instances of player objects are equal or not
    def __eq__(self, other):
      myName = self.name
      hisName = other.name
      if myName == hisName:
        return True
      else:
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    #assign state to the player and update the totalValue gained    
    def updateStatesAssignedAndTotalValueGained(self,state,colorAssigned):
        
        #"""update states assigned"""
        self.statesAssigned.append(state)
        
        #"""update total value gained"""
        for key,value in self.colorPref.items():
            
            if(key == colorAssigned):
                self.totalValueGained += int(value)
                
    def getPlayerType(self):
        return self.typeData
    
    def setPlayerType(self,typeData):
        self.typeData = typeData
        
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name
    
    def getColorPref(self):
        return self.colorPref
    
    def setColorPref(self,colorPref):
        self.colorPref = colorPref
        
    def getStatesAssigned(self):
        return self.statesAssigned
    
    def getTotalValueGained(self):
        return self.totalValueGained
        