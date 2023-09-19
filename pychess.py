"""
Program requirements:
    Python 3.10
    'pygame' module (pypi.org/project/pygame) 
"""

"""
MoveFinder:
This section of the code is responsible for generating the moves used by the computer-controlled pieces.
"""

import random, pygame
from copy import deepcopy
from time import sleep

pieceScore = {"K":100, "Q":10, "R":5, "B":3, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def FLIP(LISTIN):
    LISTOUT = deepcopy(LISTIN)
    LISTOUT.reverse()
    return LISTOUT

def NEGATE(LISTIN):
    return [-i for i in LISTIN]



# Random move generator - deprecated
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

# Returns move for the AI opponent
def findBestMove(state, valid):
    # Due to how Python handles assignment statements, deep-copying the castling rights
    # before the next AI move is generated and replacing the castling rights after
    # the AI move is required due to Python removing the rights by mistake.
    # For more information see https://tinyurl.com/copypython
    
    TEMP_CASTLING = deepcopy(state.currentCastling)
    global nextMove
    nextMove = None
    alphabeta = [-CHECKMATE, CHECKMATE]
    random.shuffle(valid)
    findNMAlphaBetaMove(state, valid, DEPTH, alphabeta, 1 if state.whiteMove else -1)
    state.currentCastling = TEMP_CASTLING
    return nextMove

# MinMax algorithm - deprecated
def findMinMaxMove(state, valid, depth, whiteMove):
    global nextMove
    if not depth:
        return findBoardScore(state)
    
    if whiteMove:
        maxScore = -CHECKMATE
        for move in valid:
            state.makeMove(move)
            nextMoves = state.getVMoves()
            score = findMinMaxMove(state, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            state.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in valid:
            state.makeMove(move)
            nextMoves = state.getVMoves()
            score = findMinMaxMove(state, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            state.undoMove()
        return minScore

# NegaMax algorithm wihtout Alpha-Beta pruning - deprecated
def findNegaMaxMove(state, valid, depth, turnMulti):
    global nextMove
    if not depth:
        return turnMulti * findBoardScore(state)
    
    maxScore = -CHECKMATE
    for move in valid:
        state.makeMove(move)
        nextMoves = state.getVMoves()
        score = -findNegaMaxMove(state, nextMoves, depth - 1, -turnMulti)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        state.undoMove()
    return maxScore

# NegaMax algorithm with Alpha-Beta pruning
def findNMAlphaBetaMove(state, valid, depth, alphabeta, turnMulti):
    # alphabeta = [alpha, beta]
    global nextMove
    if not depth:
        return turnMulti * findBoardScore(state)
    
    # move ordering will come later
    maxScore = -CHECKMATE
    for move in valid:
        state.makeMove(move)
        nextMoves = state.getVMoves()
        score = -findNMAlphaBetaMove(state, nextMoves, depth-1, NEGATE(FLIP(alphabeta)), -turnMulti)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        state.undoMove()
        
        # Pruning starts here
        if maxScore > alphabeta[0]:
            alphabeta[0] = maxScore
        if alphabeta[0] >= alphabeta[1]:
            break
    return maxScore


def findBoardScore(state):
    """Generate a score given the current GameState.
    Similar to evaluation number seen in other chess programs like lichess.org or chess.com
    """
    if state.checkmate:
        if state.whiteMove:
            return -CHECKMATE # Black wins
        else:
            return CHECKMATE # White wins
    elif state.stalemate:
        return STALEMATE
    SCORE = 0
    for row in state.board:
        for square in row:
            match square[0]:
                case "w":
                    SCORE += pieceScore[square[1]]
                case "b":
                    SCORE -= pieceScore[square[1]]
    
    return SCORE

"""

GameState:
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state, and a move log.

"""

class GameState:
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.functions = {"p": self.getPawnMoves,
                          "R": self.getRookMoves,
                          "B": self.getBishopMoves,
                          "N": self.getKnightMoves,
                          "Q": self.getQueenMoves,
                          "K": self.getKingMoves}
        self.whiteMove = True
        self.log = []
        self.wKlocation = (7, 4)
        self.bKlocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant = () # Coordinates for the square where it is possible
        self.currentCastling = Castling(True, True, True, True)
        self.castlingLog = [Castling(self.currentCastling.kingside[0],
                                     self.currentCastling.kingside[1],
                                     self.currentCastling.queenside[0],
                                     self.currentCastling.queenside[1])]

    def makeMove(self, move):
        """Basic move execution (excluding castling, en-passant, and pawn promotion)"""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.log.append(move) # Log the current move so we can undo it later
        self.whiteMove = not self.whiteMove # Switch the turns
        if move.pieceMoved == "wK": # Update the location of the white king
            self.wKlocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK": # Update the location of the black king
            self.bKlocation = (move.endRow, move.endCol)

        if move.isPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
        
        if move.isEnPassant:
            self.board[move.startRow][move.endCol] = "--"
        
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassant = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassant = ()
        
        if move.isCastle:
            match (move.endCol - move.startCol):
                case 2: # kingside/short castling
                    self.board[move.endRow][move.endCol-1], self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol+1], self.board[move.endRow][move.endCol-1]
                case _: # queenside/long castling
                    self.board[move.endRow][move.endCol+1], self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol-2], self.board[move.endRow][move.endCol+1]
        
        self.updateCastling(move)
        self.castlingLog.append(Castling(self.currentCastling.kingside[0],
                                         self.currentCastling.kingside[1],
                                         self.currentCastling.queenside[0],
                                         self.currentCastling.queenside[1]))
    
    def undoMove(self):
        """Undo a move."""
        if len(self.log) != 0: # Make sure there is a move to undo
            move = self.log.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteMove = not self.whiteMove # Switch the turns back
            if move.pieceMoved == "wK": # Update the location of the white king
                self.wKlocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK": # Update the location of the black king
                self.bKlocation = (move.startRow, move.startCol)
            
            if move.isEnPassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassant = (move.endRow, move.endCol)
            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
                self.enpassant = ()
            
            self.castlingLog.pop()
            self.currentCastling = self.castlingLog[-1]
            
            if move.isCastle:
                match (move.endCol - move.startCol):
                    case 2: # kingside/short castling
                        self.board[move.endRow][move.endCol-1], self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol+1], self.board[move.endRow][move.endCol-1]
                    case _: # queenside/long castling
                        self.board[move.endRow][move.endCol+1], self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol-2], self.board[move.endRow][move.endCol+1]
                
    
    def updateCastling(self, move):
        """Update the castling rights if the given move was a king move or a rook move:
        If the king or the rook was moved by <colour>,
        then <colour>'s right to castle should be removed.
        """
        match move.pieceMoved:
            case "wK":
                self.currentCastling.kingside[0] = False
                self.currentCastling.queenside[0] = False
            case "bK":
                self.currentCastling.kingside[1] = False
                self.currentCastling.queenside[1] = False
            case "wR":
                if move.startRow == 7:
                    if move.startRow == 0:
                        self.currentCastling.queenside[0] = False
                    elif move.startRow == 7:
                        self.currentCastling.kingside[0] = False
            case "bR":
                if move.startRow == 0:
                    if move.startCol == 0:
                        self.currentCastling.queenside[1] = False
                    elif move.startCol == 7:
                        self.currentCastling.kingside[1] = False
        match move.pieceCaptured:
            case "wR":
                if move.endRow == 7:
                    if move.endCol == 0:
                        self.currentCastling.queenside[0] = False
                    elif move.endCol == 7:
                        self.currentCastling.kingside[0] = False
            case "bR":
                if move.endRow == 0:
                    if move.endCol == 0:
                        self.currentCastling.queenside[1] = False
                    elif move.endCol == 7:
                        self.currentCastling.kingside[1] = False
                
                
    
    def getVMoves(self):
        """Get all valid moves, considering checks
        1. Generate all possible moves
        2. For each move, make that move
        3. Generate all opponent's moves
        4. For each opponent move, see if it attacks the king
        5. If it does, it is not valid
        """
        
        #for log in self.castlingLog:
        #   print(f"MOVE {self.castlingLog.index(log)}:: kingside white: {log.kingside[0]}, queenside white: {log.queenside[0]}")
        #   print(f"MOVE {self.castlingLog.index(log)}:: kingside black: {log.kingside[1]}, queenside black: {log.queenside[1]}")
        #print("\n")
        
        tempenpassant = self.enpassant
        tempCastling = Castling(self.currentCastling.kingside[0],
                                self.currentCastling.kingside[1],
                                self.currentCastling.queenside[0],
                                self.currentCastling.queenside[1])
        
        moves = self.getPMoves()
        if self.whiteMove:
            self.getCastlingMoves(self.wKlocation[0], self.wKlocation[1], moves)
        else:
            self.getCastlingMoves(self.bKlocation[0], self.bKlocation[1], moves)
        
        for i in range(len(moves)-1, -1, -1): # Go backwards through the list
            self.makeMove(moves[i])
            self.whiteMove = not self.whiteMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteMove = not self.whiteMove
            self.undoMove()
        if len(moves) == 0: # Checkmate or stalemate
            self.checkmate, self.stalemate = (True, False) if self.inCheck() else (False, True)
        else:
            self.checkmate, self.stalemate = False, False

        
        self.enpassant = tempenpassant
        self.currentCastling = tempCastling
        return moves
    
    def inCheck(self):
        if self.whiteMove:
            return self.squareAttacked(self.wKlocation[0], self.wKlocation[1])
        else:
            return self.squareAttacked(self.bKlocation[0], self.bKlocation[1])
    
    def squareAttacked(self, row, column):
        self.whiteMove = not self.whiteMove # Switch to opponent's turn
        opponentMoves = self.getPMoves()
        self.whiteMove = not self.whiteMove # Switch turns back
        for move in opponentMoves:
            if move.endRow == row and move.endCol == column: # Square is under attack
                return True
        return False
        
    
    def getPMoves(self):
        """Get all possible moves, without considering checks"""
        moves = []
        for row in range(len(self.board)): # Number of rows
            for column in range(len(self.board[row])): # Number of columns in a given row
                piece = (self.board[row][column][0], self.board[row][column][1])
                if (piece[0] == "w" and self.whiteMove) or (piece[0] == "b" and not self.whiteMove):
                    self.functions[piece[1]](row, column, moves)
        return moves
    
    def getPawnMoves(self, row, column, moves):
        if self.whiteMove: # It is white's turn, look at the white pawns
            if self.board[row - 1][column] == "--": # Advance pawns by 1 square
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "--": # Advance pawns by 2 squares
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0: # Captures to the left
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
                elif (row - 1, column - 1) == self.enpassant:
                    moves.append(Move((row, column), (row - 1, column - 1), self.board, isEnPassant = True))
            if column + 1 <= 7: # Captures to the right
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
                elif (row - 1, column + 1) == self.enpassant:
                    moves.append(Move((row, column), (row - 1, column + 1), self.board, isEnPassant = True))
        else:
            if self.board[row + 1][column] == "--": # Advance pawns by 1 square
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "--": # Advance pawns by 2 squares
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0: # Captures to the left
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
                elif (row + 1, column - 1) == self.enpassant:
                    moves.append(Move((row, column), (row + 1, column - 1), self.board, isEnPassant = True))
            if column + 1 <= 7: # Captures to the right
                if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))
                elif (row + 1, column + 1) == self.enpassant:
                    moves.append(Move((row, column), (row + 1, column + 1), self.board, isEnPassant = True))
                
                
    def getRookMoves(self, row, column, moves):
        directions = ( (-1, 0), (0, -1), (1, 0), (0, 1) )
        enemyColor = "b" if self.whiteMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece
                        break
                else: # Off the board
                    break
                    
    def getBishopMoves(self, row, column, moves):
        directions = ( (-1, -1), (-1, 1), (1, -1), (1, 1) )
        enemyColor = "b" if self.whiteMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece
                        break
                else: # Off the board
                    break
                
    def getKnightMoves(self, row, column, moves):
        directions = ( (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1) )
        friendlyColor = "w" if self.whiteMove else "b"
        for d in directions:
            endRow = row + d[0]
            endCol = column + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != friendlyColor: # Enemy piece or empty square
                    moves.append(Move((row, column), (endRow, endCol), self.board))
                    
    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)
        
    def getKingMoves(self, row, column, moves):
        kingMoves = ( (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) )
        friendlyColor = "w" if self.whiteMove else "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = column + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != friendlyColor: # Enemy piece or empty square
                    moves.append(Move((row, column), (endRow, endCol), self.board))
    
    def getCastlingMoves(self, row, column, moves):
        """Generate valid castling moves for the king at (row, column)
        There are two additional rules for castling (excluding the rules that the king and the rook must not have moved):
        1. The king must not be in check
        2. The king cannot pass through spaces under attack
        """
        
        if self.squareAttacked(row, column):
            return
        if (self.whiteMove and self.currentCastling.kingside[0]) or (not self.whiteMove and self.currentCastling.kingside[1]):
            self.castleShort(row, column, moves)
        if (self.whiteMove and self.currentCastling.queenside[0]) or (not self.whiteMove and self.currentCastling.queenside[1]):
            self.castleLong(row, column, moves)
        
    def castleShort(self, row, column, moves):
        """Kingside castling, use alongside GameState.getCastlingMoves()"""
        if self.board[row][column + 1] == self.board[row][column + 2] == "--":
            if not (self.squareAttacked(row, column + 1) or self.squareAttacked(row, column + 2)):
                moves.append(Move( (row, column), (row, column + 2), self.board, isCastle=True ))
    def castleLong(self, row, column, moves):
        """Queenside castling, use alongside GameState.getCastlingMoves()"""
        if self.board[row][column - 1] == self.board[row][column - 2] == self.board[row][column - 3] == "--":
            if not (self.squareAttacked(row, column - 1) or self.squareAttacked(row, column - 2)):
                moves.append(Move( (row, column), (row, column - 2), self.board, isCastle=True ))
    
        
