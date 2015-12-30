__author__ = 'ykp'
from decimal import Decimal
import time
import os.path


playerAStartIndex = 0
playerBStartIndex = 0
playerAEndIndex = 0
playerBEndIndex = 0
playerAMancalaIndex = 0
playerBMancalaIndex = 0
mancalaBoard = []
maxMancalaIndex = 0
minMancalaIndex = 0
mancalaBoardLength = 0
cutOffDepth = 0
outputFileHandler = 0
nextStateFileHandler = 0
rootPlayer = ''
totalStones = 0
playerADict = {}
playerBDict = {}
startTime = 0
writtenOnce = False
detailsFileHandler =''
minimumCutOffTime = 0
startTimeForParticularDepth = 0
endTimeForParticularDepth = 0

Infinity = Decimal('Infinity')
NegInfinity = Decimal('-Infinity')

class BoardNode:

    def __init__(self):
        self.board = []
        self.depth = 0
        self.value = 0
        self.state = '' #A2,A3,A4 or B2,B3,B4 etc
        self.role ='' # MIN/MAX
        self.nextState = ''
        self.path = []
        self.status = ''
        self.player = ''
        self.alpha = ''
        self.beta = ''



def evaluate(board):

    totalUtility = 0


    # how far ahead am i from my opponent - the same function we used for the assignment
    if rootPlayer == "B":
        H1 =  board[playerBMancalaIndex]-board[playerAMancalaIndex]
    else:
        H1 = board[playerAMancalaIndex]-board[playerBMancalaIndex]

    # How close am i to winning
    # if a player has more than half of the total stones, he ois guaranteed to win, so using it to calculate this heuristic
    if rootPlayer == "B":
        half = totalStones/2
        H2 = totalStones - ((half+1) - board[playerBMancalaIndex])
    else:
        half = totalStones/2
        H2 = totalStones - ((half+1) - board[playerAMancalaIndex])

    # how close is opponent is to winning
    if rootPlayer == "B":
        half = totalStones/2
        H3 = (half+1) - board[playerAMancalaIndex]
    else:
        half = totalStones/2
        H3 = (half+1) - board[playerBMancalaIndex]

    return H1+H2+H3

def isGameOver(board):
    mBoard = list(board)
    gameOverA = True
    gameOverB = True
    gameOverObject = {}


    for x in range(0,(len(mBoard)/2)-1):
        if x != playerAMancalaIndex:
            if mBoard[x] != 0:
                gameOverA = False
                break

    for x in range((len(mBoard)/2),len(mBoard)-1):
        if x != playerBMancalaIndex:
            if mBoard[x] != 0:
                gameOverB = False
                break

    if gameOverA:
        sum = 0
        for x in range((len(mBoard)/2),len(mBoard)-1):

            if x != playerBMancalaIndex:
                sum += mBoard[x]
                mBoard[x] = 0
        mBoard[playerBMancalaIndex] += sum

    if gameOverB:
        sum = 0
        for x in range(0,(len(mBoard)/2)-1):

            if x != playerAMancalaIndex:
                sum += mBoard[x]
                mBoard[x] = 0
        mBoard[playerAMancalaIndex] += sum

    if gameOverA:
        gameOverObject["player"] = "A"
        gameOverObject["isGameOver"] = True
        gameOverObject["updatedBoard"] = mBoard
    elif gameOverB:
        gameOverObject["player"] = "B"
        gameOverObject["isGameOver"] = True
        gameOverObject["updatedBoard"] = mBoard
    elif gameOverA and gameOverB:
        gameOverObject["player"] = "both"
        gameOverObject["isGameOver"] = True
        gameOverObject["updatedBoard"] = mBoard
    else:
        gameOverObject["isGameOver"] = False



    return gameOverObject

def initializeDataStructures(boardConfiguration):

    global playerAMancalaIndex
    global playerBMancalaIndex
    global playerAStartIndex
    global playerAEndIndex
    global playerBStartIndex
    global playerBEndIndex
    global mancalaBoard
    global maxMancalaIndex
    global minMancalaIndex
    global mancalaBoardLength
    global totalStones
    global playerBDict
    global playerADict

    length = len(boardConfiguration["player2BoardConfiguration"]) - 1
    for element in boardConfiguration["player2BoardConfiguration"]:
        mancalaBoard.append(int(element))
        playerADict[length] = 0
        length -= 1
    mancalaBoard.reverse()


    mancalaBoard.append(boardConfiguration["player2MancalaCount"])

    playerAMancalaIndex = len(mancalaBoard)-1
    playerAStartIndex = playerAMancalaIndex - 1
    playerAEndIndex = 0
    minMancalaIndex = playerAMancalaIndex

    startIndex = playerAMancalaIndex+1
    for element in boardConfiguration["player1BoardConfiguration"]:
        mancalaBoard.append(int(element))
        playerBDict[startIndex] = 0
        startIndex+=1
    mancalaBoard.append(boardConfiguration["player1MancalaCount"])

    playerBMancalaIndex = len(mancalaBoard) - 1
    playerBStartIndex = playerAMancalaIndex + 1
    playerBEndIndex = playerBMancalaIndex - 1
    maxMancalaIndex = playerBMancalaIndex
    mancalaBoardLength = len(mancalaBoard)

    for x in mancalaBoard:
        totalStones += x

