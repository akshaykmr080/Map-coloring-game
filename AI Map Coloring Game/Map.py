import os
import Player
import State
import Map
import copy
import math
import sys

depthAllowed = None
def readFile(fileName,mode):
    #read the initial lines and parse it
    colors = []
    initialStates = []
    player1 = Player.Player("max","player1")
    player2 = Player.Player("min","player2")
    mapAus = None
    mapDict = {}
    i = 0
    depth = None
    
    #hold the states assigned to each player
    playerToState = {player1.name : [] , player2.name : []}
    
    with open(fileName, mode) as f:
        for line in f:
            #read the first line
            if(i==0):
                colors = line.split(",")
            elif(i==1):
                #read the second line
                initialStates = line.split(",")
                states = []
                for data in initialStates:
                    tempData = data.split(":")
                    state = State.State(tempData[0].strip())
                    colorAndPlayer = tempData[1].split("-")
                    state.setColorAssigned(colorAndPlayer[0].strip())
                    
                    #update player and states
                    if(int(colorAndPlayer[1]) == 1):
                        player1.updateStatesAssignedAndTotalValueGained(state,colorAndPlayer[0].strip())
                        state.setPlayerAssigned(player1)
                        playerToState[player1.name.strip()].append(state)
                    elif(int(colorAndPlayer[1]) == 2):
                        player2.updateStatesAssignedAndTotalValueGained(state,colorAndPlayer[0].strip())
                        state.setPlayerAssigned(player2)
                        playerToState[player2.name.strip()].append(state)
                        
                        ####IMPORTANT : store the previous state colored and the color assigned in a map for future reference ###
                        mapDict['state'] = state
                        mapDict['colorAssigned'] = colorAndPlayer[0].strip()
                    states.append(state);
                
                #store the initial player objects   
                gamePlayers = [player1,player2]
                #create the initial map
                mapAus = Map.Map(playerToState,gamePlayers)
                for state in states:
                    #add all the states to the map (both colored and uncolored)
                    mapAus.addStates(state)
            elif(i==2):
                #store the depth
                depth = line
            elif(i==3):
                #store the color pref for each player
                colorAndValueDict = {}
                colorAndValueData = line.split(",")
                for data in colorAndValueData:
                    colorAndValueDict[data.split(":")[0].strip()] = data.split(":")[1].strip()
                mapAus.getPlayers()[0].setColorPref(colorAndValueDict)
                
            elif(i == 4):
                colorAndValueDict = {}
                colorAndValueData = line.split(",")
                for data in colorAndValueData:
                    colorAndValueDict[data.split(":")[0].strip()] = data.split(":")[1].strip()
                    
                mapAus.getPlayers()[1].setColorPref(colorAndValueDict)
            
            else :
                #parse the states and set up the adjacent states and domain colors for each state
                stateAndAdjacent = line.split(":")
                adjacentStates = stateAndAdjacent[1].split(",")
                
                adjacentStates = [x.strip('\n') for x in adjacentStates]
                adjacentStates = [x.strip(' ') for x in adjacentStates]
                addedStates = mapAus.getStates()
                exists = False
                domain = copy.deepcopy(colors)
                domain = [x.strip('\n') for x in domain]
                domain = [x.strip(' ') for x in domain]
                #check if state is already added to the map. if not, add it to the map
                for state in addedStates:
                    if(state.getName().strip(' ') == stateAndAdjacent[0].strip(' ')):
                        exists = True
                        state.setAdjacentStates(adjacentStates)
                if(exists == False):
                    for state in adjacentStates:
                        for added in addedStates :
                            if(state == added.getName() and added.getColorAssigned() != None and 		added.getColorAssigned().strip(' ') in domain):
                                domain.remove(added.getColorAssigned().strip(' '))
                                

                    newState = State.State(stateAndAdjacent[0],adjacentStates,domain)
                    mapAus.addStates(newState)
            i = i+1
    ###IMPORTANT : add the map object to the dictionary for future reference#####
    mapDict['map'] = mapAus
    alphabeta_full_search(mapDict,depth.strip())                 
                    