class Castling():
    def __init__(self, shortW, shortB, longW, longB):
        """
        The terms 'short' and 'long' refer to the types of castling:
        Short castling is another way of referring to kingside castling,
        Long castling is another way of referring to queenside castling.
        
        self.kingside and self.queenside are set up as a tuple to reduce lines.
        The first item in both tuples are white's rights, and the second item is black's rights
        """
        self.kingside = [shortW, shortB]
        self.queenside = [longW, longB]
        

class Move():
    # Converting ranks to rows, files to columns, and vice versa
    rankstoRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colstoFiles = {v: k for k, v in filestoCols.items()}
    
    def __init__(self, start, end, board, isEnPassant = False, isCastle = False):
        def getID(*args):
            length = len(args)
            temp = 0
            for i in range(length, 0, -1):
                item = args[(length - i)]
                temp += item * (10 ** (i - 1))
            return temp
        
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.ID = getID(self.startRow, self.startCol, self.endRow, self.endCol)
        
        self.isPromotion = False
        self.isPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        
        self.isEnPassant = isEnPassant
        if self.isEnPassant:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        self.isCastle = isCastle

    # Override the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.ID == other.ID
    
    def getEndMove(self):
        """Convert an end coordinate into readable notation."""
        return self.getRF(self.endRow, self.endCol)
    
    def getStartMove(self):
        """Convert a start coordinate into readable notation."""
        return self.getRF(self.startRow, self.startCol)
    
    def getRF(self, row, column):
        """Get the rank and file of a square given its row and column."""
        return self.colstoFiles[column] + self.rowstoRanks[row]

