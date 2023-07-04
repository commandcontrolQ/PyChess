
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
        self.whiteMove = True
        self.log = []
        
 
"""

Below this class is the main code. It is responsible for handling user input,
as well as displaying the current GameState object.
 
"""
 
import pygame
# from chess import ChessEngine
 
WIDTH, HEIGHT = 512, 512
DMN = 8 # Dimension of the chess board
SSIZE = HEIGHT // DMN
FPS = 15
IMAGES = {}

# Initialize images. This will be called once in the main loop.
def loadImages():
    pieces = ["wp","wR","wN","wB","wQ","wK","bp","bR","bN","bB","bQ","bK"]
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load("images/%s.png" % p), (SSIZE, SSIZE))

# Main function - handles user input and updating graphics

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    state = GameState()
    loadImages() # run this once, before the loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
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
    for ROW in range(DMN):
        for COL in range(DMN):
            color = colors[((ROW+COL) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(COL * SSIZE, ROW * SSIZE, SSIZE, SSIZE))



def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current GameState.board
    """
    for ROW in range(DMN):
        for COL in range(DMN):
            piece = board[ROW][COL]
            if piece != "--": # Piece is not empty!
                screen.blit(IMAGES[piece], pygame.Rect(COL * SSIZE, ROW * SSIZE, SSIZE, SSIZE))



if __name__ == "__main__":
    main()










