"""
PyChess AI
Chess board using Tkinter + Chess AI using Tensorflow

Python should be able to take a FEN notation,
i.e. rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
and put it into a list modified,
i.e. ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", 0, "KQkq", 0, [0, 1]]
and then go through and set the current state of the board.

test FENs:

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
r1bk3R/pp3Q2/8/2N1Pp2/6p1/6P1/PP3PP1/R3K3 b Q - 0 0


"""

import pygame, os

# Set the INTERNAL chess board, chess pieces and images

# chess_board_int = [[ *list of pieces* ], [ *list of coordinates* ]] 
# pieces = chess_board_int[0], coords = chess_board_int[1]
chess_board_int = [[
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
], [
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
    [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)],
    [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)],
    [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)],
    [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)],
    [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
    [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
]]



################################################################

# Under construction - all pieces will be replaced with sprites in the near future

################################################################

img_dir = "chess_pieces"
pieces = {}
for filename in os.listdir(img_dir):
    name, ext = os.path.splitext(filename)
    pieces[name] = pygame.image.load(os.path.join(img_dir, filename))

chess_pieces = {
    "b": "bishop_B",
    "B": "bishop_W",
    "k": "king_B",
    "K": "king_W",
    "n": "knight_B",
    "N": "knight_W",
    "p": "pawn_B",
    "P": "pawn_W",
    "q": "queen_B",
    "Q": "queen_W",
    "r": "rook_B",
    "R": "rook_W",

}


class cPiece(pygame.sprite.Sprite):
    def __init__(self, pieceType, x, y):
        img_dir = "chess_pieces"
        chess_images = {}
        for filename in os.listdir(img_dir):
            name, ext = os.path.splitext(filename)
            pieces[name] = pygame.image.load(os.path.join(img_dir, filename))

        chess_pieces = {
            "b": "bishop_B",
            "B": "bishop_W",
            "k": "king_B",
            "K": "king_W",
            "n": "knight_B",
            "N": "knight_W",
            "p": "pawn_B",
            "P": "pawn_W",
            "q": "queen_B",
            "Q": "queen_W",
            "r": "rook_B",
            "R": "rook_W",
            
        }
        if pieceType not in ["b", "B", "k", "K", "n", "N", "p", "P", "q", "Q", "r", "R"] or (not isinstance(x, int)) or (not isinstance(y, int)):
            emsg = "Class cPiece() was not called correctly - check input"
            raise Warning(emsg)
        
        self.piece = chess_pieces[pieceType]
        self.image = chess_images[self.piece]
        self.coords = (x, y)
    def setCoords(self, newX, newY):
        self.coords = (newX, newY)
    def getCoords(self):
        return self.coords

################################################################

# Under construction - all pieces will be replaced with sprites in the near future

################################################################