"""

Below this class is the main code. It is responsible for handling user input,
as well as displaying the current GameState object.

"""
 
WIDTH, HEIGHT = 512, 512
DIMENSION = 8 # Dimension of the chess board
squareSize = HEIGHT // DIMENSION
FPS = 15
IMAGES = {} # Blank dictionary to store images

# Initialize images. This will be called once in the main loop.
def loadImages():
    """Loads all images into a dictionary called 'IMAGES' to be referenced when creating the board."""
    pieces = ["wp","wR","wN","wB","wQ","wK","bp","bR","bN","bB","bQ","bK"]
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load("images/%s.png" % p), (squareSize, squareSize))

# Main function - handles user input and updating graphics

def main():
    pygame.init() # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Set the height and width of the pygame window
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    state = GameState()
    valid = state.getVMoves()
    
    anim = False # Flag this variable when you want to animate a move
    moveMade = False # Flag this variable when a valid move is made
    
    gameOver = False # Flag this variable when the game is over
    loadImages() # This loads all of the images, which should only be done once
    
    selected = () # Initially, no square is selected. This should keep track of the user's last clicked square as a tuple (row, column)
    clicks = [] # This should keep track of the player's current clicks as two tuples in a list [(start_row, start_column), (end_row, end_column)]
    
    whitePlayer = True # If a human is playing white, this variable is set to True. If an AI is playing white, this variable is False
    blackPlayer = False # If a human is playing black, this variable is set to False. If an AI is playing black, this variable is True
    
    done = False
    while not done:
        humanTurn = (state.whiteMove and whitePlayer) or (not state.whiteMove and blackPlayer)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN: # Key handler
