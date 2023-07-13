"""
Program requirements:
    Python 3.10
    'pygame' module (pypi.org/project/pygame)
    'chess' module (pypi.org/project/chess)
"""


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
    
    def getVMoves(self):
        """Get all valid moves, considering checks
        1. Generate all possible moves
        2. For each move, make that move
        3. Generate all opponent's moves
        4. For each opponent move, see if it attacks the king
        5. If it does, it is not valid
        """
        moves = self.getPMoves()
        
        for i in range(len(moves)-1, -1, -1): # Go backwards through the list
            self.makeMove(moves[i])
            self.whiteMove = not self.whiteMove 
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteMove = not self.whiteMove
            self.undoMove()
        if len(moves) == 0: # Checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        
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
            if column + 1 <= 7: # Captures to the right
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
        else:
            if self.board[row + 1][column] == "--": # Advance pawns by 1 square
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "--": # Advance pawns by 2 squares
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0: # Captures to the left
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            if column + 1 <= 7: # Captures to the right
                if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))
                
                
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
            if 0 <= endRow < 8 and 0 <= endCol <= 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != friendlyColor: # Enemy piece or empty square
                    moves.append(Move((row, column), (endRow, endCol), self.board))


class Move():
    # Converting ranks to rows, files to columns, and vice versa
    rankstoRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colstoFiles = {v: k for k, v in filestoCols.items()}
    
    def __init__(self, start, end, board):
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
    
    # Override the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.ID == other.ID
    
    def getNotation(self):
        """Convert a starting coordinate and an end coordinate into readable notation."""
        return self.getRF(self.startRow, self.startCol) + self.getRF(self.endRow, self.endCol)
    
    def getRF(self, row, column):
        """Get the rank and file of a square given its row and column."""
        return self.colstoFiles[column] + self.rowstoRanks[row]

"""

Below this class is the main code. It is responsible for handling user input,
as well as displaying the current GameState object.
 
"""
 
import pygame
# from chess import ChessEngine
 
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
    moveMade = False # Flag this variable when a valid move is made
    loadImages() # This loads all of the images, which should only be done once
    selected = () # Initially, no square is selected. This should keep track of the user's last clicked square as a tuple (row, column)
    clicks = [] # This should keep track of the player's current clicks as two tuples in a list [(start_row, start_column), (end_row, end_column)]
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN: # Key handler
                if event.key == pygame.K_z:
                    state.undoMove()
                    moveMade = True
            elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse handler
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
                    print(move.getNotation())
                    if move in valid:
                        state.makeMove(move)
                        moveMade = True
                        selected = () # Reset user clicks
                        clicks = []
                    else:
                        clicks = [selected] 
        
        if moveMade:
            valid = state.getVMoves()
            moveMade = False
        drawState(screen, state)
        clock.tick(FPS)
        pygame.display.flip()

# Draw the current GameState onto the board

def drawState(screen, state):
    drawBoard(screen) # Draw the squares on the board
    drawPieces(screen, state.board) # Draw the pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    """
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



if __name__ == "__main__":
    main()










