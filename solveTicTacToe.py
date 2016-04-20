import random
import sys

class Game:
    def __init__(self):
        # initial boards
        self.boards = {"A":range(9), "B":range(9), "C":range(9)}
        self.dead_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                              [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.simpleForm = '''
                    %s
                    %s %s %s
                    %s %s %s
                    %s %s %s
                    '''
        self.doubleForm = '''
                    %s       %s
                    %s %s %s     %s %s %s
                    %s %s %s     %s %s %s
                    %s %s %s     %s %s %s
                    '''
        self.tripleForm = '''
                    %s       %s       %s
                    %s %s %s     %s %s %s     %s %s %s
                    %s %s %s     %s %s %s     %s %s %s
                    %s %s %s     %s %s %s     %s %s %s
                    '''

    # ============== board section ==============
    # prints all living boards
    def printBoards(self):
        livingBoardList = [key for key in ["A", "B", "C"] \
                            if not self.isDead(self.boards[key])]
        if len(livingBoardList) == 1:
            key = livingBoardList[0]
            print self.simpleForm % tuple([key+": "] +
                                            self.boards[key][0:3] +
                                            self.boards[key][3:6] +
                                            self.boards[key][6:9])
        elif len(livingBoardList) == 2:
            key = livingBoardList
            print self.doubleForm % tuple([key[0]+": "] + [key[1]+": "] +
                                            self.boards[key[0]][0:3] + \
                                            self.boards[key[1]][0:3] + \
                                            self.boards[key[0]][3:6] + \
                                            self.boards[key[1]][3:6] + \
                                            self.boards[key[0]][6:9] + \
                                            self.boards[key[1]][6:9])
        elif len(livingBoardList) == 3:
            key = livingBoardList
            print self.tripleForm % tuple([key[0]+": "] + \
                                            [key[1]+": "] + \
                                            [key[2]+": "] + \
                                            self.boards[key[0]][0:3] + \
                                            self.boards[key[1]][0:3] + \
                                            self.boards[key[2]][0:3] + \
                                            self.boards[key[0]][3:6] + \
                                            self.boards[key[1]][3:6] + \
                                            self.boards[key[2]][3:6] + \
                                            self.boards[key[0]][6:9] + \
                                            self.boards[key[1]][6:9] + \
                                            self.boards[key[2]][6:9])
        #print "Fingerprints: " + str([self.getFingerprint(self.boards[key]) \
        #                            for key in ["A", "B", "C"]]) + " = " + \
        #                            str(self.multiplyFP(self.boards)) + "\n"

    # returns True if the input single board is dead
    def isDead(self, board):
        for pattern in self.dead_patterns:
            isCrossInARow = [board[index] == 'X' for index in pattern]
            if isCrossInARow == [True]*3:
                return True
        return False

    # returns True if all boards are dead
    def isAllBoardDead(self, boards):
        for board in boards.values():
            if not self.isDead(board):
                return False
        return True

    # returns a list of four rotated boards
    def rotate(self, board):
        rotated_boards = [board]
        temp = list(board)
        for i in range(3):
            newBoard = list(board)
            newBoard[0] = temp[6]
            newBoard[1] = temp[3]
            newBoard[2] = temp[0]
            newBoard[3] = temp[7]
            newBoard[5] = temp[1]
            newBoard[6] = temp[8]
            newBoard[7] = temp[5]
            newBoard[8] = temp[2]
            temp = list(newBoard)
            for i in range(9):
                if temp[i] != 'X':
                    temp[i] = i
            rotated_boards.append(temp)
        return rotated_boards

    # returns a list of four refleted boards
    def reflect(self, board):
        reflectedBoards = []
        newBoard = list(board)
        newBoard[0] = board[6]
        newBoard[1] = board[7]
        newBoard[2] = board[8]
        newBoard[6] = board[0]
        newBoard[7] = board[1]
        newBoard[8] = board[2]
        for i in range(9):
            if newBoard[i] != 'X':
                newBoard[i] = i
        reflectedBoards.append(newBoard)
        newBoard = list(board)
        newBoard[0] = board[2]
        newBoard[2] = board[0]
        newBoard[3] = board[5]
        newBoard[5] = board[3]
        newBoard[6] = board[8]
        newBoard[8] = board[6]
        for i in range(9):
            if newBoard[i] != 'X':
                newBoard[i] = i
        reflectedBoards.append(newBoard)
        newBoard = list(board)
        newBoard[1] = board[3]
        newBoard[3] = board[1]
        newBoard[5] = board[7]
        newBoard[7] = board[5]
        newBoard[2] = board[6]
        newBoard[6] = board[2]
        for i in range(9):
            if newBoard[i] != 'X':
                newBoard[i] = i
        reflectedBoards.append(newBoard)
        newBoard = list(board)
        newBoard[0] = board[8]
        newBoard[8] = board[0]
        newBoard[1] = board[5]
        newBoard[5] = board[1]
        newBoard[3] = board[7]
        newBoard[7] = board[3]
        for i in range(9):
            if newBoard[i] != 'X':
                newBoard[i] = i
        reflectedBoards.append(newBoard)
        return reflectedBoards

    # returns a list of unique transformed boards by rotation or reflection
    def transform(self, board):
        totalBoards = self.rotate(board)
        for pattern in self.reflect(board):
            if pattern not in totalBoards:
                totalBoards.append(pattern)
        return totalBoards

    def isSpace(self, boards, moveInput):
        if moveInput[0] in boards.keys() and int(moveInput[1]) in range(9):
            return boards[moveInput[0]][int(moveInput[1])] != 'X'
        return False

    # =========== fingerprint section ===========
    # returns the fingerprint of input single board
    def getFingerprint(self, board):
        if self.isDead(board):
            return {'1':1}
        pattern_1 = [['X', 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 'X', 2, 3, 4, 5, 6, 7, 8],
                     ['X', 'X', 'X', 3, 4, 5, 6, 7, 8],
                     ['X', 1, 2, 3, 'X', 5, 6, 7, 'X'],
                     ['X', 1, 2, 3, 4, 'X', 6, 'X', 8],
                     [0, 'X', 2, 3, 'X', 5, 6, 'X', 8],
                     ['X', 'X', 'X', 'X', 4, 5, 6, 7, 8],
                     ['X', 'X', 'X', 3, 'X', 5, 6, 7, 8],
                     ['X', 'X', 'X', 3, 4, 5, 'X', 7, 8],
                     ['X', 'X', 'X', 3, 4, 5, 6, 'X', 8],
                     ['X', 'X', 2, 3, 'X', 5, 6, 'X', 8],
                     ['X', 'X', 2, 3, 'X', 5, 6, 7, 'X'],
                     ['X', 1, 'X', 3, 'X', 5, 'X', 7, 8]]
        pattern_a = [['X', 1, 2, 3, 4, 5, 6, 7, 'X'],
                     [0, 'X', 2, 'X', 4, 5, 6, 7 , 8],
                     [0, 'X', 2, 3, 4, 5, 6, 'X' , 8],
                     ['X', 'X', 2, 3, 4, 5, 'X', 7, 8],
                     ['X', 1, 'X', 3, 'X', 5, 6, 7, 8],
                     ['X', 1, 'X', 3, 4, 5, 6, 'X', 8],
                     ['X', 1, 2, 3, 'X', 'X', 6, 7, 8],
                     ['X', 'X', 2, 'X', 'X', 5, 6, 7, 8],
                     ['X', 'X', 2, 'X', 4, 'X', 6, 7, 8],
                     ['X', 'X', 2, 'X', 4, 5, 6, 7, 'X'],
                     ['X', 'X', 2, 3, 4, 5, 6, 'X', 'X'],
                     ['X', 1, 'X', 3, 4, 5, 'X', 7, 'X'],
                     [0, 'X', 2, 'X', 4, 'X', 6, 'X', 8],
                     ['X', 'X', 2, 3, 'X', 'X', 'X', 7, 8],
                     ['X', 'X', 2, 3, 4, 'X', 'X', 'X', 8],
                     ['X', 'X', 2, 3, 4, 'X', 'X', 7, 'X'],
                     ['X', 'X', 2, 'X', 4, 'X', 6, 'X', 'X']]
        pattern_b = [['X', 1, 'X', 3, 4, 5, 6, 7, 8],
                     ['X', 1, 2, 3, 'X', 5, 6, 7, 8],
                     ['X', 1, 2, 3, 4, 'X', 6, 7, 8],
                     [0, 'X', 2, 3, 'X', 5, 6, 7, 8],
                     ['X', 'X', 2, 'X', 4, 5, 6, 7, 8],
                     [0, 'X', 2, 'X', 4, 'X', 6, 7, 8],
                     ['X', 'X', 2, 3, 'X', 'X', 6, 7, 8],
                     ['X', 'X', 2, 3, 'X', 5, 'X', 7, 8],
                     ['X', 'X', 2, 3, 4, 'X', 'X', 7, 8],
                     ['X', 'X', 2, 3, 4, 5, 'X', 'X', 8],
                     ['X', 'X', 2, 3, 4, 5, 'X', 7, 'X'],
                     ['X', 1, 'X', 3, 'X', 5, 6, 'X', 8],
                     ['X', 1, 2, 3, 'X', 'X', 6, 'X', 8],
                     ['X', 'X', 2, 'X', 4, 'X', 6, 'X', 8],
                     ['X', 'X', 2, 'X', 4, 'X', 6, 7, 'X']]
        pattern_c = [[0, 1, 2, 3, 4, 5, 6, 7, 8]]
        pattern_d = [['X', 'X', 2, 3, 4, 'X', 6, 7, 8],
                     ['X', 'X', 2, 3, 4, 5, 6, 'X', 8],
                     ['X', 'X', 2, 3, 4, 5, 6, 7, 'X']]
        pattern_ab = [['X', 'X', 2, 3, 'X', 5, 6, 7, 8],
                      ['X', 1, 'X', 3, 4, 5, 'X', 7, 8],
                      [0, 'X', 2, 'X', 'X', 5, 6, 7, 8],
                      ['X', 'X', 2, 3, 4, 'X', 6, 'X', 8],
                      ['X', 'X', 2, 3, 4, 'X', 6, 7, 'X']]
        pattern_ad = [['X', 'X', 2, 3, 4, 5, 6, 7, 8]]
        pattern_c2 = [[0, 1, 2, 3, 'X', 5, 6, 7, 8]]
        living_patterns = pattern_1 + pattern_a + pattern_b + pattern_c + \
                       pattern_d + pattern_ab + pattern_ad + pattern_c2
        transformedBoard = [i for i in self.transform(board) \
                                if i in living_patterns][0]
        if transformedBoard in pattern_1:
            return {'1':1}
        elif transformedBoard in pattern_a:
            return {'a':1}
        elif transformedBoard in pattern_b:
            return {'b':1}
        elif transformedBoard in pattern_c:
            return {'c':1}
        elif transformedBoard in pattern_d:
            return {'d':1}
        elif transformedBoard in pattern_ab:
            return {'a':1, 'b':1}
        elif transformedBoard in pattern_ad:
            return {'a':1, 'd':1}
        elif transformedBoard in pattern_c2:
            return  {'c':2}
        else:
            return False

    # returns the multiplied fingerprint of input boards
    def multiplyFP(self, boards):
        fingerprints = [self.getFingerprint(boards[key]) \
                            for key in ["A", "B", "C"]]
        totalFP = {}
        for boardFP in fingerprints:
            for cha in boardFP:
                if cha not in totalFP.keys():
                    totalFP[cha] = boardFP[cha]
                else:
                    totalFP[cha] += boardFP[cha]
        if '1' in totalFP.keys():
            if totalFP.keys() != ['1']:
                del totalFP['1']
            else:
                totalFP = {'1':1}
        return totalFP

    # ================ AI section ================
    # Evaluation function of state
    def evalFunc(self, boards):
        winning_fingerprints = [{"a":1}, {"b":2}, {"c":2}, {"b":1, "c":1}]
        fingerPrint = self.multiplyFP(boards)
        if fingerPrint in winning_fingerprints:
            return 10
        return 0

    # returns successor boards given current boards and action
    def getSuccBoards(self, boards, action):
        succBoards = {}
        for key in ["A", "B", "C"]:
            succBoards[key] = list(boards[key])
        succBoards[action[0]][int(action[1])] = 'X'
        return succBoards

    # returns a list of legal actions given boards
    def getLegalActions(self, boards):
        livingBoardList = [key for key in ["A", "B", "C"] \
                            if not self.isDead(self.boards[key])]
        legalActions = []
        for key in livingBoardList:
            legalActions += [key+str(i) for i in boards[key] if i != "X"]
        return legalActions

    # maxValue function in Minimax Search
    def getAIMove(self, boards):
        legalActions = self.getLegalActions(boards)
        maxValue = -float("inf")
        maxAct = None
        for act in legalActions:
            succ  = self.getSuccBoards(boards, act)
            evalSucc = self.evalFunc(succ)
            if evalSucc > maxValue:
                maxValue = evalSucc
        maxActs = [act for act in legalActions \
                if self.evalFunc(self.getSuccBoards(boards, act)) == maxValue]
        # Randomness for more interesting moves
        return random.choice(maxActs)

    # returns player's input
    def getPlayerMove(self, boards):
        move = raw_input("Your move: ").upper()
        while len(move) != 2 or move[0] not in boards.keys() or\
                not self.isSpace(boards, move) or self.isDead(boards[move[0]]):
            move = raw_input("Invalid move! Enter your move again: ").upper()
        return move

    # execute the move on boards
    def makeMove(self, boards, move):
        boards[move[0]][int(move[1])] = 'X'

    # ============ game flow section ============
    # introduction of the game
    def intro(self):
        print '''
                \n\tThis game contains three 3x3 classic Tic-Tac-Toe boards.
                \n\tBoth player and AI play 'X'.
                \n\tThe player who plays the last move loses the game.
                \n\tAI will always make the first move.
                \n\tYou can play the game as follows: e.g., if you enter 'A1',
                \n\tthat means you want to put a cross in position 1 of board A.
                \n\tPress Ctrl + C to quit the game
              '''

    # start the game
    def startGame(self):
        print '''
                \n\t-------------------------------------
                \n\tWelcome to 3-board misere Tic-Tac-Toe
                \n\t-------------------------------------
              '''
        self.intro()
        self.enterLoop()

    # enter the loop
    def enterLoop(self):
        playFlag = True
        turn = "AI"
        while playFlag:
            # Get move
            if turn == "AI":
                move = self.getAIMove(self.boards)
                print "AI: " + move
            elif turn == "Player":
                move = self.getPlayerMove(self.boards)
            self.makeMove(self.boards, move)
            # print all living boards
            self.printBoards()
            if self.isAllBoardDead(self.boards):
                break
            # Turn switching
            if turn == "AI":
                turn = "Player"
            else:
                turn = "AI"
        # Winning/losing message
        if turn == "AI":
            print '''
                    \n\t-------------------------------------
                    \n\tCongratulations! You won against AI!
                    \n\t-------------------------------------
                  '''
        else:
            print '''
                    \n\t----------------------------
                    \n\tGame over! You are defeated!
                    \n\t----------------------------
                  '''
        self.endGame()

    # end the game
    def endGame(self):
        playAgain = raw_input("Play again?(y/n): ").lower()
        if playAgain == "y":
            self.__init__()
            self.startGame()
        else:
            print '''
                    \n\t-----------------------------------------
                    \n\tThank you for playing! See you next time!
                    \n\t-----------------------------------------
                  '''
            sys.exit()

if __name__ == "__main__":
    TicTacToe = Game()
    TicTacToe.startGame()