##                if event.key == pygame.K_z: # Undo move
##                    state.undoMove()
##                    moveMade = True
##                    anim = False
                if event.key == pygame.K_r: # Reset game
                    state = GameState()
                    valid = state.getVMoves()
                    selected = ()
                    clicks = []
                    moveMade = False
                    anim = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse handler
                if not gameOver and humanTurn:
                    mousepos = pygame.mouse.get_pos() # Get the location of the mouse in the window, stored as (x, y)
                    column = mousepos[0] // squareSize
                    row = mousepos[1] // squareSize
                    if (row, column) == selected: # Check if the user has clicked the same square twice
                        selected = () # Clear the last clicked square stored in the tuple.
                        clicks = [] # Clear the player's current clicks
                    else:
                        selected = (row, column)
                        clicks.append(selected) # Append the 'clicks' list for both the 1st and 2nd clicks
                    if len(clicks) == 2: # Check if there are two coordinates in the 'clicks' list
                        move = Move(clicks[0], clicks[1], state.board)
                        """
                        notation = (move.getEndMove()) if (move.pieceMoved[1] == "p") or (move.pieceMoved == "-") else (move.pieceMoved[1] + move.getEndMove())
                        if move.pieceCaptured != "--":
                            if move.pieceMoved[1] != "p":
                                notation = [i for i in notation]
                                notation.insert(1, "x")
                            else:
                                notation = [i for i in notation]
                                notation.insert(0, move.getStartMove()[0])
                                notation.insert(1, "x")
                        if state.inCheck():
                            notation = [i for i in notation]
                            notation.append("+")
                        notation = "".join(notation)
                        print(notation)
                        """
                        for i in range(len(valid)):
                            if move == valid[i]:
                                state.makeMove(valid[i])
                                anim = True
                                moveMade = True
                                selected = () # Reset user clicks
                                clicks = []
                        if not moveMade:
                            clicks = [selected] 
        
        # AI move finder
        if not (gameOver or humanTurn):
            AIMove = findBestMove(state, valid)
            if AIMove is None:
                AIMove = findRandomMove(valid)
            state.makeMove(AIMove)
            moveMade = True
            anim = True
        
        if moveMade:
            if anim:
                animate(screen, state.log[-1], state.board, clock)
            valid = state.getVMoves()
            moveMade = False
            anim = False
            
        drawState(screen, state, valid, selected)
        
        if state.checkmate:
            gameOver = True
            done = True
            if state.whiteMove:
                drawText("Game finished - Black won by checkmate!", screen)
            else:
                drawText("Game finished - White won by checkmate!", screen)
        elif state.stalemate:
            gameOver = True
            done = True
            drawText("Game finished - Draw by stalemate", screen)
        
        clock.tick(FPS)
        pygame.display.flip()