def getOppositeIndex(playerMancalaIndex,actualIndex):
    return (((playerMancalaIndex - actualIndex) * 2 ) + actualIndex) % mancalaBoardLength



def playAMancala(index,board,depth,alpha,beta):

    mBoard = list(board)
    node = BoardNode()
    node.depth = depth + 1
    node.state = 'A' + str(getOppositeIndex(playerAMancalaIndex,index) - (playerBEndIndex - playerBStartIndex))
    node.player = "B"
    node.alpha = alpha
    node.beta = beta

    if rootPlayer == "B":
        node.role = "max"
        node.value = NegInfinity

    else:
        node.role = "min"
        node.value = Infinity

    valueOfPitToBeEmptied = mBoard[index]
    node.path.append(node.state)
    mBoard[index] = 0

    if valueOfPitToBeEmptied == 0:
        return "empty"

    ind = index + 1
    while valueOfPitToBeEmptied > 0:
        if ind != playerBMancalaIndex:
            mBoard[ind] += 1
            valueOfPitToBeEmptied -= 1
            actualIndex = ind
            ind = (ind + 1) % mancalaBoardLength
        else:
            ind = (ind + 1) % mancalaBoardLength



    if playerAEndIndex <= actualIndex <= playerAStartIndex:
        if(mBoard[actualIndex] == 1):
            mBoard[playerAMancalaIndex] += 1
            mBoard[actualIndex] = 0
            oppositePitIndex = getOppositeIndex(playerAMancalaIndex,actualIndex)
            mBoard[playerAMancalaIndex] += mBoard[oppositePitIndex]
            mBoard[oppositePitIndex] = 0

    node.board = mBoard
    gameOverObject = isGameOver(node.board)

    if gameOverObject["isGameOver"]:
        node.board = gameOverObject["updatedBoard"]
        node.status = "gameover"
        node.value = evaluate(node.board)
        return node

    if actualIndex == playerAMancalaIndex:
            node.status = "hasbonusmove"
            node.board = mBoard
            node.player = "A"
            if rootPlayer == "B":
                node.value = Infinity
                node.role = "min"
            else:
                node.value = NegInfinity
                node.role = "max"
            return node

    return node

def playBMancala(index,board,depth,alpha,beta):
    mBoard = list(board)
    node = BoardNode()
    node.depth = depth + 1
    node.state = 'B' + str(index - (playerBEndIndex - playerBStartIndex))
    node.player = "A"
    node.alpha = alpha
    node.beta = beta

    if rootPlayer == "B":
        node.role = "min"
        node.value = Infinity
    else:
        node.role = "max"
        node.value = NegInfinity


    valueOfPitToBeEmptied = mBoard[index]
    node.path.append(node.state)
    mBoard[index] = 0
    if valueOfPitToBeEmptied == 0:
        return "empty"
    ind = index + 1
    while valueOfPitToBeEmptied > 0:
        if ind != playerAMancalaIndex:
            mBoard[ind] += 1
            valueOfPitToBeEmptied -= 1
            actualIndex = ind
            ind = (ind + 1) % mancalaBoardLength
        else:
            ind = (ind + 1) % mancalaBoardLength


    if playerBStartIndex <= actualIndex <= playerBEndIndex:
        if(mBoard[actualIndex] == 1):
            mBoard[playerBMancalaIndex] += 1
            mBoard[actualIndex] = 0
            oppositePitIndex = (((playerBMancalaIndex - actualIndex) * 2 ) + actualIndex) % mancalaBoardLength
            mBoard[playerBMancalaIndex] += mBoard[oppositePitIndex]
            mBoard[oppositePitIndex] = 0

    node.board = mBoard
    gameOverObject = isGameOver(node.board)

    if gameOverObject["isGameOver"]:
        node.board = gameOverObject["updatedBoard"]
        node.status = "gameover"
        node.value = evaluate(node.board)
        return node

    if actualIndex == playerBMancalaIndex:
        node.status = "hasbonusmove"
        node.board = mBoard
        node.player = "B"
        if rootPlayer == "B":
            node.role = "max"
            node.value = NegInfinity
        else:
            node.role = "min"
            node.value = Infinity
        return node

    return node