def alphabeta_full_search(mapInAlphaBeta,depth):
    """Search game to determine best action; use alpha-beta pruning."""

    def max_value(mapInMax, alpha, beta, depthInMax,depth):
        v = -float('inf')
        stateColoredInMax = None
        colorAssignedInMax = None
        stringToWrite = None
        #check for terminal test or if the depth has been exceeded. if true, return the value of the map. 
        if mapInMax['map'].terminalStateTest() or int(depthInMax) >= int(depth):
            mapInMax['map'].updateMapValue()
            stringToWrite = mapInMax['state'].getName() +", "+mapInMax['colorAssigned']+", "+str(depthInMax)+", "+str(mapInMax['map'].getMapValue())+", "+str(alpha)+", "+str(beta)+"\n"
            #print(stringToWrite)
            f.write(stringToWrite)
            return mapInMax['map'].getMapValue(),mapInMax['state'].getName() ,mapInMax['colorAssigned']
        else :
            stringToWrite = mapInMax['state'].getName()+", "+mapInMax['colorAssigned']+", "+str(depthInMax)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
            #print(stringToWrite)
            f.write(stringToWrite)
        
        #get all the successor states of the map. 
        for mapData in getSuccessors(mapInMax,"player1"):
            
            #get the value, state and colorAssigned from min player
            value,stateColoredFromMin,colorAssignedFromMin = min_value(mapData, alpha, beta, int(depthInMax)+1,depth)
            #perform alpha beta pruning
            if(v < value):
              stateColoredInMax = mapData['state'].getName()
              colorAssignedInMax = mapData['colorAssigned']
              v = value
              
            if v >= beta:
                stringToWrite = mapInMax['state'].getName() +", "+mapInMax['colorAssigned']+", "+str(depthInMax)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
                #print(stringToWrite)
                f.write(stringToWrite)
                return v,stateColoredInMax,colorAssignedInMax
            alpha = max(alpha, v)
            stringToWrite = mapInMax['state'].getName() +", "+mapInMax['colorAssigned']+", "+str(depthInMax)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
            #print(stringToWrite)
            f.write(stringToWrite)
        #return the value, best state obtained and the color assigned
        return v,stateColoredInMax,colorAssignedInMax

    def min_value(mapInMin, alpha, beta, depthInMin,depth):
        
        v = float('inf')
        stateColoredInMin = None
        colorAssignedInMin = None
        #check for terminal test or if the depth has been exceeded. if true, return the value of the map.
        if mapInMin['map'].terminalStateTest() or int(depthInMin) >= int(depth):
             mapInMin['map'].updateMapValue()
             stringToWrite = mapInMin['state'].getName() +", "+mapInMin['colorAssigned']+", "+str(depthInMin)+", "+str(mapInMin['map'].getMapValue())+", "+str(alpha)+", "+str(beta)+"\n"
             #print(stringToWrite)
             f.write(stringToWrite)
             return mapInMin['map'].getMapValue(),mapInMin['state'].getName(),mapInMin['colorAssigned']
        else :
            stringToWrite = mapInMin['state'].getName() +", "+mapInMin['colorAssigned']+", "+str(depthInMin)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
            #print(stringToWrite)
            f.write(stringToWrite)
         
        #get all the successor states of the map
        for mapData in getSuccessors(mapInMin,"player2"):
          
            #get the value, state and colorAssigned from min player
            valueInMin,stateFromMax,colorFromMax = max_value(mapData, alpha, beta, depthInMin+1,depth)
            #perform alpha beta pruning
            if(v > valueInMin):
              stateColoredInMin = mapData['state'].getName()
              colorAssignedInMin = mapData['colorAssigned']
              v = valueInMin
            #v = min(v, valueInMin)
            if v <= alpha:
                stringToWrite = mapInMin['state'].getName()+", "+mapInMin['colorAssigned']+", "+str(depthInMin)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
                #print(stringToWrite)
                f.write(stringToWrite)
                return v,stateColoredInMin,colorAssignedInMin
            beta = min(beta, v)
            stringToWrite = mapInMin['state'].getName()+", "+mapInMin['colorAssigned']+", "+str(depthInMin)+", "+str(v)+", "+str(alpha)+", "+str(beta)+"\n"
            #print(stringToWrite)
            f.write(stringToWrite)
        #return the value, best state obtained and the color assigned
        return v,stateColoredInMin,colorAssignedInMin

    # Body of alphabeta_search starts here:
    valueToPrint,StateToGo,ColorToAssign = max_value(mapInAlphaBeta,-float('inf'),float('inf'),0,depth)
    stringData = StateToGo+", "+ColorToAssign+", "+str(valueToPrint)
    f.write(stringData)
   
                 