def squareHighlight(screen, state, moves, squareSelected):
    """Move highlighting: Highlight both the piece selected and where it can move.

    Args:
        screen: pygame window
        state: the current state of the board
        moves: list of valid moves
        square: the square selected
    """
    if squareSelected != ():
        row, column = squareSelected
        if state.board[row][column][0] == ("w" if state.whiteMove else "b"):
            SQUARE = pygame.Surface((squareSize, squareSize))
            SQUARE.set_alpha(100) # Transparency (transparent : 0 -> 255 : opaque)
            SQUARE.fill(pygame.Color("blue"))
            screen.blit(SQUARE, (column * squareSize, row * squareSize))
            SQUARE.fill(pygame.Color("yellow"))
            for move in moves:
                if move.startRow == row and move.startCol == column:
                    screen.blit(SQUARE, (squareSize * move.endCol, squareSize * move.endRow))
                    

# Draw the current GameState onto the board

def drawState(screen, state, validMoves, selectedSquare):
    drawBoard(screen) # Draw the squares on the board
    squareHighlight(screen, state, validMoves, selectedSquare)
    drawPieces(screen, state.board) # Draw the pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    """
    global colors
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * squareSize, row * squareSize, squareSize, squareSize))



def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current GameState.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": # Piece is not empty!
                screen.blit(IMAGES[piece], pygame.Rect(column * squareSize, row * squareSize, squareSize, squareSize))

def animate(screen, move, board, clock):
    """Animate the given move."""
    global colors
    rowChange = move.endRow - move.startRow
    columnChange = move.endCol - move.startCol
    frames = 6 # frames per square
    fCount = frames * (abs(rowChange) + abs(columnChange))
    
    for f in range(fCount + 1):
        temp = [rowChange*f/fCount, columnChange*f/fCount]
        row, column = move.startRow + temp[0], move.startCol + temp[1]
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        finalSquare = pygame.Rect(move.endCol * squareSize, move.endRow * squareSize, squareSize, squareSize)
        pygame.draw.rect(screen, color, finalSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], finalSquare)
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(column * squareSize, row * squareSize, squareSize, squareSize))
        
        pygame.display.flip()
        clock.tick(60)

def drawText(text, screen):
    FONT = pygame.font.SysFont("Arial", 24, True, False)
    textObj = FONT.render(text, 0, pygame.Color("red"))
    textLoc = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    screen.blit(textObj, textLoc)

if __name__ == "__main__":
    main()
    sleep(5)

"""
A portion of this code was derived from Eddie Sharick, Teacher of Computer Science and Physics
His YouTube channel is linked below:
https://www.youtube.com/@eddiesharick6649
"""
