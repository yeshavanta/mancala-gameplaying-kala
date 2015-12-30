__author__ = 'ykp'
from Modules import competition
from Modules import alphabeta
from Modules import greedyagain
from Modules import minimax
import time

def readBoardConfigurationsFromInputFile(filename):
    inputFileHandler = open(filename,"r")

    boardConfiguration = {}
    counter = 1;
    while True:

        line = inputFileHandler.readline()
        line = line.rstrip()

        if line=='':
            break

        if counter ==1:
            boardConfiguration["task"] = int(line)
            counter += 1

        elif counter ==2:
            boardConfiguration["playerRole"] = int(line)
            counter += 1

        elif counter == 3:
            boardConfiguration["cutoffDepth"] = int(line)
            counter += 1

        elif counter == 4:
            splitLine = line.split(' ')
            boardConfiguration["player2BoardConfiguration"] = splitLine
            counter += 1

        elif counter == 5:
            splitLine = line.split(' ')
            boardConfiguration["player1BoardConfiguration"] = splitLine
            counter += 1

        elif counter == 6:
            boardConfiguration["player2MancalaCount"] = int(line)
            counter += 1

        elif counter == 7:
            boardConfiguration["player1MancalaCount"] = int (line)
            counter += 1
    return boardConfiguration


if __name__ =='__main__':
    start_time = time.time()
    boardConfiguration = readBoardConfigurationsFromInputFile("input.txt")
    strategy = boardConfiguration["task"]

    if strategy == 1:
        boardConfiguration["cutoffDepth"] == 1
        greedyagain.greedy(boardConfiguration)

    elif strategy== 2:
        minimax.minimax(boardConfiguration)

    elif strategy == 3:
        alphabeta.alphabeta(boardConfiguration)

    else:
        competition.competition(boardConfiguration,start_time)