# Generate a modified FEN list given regular FEN notation
# Update the chess board given a FEN list
# Convert a modified FEN list to regular FEN notation
class FEN:
    """Convert between FEN list and regular FEN notation and update the internal chess board
    given the FEN string corresponding to the requested board position.
    
    Functions:
        get_fen_list(fen_string) - Convert regular FEN notation to a FEN list that is 
        easier to use, especially when trying to update the board

        update_board(fen_list) - Update the current board using a given FEN list.

        get_current_fen() - Read the current board and generate a regular FEN string.

        evaluate(fen_string) - Evaluate the current position of a board given the FEN string
        [Requires 'chess', 'chess.engine', and a local copy of 'stockfish.exe']
        
    """
    def get_fen_list(fen_string):
        # Example of a fen string: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # First, split the string into a list for every space, except the last two numbers
        fen_list = fen_string[:-4].split(" ")
        # Then, create a temproary list to contain the last two numbers (and then convert them to a string)
        # After that, append the temproary list to the FEN list, and return that.
        __temp_list__ = fen_string[-3:]
        fen_list.append([int(i) for i in __temp_list__.split(" ")])
        return fen_list
    def update_board(fen_list):
        """
        Updates the internal chess board using a FEN list
        """
        # Split the FEN list into different sections for readability
        fen_arrangement = fen_list[0]
        fen_nextMove = fen_list[1]
        fen_castling = fen_list[2]
        fen_enpassant = fen_list[3]
        fen_moveCount = fen_list[4]
        # For now, only the FEN arrangement and the next to move will be used - en passant, castling and move count will be established later
        # Go through every single character in fen_arrangement and interpret what to do!
        current_x, current_y = 0, 0
        for i in fen_arrangement:
            if str.isnumeric(i): # Check to see if the current character is a number
                if int(i) == 8: # Check to see if the 'number' is 8 (therefore there are no pieces on the line)
                    pass
                else:
                    current_x += int(i) - 1
            elif str.isascii(i) or str.isalpha(i):
                if i == "/":
                    current_y += 1
                    current_x = 0
                else:
                    chess_board_int[0][current_y].insert(current_x, i)
                    current_x += 1
        for rows in chess_board_int[0]: #~#~#
            __current_row__ = chess_board_int[0].index(rows)
            for v in range(0, 8):
                sq = rows[v]
                __current_sq__ = v
                if sq != 0: # Check to see if the current square isnt 0
                    ssize = 60
                    __current_coords__ = chess_board_int[1][__current_row__][__current_sq__]
                    image = pieces[chess_pieces[sq]]
                    ptx = ssize * __current_coords__[0]
                    pty = ssize * __current_coords__[1]
                    screen.blit(image, (ptx, pty))
                    pygame.display.flip()
                else:
                    pass
                
        pass
    def get_current_fen():
        """
        Get the current FEN notation of the board.
        """
    def evaluate(fen_string):
        import chess
        import chess.engine
        import time
        engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")
        board = chess.Board(fen_string)
        info = engine.analyse(board, chess.engine.Limit(time=1.0))
        __eval__ = info["score"].relative.score(mate_score=1000000) / 100
        engine.quit()
        return __eval__

def eval_window():
    import math
    def mround(x):
        if x - int(x) >= 0.5:
            return math.ceil(x)
        elif x - int(x) < 0.5:
            return math.floor(x)
        elif x - int(x) == 0.0:
            return x

    import tkinter, time
    ewin = tkinter.Tk()
    ewin.geometry("250x175")
    score = FEN.evaluate('r1bk3R/pp3Q2/8/2N1Pp2/6p1/6P1/PP3PP1/R3K3 b Q - 0 0')
    msg1 = f"The current evaluation is {score}"
    MAXIM = 10000
    if score > 0.0:
        if score < 3.0:
            msg2 = f"White is about {int(score)} points up"
        elif MAXIM - score <= 10:
            if score == MAXIM:
                msg2 = "White has mate!"
            else:
                msg2 = f"White has mate in approx {(MAXIM - mround(score))} moves"
        elif score >= 3.0:
            msg2 = f"White is winning, about {int(score)} points up"
    elif score < 0.0:
        if score > -3.0:
            msg2 = f"Black is about {int(-score)} points up"
        elif MAXIM + score <= 10:
           if score == MAXIM:
                msg2 = "Black has mate!"
           else:
                msg2 = f"Black has mate in approx {(MAXIM + mround(score))} moves"
        elif score <= -3.0:
            msg2 = f"Black is winning, about {int(-score)} points up"
    wscr = tkinter.Label(ewin, text=msg1, anchor="center")
    wevl = tkinter.Label(ewin, text=msg2, anchor="center")
    wscr.pack()
    wevl.pack()
    ewin.mainloop()
        

# Initialize Pygame
pygame.init()

# Set the size of the board
size = (480, 480)

# Create a window with the specified size
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Chess Board")

# Define required colours
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# Define the size of the squares
square_size = 60

# Create a chess board
chess_board = [[WHITE, BROWN] * 4, [BROWN, WHITE] * 4] * 4

# Loop through the rows and columns of the board
for row in range(8):
    for column in range(8):
        # Draw a square in the appropriate color
        pygame.draw.rect(screen, chess_board[row][column], [column * square_size, row * square_size, square_size, square_size])

# Update the display
pygame.display.flip()

fenList = FEN.get_fen_list("r1bk3R/pp3Q2/8/2N1Pp2/6p1/6P1/PP3PP1/R3K3 b Q - 0 0")
FEN.update_board(fenList)



# Update the display
pygame.display.flip()

# Pygame loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                eval_window()

# Exit pygame
pygame.quit()