def getNextState(node):
    currentTime = time.time()
    global cutOffDepth
    if currentTime - startTime >= minimumCutOffTime and writtenOnce == True:
        exit()

    elif currentTime - startTime >= 35:
        printNextState(node,True,time.time()-startTimeForParticularDepth)

    if node.status == "hasbonusmove":
        if node.player == "A":
            for key,value in sorted(playerADict.iteritems(),  key=lambda (k,v): (v,k),reverse=True):
                index = key
                nextNode = playAMancala(index,node.board,node.depth,node.alpha,node.beta)
                if nextNode != "empty":
                    nextNode.depth -= 1
                    if nextNode.status == "gameover":
                        if nextNode.role == "max":
                            if nextNode.value > nextNode.alpha:
                                nextNode.alpha = nextNode.value
                        elif nextNode.role == "min":
                            if nextNode.value < nextNode.beta:
                                nextNode.beta = nextNode.value
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    #elif nextNode.depth < cutOffDepth or nextNode.status=="hasbonusmove":
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        willBePruned = False
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevAlpha = node.alpha
                            if node.value > node.alpha:
                                node.alpha = node.value
                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value >= node.beta:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            playerADict[key] = pow(2,node.depth)
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(prevAlpha)+','+str(node.beta)+'\n')
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
                    else:
                        willBePruned = False
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevBeta = node.beta
                            if node.value < node.beta:
                                node.beta = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value <= node.alpha:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(prevBeta)+'\n')
                            playerADict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
                index -= 1
        else:
            for key,value in sorted(playerBDict.iteritems(),  key=lambda (k,v): (v,k),reverse=True):
                index = key
                nextNode = playBMancala(index,node.board,node.depth,node.alpha,node.beta)
                if nextNode != "empty":
                    nextNode.depth -= 1
                    if nextNode.status == "gameover":
                        if nextNode.role == "max":
                            if nextNode.value > nextNode.alpha:
                                nextNode.alpha = nextNode.value
                        elif nextNode.role == "min":
                            if nextNode.value < nextNode.beta:
                                nextNode.beta = nextNode.value
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    #elif nextNode.depth < cutOffDepth or nextNode.status=="hasbonusmove":
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        willBePruned = False
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevAlpha = node.alpha
                            if node.value > node.alpha:
                                node.alpha = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value >= node.beta:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(prevAlpha)+','+str(node.beta)+'\n')
                            playerBDict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
                    else:
                        willBePruned = False
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevBeta = node.beta
                            if node.value < node.beta:
                                node.beta = node.value
                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value <= node.alpha:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(prevBeta)+'\n')
                            playerBDict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
                index += 1

    elif node.depth >=cutOffDepth:
        node.value = evaluate(node.board)
        # if node.status != "gameover":
        #     outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
        return node

    else:
        if node.player == "B":
            # its a max node, so iterate correspondingly
            for key,value in sorted(playerBDict.iteritems(),  key=lambda (k,v): (v,k),reverse=True):
                index = key
                nextNode = playBMancala(index,node.board,node.depth,node.alpha,node.beta)
                if nextNode != "empty":
                    if nextNode.status == "gameover":
                        if nextNode.role == "max":
                            if nextNode.value > nextNode.alpha:
                                nextNode.alpha = nextNode.value
                        elif nextNode.role == "min":
                            if nextNode.value < nextNode.beta:
                                nextNode.beta = nextNode.value
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    #elif nextNode.depth < cutOffDepth or nextNode.status == "hasbonusmove":
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        willBePruned = False
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevAlpha = node.alpha
                            if node.value > node.alpha:
                                node.alpha = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value >= node.beta:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(prevAlpha)+','+str(node.beta)+'\n')
                            playerBDict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')


                    else:
                        willBePruned = False
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevBeta = node.beta
                            if node.value < node.beta:
                                node.beta = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value <= node.alpha:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(prevBeta)+'\n')
                            playerBDict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')


                index += 1

        else:
            for key,value in sorted(playerADict.iteritems(),  key=lambda (k,v): (v,k),reverse=True):
                index = key
                nextNode = playAMancala(index,node.board,node.depth,node.alpha,node.beta)
                if nextNode != "empty":
                    if nextNode.status == "gameover":
                        if nextNode.role == "max":
                            if nextNode.value > nextNode.alpha:
                                nextNode.alpha = nextNode.value
                        elif nextNode.role == "min":
                            if nextNode.value < nextNode.beta:
                                nextNode.beta = nextNode.value
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    #elif nextNode.depth < cutOffDepth or nextNode.status == "hasbonusmove":
                        #outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+','+str(nextNode.alpha)+','+str(nextNode.beta)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        willBePruned = False
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevAlpha = node.alpha
                            if node.value > node.alpha:
                                node.alpha = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value >= node.beta:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(prevAlpha)+','+str(node.beta)+'\n')
                            playerADict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')


                    else:
                        willBePruned = False
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            prevBeta = node.beta
                            if node.value < node.beta:
                                node.beta = node.value

                            if node.alpha != NegInfinity and node.beta != Infinity:
                                if node.value <= node.alpha:
                                    willBePruned = True
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                        if willBePruned:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(prevBeta)+'\n')
                            playerADict[key] = pow(2,node.depth)
                            break
                        #else:
                            #outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+','+str(node.alpha)+','+str(node.beta)+'\n')
                index -= 1

    node.path.insert(0,node.state)
    return node

