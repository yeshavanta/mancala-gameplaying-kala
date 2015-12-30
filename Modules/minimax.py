__author__ = 'ykp'
from decimal import Decimal


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
outputFileHandler = open('traverse_log.txt','w')
nextStateFileHandler = open('next_state.txt','w')
rootPlayer = ''

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



def evaluate(board):

    if rootPlayer == "B":
        return board[playerBMancalaIndex]-board[playerAMancalaIndex]
    else:
        return board[playerAMancalaIndex]-board[playerBMancalaIndex]

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
    global cutOffDepth


    cutOffDepth = boardConfiguration["cutoffDepth"]
    for element in boardConfiguration["player2BoardConfiguration"]:
        mancalaBoard.append(int(element))
    mancalaBoard.reverse()
    mancalaBoard.append(boardConfiguration["player2MancalaCount"])

    playerAMancalaIndex = len(mancalaBoard)-1
    playerAStartIndex = playerAMancalaIndex - 1
    playerAEndIndex = 0
    minMancalaIndex = playerAMancalaIndex

    for element in boardConfiguration["player1BoardConfiguration"]:
        mancalaBoard.append(int(element))
    mancalaBoard.append(boardConfiguration["player1MancalaCount"])

    playerBMancalaIndex = len(mancalaBoard) - 1
    playerBStartIndex = playerAMancalaIndex + 1
    playerBEndIndex = playerBMancalaIndex - 1
    maxMancalaIndex = playerBMancalaIndex
    mancalaBoardLength = len(mancalaBoard)

def getOppositeIndex(playerMancalaIndex,actualIndex):
    return (((playerMancalaIndex - actualIndex) * 2 ) + actualIndex) % mancalaBoardLength



def playAMancala(index,board,depth):

    mBoard = list(board)
    node = BoardNode()
    node.depth = depth + 1
    node.state = 'A' + str(getOppositeIndex(playerAMancalaIndex,index) - (playerBEndIndex - playerBStartIndex))
    node.player = "B"

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

def playBMancala(index,board,depth):
    mBoard = list(board)
    node = BoardNode()
    node.depth = depth + 1
    node.state = 'B' + str(index - (playerBEndIndex - playerBStartIndex))
    node.player = "A"
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

    if node.status == "hasbonusmove":
        if node.player == "A":
            index = playerAStartIndex
            while index >= playerAEndIndex:
                nextNode = playAMancala(index,node.board,node.depth)
                if nextNode != "empty":
                    nextNode.depth -= 1
                    if nextNode.status == "gameover":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    elif nextNode.depth < cutOffDepth or nextNode.status=="hasbonusmove":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                    else:
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                index -= 1
        else:
            index = playerBStartIndex
            while index <= playerBEndIndex:
                nextNode = playBMancala(index,node.board,node.depth)
                if nextNode != "empty":
                    nextNode.depth -= 1
                    if nextNode.status == "gameover":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    elif nextNode.depth < cutOffDepth or nextNode.status=="hasbonusmove":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                    else:
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                index += 1

    elif node.depth >=cutOffDepth:
        node.value = evaluate(node.board)
        if node.status != "gameover":
            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
        return node

    else:
        if node.player == "B":
            # its a max node, so iterate correspondingly
            index = playerBStartIndex
            while index <= playerBEndIndex:
                nextNode = playBMancala(index,node.board,node.depth)
                if nextNode != "empty":
                    if nextNode.status == "gameover":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    elif nextNode.depth < cutOffDepth or nextNode.status == "hasbonusmove":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')

                    getNextState(nextNode)
                    if node.role == "max":
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                    else:
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                index += 1

        else:
            index = playerAStartIndex
            while index >= playerAEndIndex:
                nextNode = playAMancala(index,node.board,node.depth)
                if nextNode != "empty":
                    if nextNode.status == "gameover":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    elif nextNode.depth < cutOffDepth or nextNode.status == "hasbonusmove":
                        outputFileHandler.write(str(nextNode.state)+','+str(nextNode.depth)+','+ str(nextNode.value)+'\n')
                    getNextState(nextNode)
                    if node.role == "max":
                        if( node.value < nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                    else:
                        if( node.value > nextNode.value):
                            node.value = nextNode.value
                            node.path = nextNode.path
                            if nextNode.status == "hasbonusmove":
                                node.nextState = nextNode.nextState
                            else:
                                node.nextState = nextNode.board
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')
                        else:
                            outputFileHandler.write(str(node.state)+','+str(node.depth)+','+ str(node.value)+'\n')

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

def printNextState(nextState):
    board = nextState.nextState
    index = playerAStartIndex
    playerABoardString = ''
    playerBBoardString = ''


    while index >= playerAEndIndex:
        if index == playerAEndIndex:
            playerABoardString += (str(board[index])+'\n')
        else:
            playerABoardString += (str(board[index])+' ')
        index -= 1

    nextStateFileHandler.write(playerABoardString)
    index = playerBStartIndex
    while index <= playerBEndIndex:
        if index == playerBEndIndex:
            playerBBoardString += (str(board[index])+'\n')
        else:
            playerBBoardString += (str(board[index])+' ')
        index += 1

    nextStateFileHandler.write(playerBBoardString)
    nextStateFileHandler.write((str(board[playerAMancalaIndex])+'\n'))
    nextStateFileHandler.write((str(board[playerBMancalaIndex])+'\n'))

def minimax(boardConfiguration):
    initializeDataStructures(boardConfiguration)

    global rootPlayer
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

    outputFileHandler.write('Node'+','+'Depth'+','+ 'Value'+'\n')
    outputFileHandler.write(str(root.state)+','+str(root.depth)+','+ str(root.value)+'\n')
    nextState = getNextState(root)
    printNextState(nextState)