def getSuccessors(mapD,playerName):
    playerTostate = mapD['map'].getPlayerToState()
    player1States = playerTostate["player1"]
    player2States = playerTostate["player2"]
    AllStates = mapD['map'].getStates()
  
    mapList = []
    #list the states which are allready occupied
    occupiedStates = list(set(player1States) | set(player2States))
    #get all adjacent states of colored states
    adjacentStateSet = set()
    
    #remove occupied states from all states and set it as adjacent states      
    for eachState in occupiedStates:
      for eachAllState in AllStates:
        if(eachState.getName()  == eachAllState.getName()):
          adjacentStateSet = adjacentStateSet.union(eachAllState.getAdjacentStates())
          
    adjacentStateSet = adjacentStateSet - set([x.getName() for x in occupiedStates])
    newStateList = []
    for x in AllStates:
      if(x.getName() in adjacentStateSet):
        newStateList.append(x)
    #sort the adjacent states which can be colored    
    newStateList = sorted(newStateList, key=lambda x: x.getName())
    
    #for each state, create a new copy of the map. color the state in that map and add it to the list of successors
    for eachState in newStateList:
        player = None
        newMapList = None
        domainColors = eachState.getDomain()
        for domainC in sorted(domainColors):
          
                #make a copy of the state
                nextState = copy.deepcopy(eachState)
                
                #make a new copy of the map
                newMap = copy.deepcopy(mapD['map'])
                nextState.setColorAssigned(domainC)
                #get the players and update the states colored by them                
                players = newMap.getPlayers()
                for eachPlayer in players:
                    if(eachPlayer.getName() == playerName):
                        eachPlayer.updateStatesAssignedAndTotalValueGained(nextState,domainC)
                        
                        
                #update the adjacent states in the new map       
                for eachStateTrace in newMap.getStates():
                    if(eachStateTrace.getName() == nextState.getName()):
                        nextState.setAdjacentStates(eachStateTrace.getAdjacentStates())
                newMap.setPlayerToState(playerName,nextState)
                
                adjStates = nextState.getAdjacentStates()
                stateList = newMap.getStates()
                
                emptyStateList = list()
                #update the domain colors of the adjacent states
                for eachStateData in stateList:
                    if(eachStateData.getColorAssigned() == None):
                        if(eachStateData.getName() in adjStates):
                            domainColors = eachStateData.getDomain()
                            if(domainC in domainColors):
                              domainColors.remove(domainC)
                              
                            if(len(domainColors) == 0):
                              emptyStateList.append(eachStateData)
              
                              
                for removeStateData in emptyStateList:
                  newMap.getStates().remove(removeStateData)
                        
                newMap.getStates().remove(nextState)
                newMap.getStates().add(nextState)
                dataToReturn = {}
                
                ######IMPORTANT : create a dictionary which hold the map object and the state which was colored in that map and the color assigned to it#####
                
                dataToReturn['map'] = newMap
                dataToReturn['state'] = nextState
                dataToReturn['colorAssigned'] = domainC
                mapList.append(dataToReturn)
                
    #mapList - list of dictinaries            
    return (mapList)   

        
        
f= open("output.txt", "w")
readFile(sys.argv[2],"r")