def printDataStructures():
    print "Mancala Board: ",mancalaBoard
    print "playerAStartIndex: ",playerAStartIndex
    print "playerBStartIndex: ",playerBStartIndex
    print "playerAEndIndex: ",playerAEndIndex
    print "playerBEndIndex: ",playerBEndIndex
    print "playerAMancalaIndex: ",playerAMancalaIndex
    print "playerBMancalaIndex: ",playerBMancalaIndex

def printNextState(nextState,terminate,period):
    global writtenOnce
    global nextStateFileHandler
    global detailsFileHandler
    global cutOffDepth
    nextStateFileHandler = open('output.txt','w')
    detailsFileHandler = open('details.txt','w')
    if writtenOnce == False:
        writtenOnce = True

    path = nextState.path
    firstVal = ''
    foundnonroot = False
    for x in range(0,len(path)):
        currentVal = path[x]
        if currentVal != "root":
            if not foundnonroot:
                firstVal = currentVal[:1]
                nextStateFileHandler.write(currentVal+'\n')
                nextStateFileHandler.flush()
                foundnonroot = True
            else:
                if currentVal[:1] == firstVal[:1]:
                    nextStateFileHandler.write(currentVal+'\n')
                    nextStateFileHandler.flush()
                else:
                    break

    detailsFileHandler.write(str(cutOffDepth)+'\n')
    detailsFileHandler.write(str(period))
    print "time of execution",time.time()-startTime
    nextStateFileHandler.close()
    detailsFileHandler.close()
    if terminate:
        exit()

def competition(boardConfiguration,start_time):
    initializeDataStructures(boardConfiguration)

    global cutOffDepth
    global rootPlayer
    global startTime
    global minimumCutOffTime
    global startTimeForParticularDepth
    global endTimeForParticularDepth

    startTime = start_time

    if os.path.isfile('details.txt'):
        counter = 1
        localDetailsFileHandler = open('details.txt','r')
        while True:
            line = localDetailsFileHandler.readline()
            line = line.rstrip()
            if line == '':
                break
            if counter == 1:
                cutOffDepth = int(line)
            elif counter == 2:
                minimumCutOffTime = float(line)
            counter += 1
    else:
        cutOffDepth = 7
        minimumCutOffTime = 9
    remainingTime = boardConfiguration["cutoffDepth"]

    print "minimumCutOffTime is : ",minimumCutOffTime
    root = BoardNode()
    root.role = "max"
    root.state = "root"
    if (boardConfiguration["playerRole"]== 1):
        root.player = "B"
        rootPlayer = "B"
    else:
        root.player = "A"
        rootPlayer = "A"
    root.depth = 0
    root.value = NegInfinity
    root.board = mancalaBoard
    root.path.append("root")
    root.alpha = NegInfinity
    root.beta = Infinity

    pathSoFar = ''
    similarityCounter = 0
    startTimeForParticularDepth = start_time
    while True:
        nextState = getNextState(root)
        endTimeForParticularDepth = time.time()
        printNextState(nextState,False,endTimeForParticularDepth-startTimeForParticularDepth)
        startTimeForParticularDepth = endTimeForParticularDepth
        cutOffDepth += 1
        path = nextState.path
        pathValue = ''
        for x in range(1,len(path)):
            currentVal = path[x]
            if currentVal != "root":
                if x == 1:
                    firstVal = currentVal[:1]
                    pathValue += currentVal
                else:
                    if currentVal[:1] == firstVal[:1]:
                        pathValue+=currentVal
                    else:
                        break
        if pathSoFar == pathValue:
            similarityCounter += 1
        else:
            pathSoFar=pathValue
            similarityCounter = 0

        if similarityCounter == 3:
            exit()
        print nextState.nextState
        print root.path

    print "time of execution: ",time.time()-startTime

    #outputFileHandler.write('Node'+','+'Depth'+','+ 'Value'+','+'Alpha'+','+'Beta'+'\n')
    #outputFileHandler.write(str(root.state)+','+str(root.depth)+','+ str(root.value)+','+str(root.alpha)+','+str(root.beta)+'\n')
    # nextState = getNextState(root)
    # printNextState(nextState)
