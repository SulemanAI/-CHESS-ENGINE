 # Main Driver File . Responsible for User Input and current GameState

import pygame as p
# import chess
import ChessEngine , ChessAI
import pyttsx3
import threading
import sys
from multiprocessing import Process,Queue

print("Running menu")
# from menu import bot
if "menu_shown" not in sys.argv:
    sys.argv.append("menu_shown")
    from menu import bot  # Import menu only if it hasn't been shown                                                


BOARD_WIDTH = BOARD_HEIGHT = 512
MoveLogPanel_WIDTH = 275

MoveLogPanel_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Initialize a global dictionary of images

# currentMove = 0
# moveHistory = []
#bot = 0


# BUTTON_COLOR = (70, 70, 70)
# TEXT_COLOR = (255, 255, 255)

# buttons = [
#         (p.Rect(BOARD_WIDTH - 200, BOARD_HEIGHT + 10, 80, 40), "Previous"),
#         (p.Rect(BOARD_WIDTH - 100, BOARD_HEIGHT + 10, 80, 40), "Next")
#     ]


def LoadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:  
        IMAGES[piece] = p.transform.scale(p.image.load(piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Main driver for our code and responsible for user input and updating the graphics

def flipBoard(board):
    return [row[::-1] for row in board[::-1]]  # Reverse both rows and columns

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def displayStalemateText(screen):
    drawEndGameText(screen, "StaleMate")

def displayCheckmateText(screen):
    drawEndGameText(screen, "CheckMate")

# def displayCheckText(screen):
#     drawEndGameText(screen, "Check")

def draw_labels(screen):   
    font = p.font.SysFont('Courier New', 15)
    color = p.Color('black')
    colors = p.Color('Navy Blue')
    for i in range(8):
        # Draw file labels
        label = font.render(chr(97 + i), True, colors)
        screen.blit(label, (i * SQ_SIZE + SQ_SIZE // 2 - label.get_width() // 2, BOARD_HEIGHT - label.get_height()))

        # Draw rank labels
        label = font.render(str(8 - i), True, color)
        screen.blit(label, (0 , i * SQ_SIZE + SQ_SIZE // 2 - label.get_height() // 2))

# def drawTextOnButton(screen, text, buttonRect):
#     font = p.font.SysFont('Arial', 24)
#     textSurf = font.render(text, True, TEXT_COLOR)
#     textRect = textSurf.get_rect(center=buttonRect.center)
#     screen.blit(textSurf, textRect)

# # Draw buttons
# def drawButtons(screen, buttons):
#     for button in buttons:
#         p.draw.rect(screen, BUTTON_COLOR, button)
#         drawTextOnButton(screen, buttons[button], button)

def main():
    print("Running Main")
    p.init()

    p.font.init()  # Explicitly initialize the font module
    screen = p.display.set_mode((BOARD_WIDTH + MoveLogPanel_WIDTH, BOARD_HEIGHT))
    p.display.set_caption("Chess Engine made by Muhammad Suleman")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont  = p.font.SysFont("Arial", 15, False , False)
    gs = ChessEngine.GameState()
    print(gs.board)
    validMoves = gs.getValidMoves() 
    moveMade = False #flag variable for when a move is made
    # animate = False #flag variable for when we should animate a move
    LoadImages()  # Load images once before the while loop


    running = True 
    sqSelected = () # no square is selected initially , keep track of the last click of the user (tuple: row , col) 
    playerClicks = [] # keep track of player clicks (two tuple: [(6,4),(4,4)])
    gameOver = False
    # speak_thread = threading.Thread(target=speak, args=("Welcome to the Chess Engine made by Muhammad Suleman",))
    # speak_thread.start()

    playerOne = True #if human is playing so it is true , else => AI == False
    playerTwo = False #Same as above but for black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne ) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # mouse handler    
              if not gameOver:  
                location = p.mouse.get_pos() #(x,y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                # if e.key == p.K_LEFT and currentMove > 0:
                #     currentMove -= 1
                #     gs.board.pop()
                # if e.key == p.K_RIGHT and currentMove < len(moveHistory):
                #     gs.board.push(moveHistory[currentMove])
                #     currentMove += 1 



                
                # # Adjust coordinates if it's Black's turn and the board is flipped
                if not gs.whiteToMove:
                    row, col = DIMENSION - 1 - row, DIMENSION - 1 - col

                if sqSelected == (row, col) or col >= 8:  # If the user clicked the same square again, deselect it or user clicked move log
                    sqSelected = () #deselect the selected square
                    playerClicks = [] #clear the player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append((sqSelected)) # append for both i.e. 1st and 2nd click
                if len(playerClicks) == 2 and humanTurn: # after 2nd click
                     move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board,gs)
                    #  print(move.getChessNotation())
                     for i in range(len(validMoves)):     
                        if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  
                                moveMade = True
                                # animate = True
                                sqSelected = () #reset user click
                                playerClicks = [] # clear the player clicks
                     if not moveMade:
                      playerClicks = [sqSelected] 

            elif e.type == p.KEYDOWN:  #key handler  
                if e.key == p.K_z:  # undo when the last move 'z' is pressed 
                    gs.undoMove()
                    moveMade = True
                    # animate = False
                    lastMove = gs.moveLog[-1] if len(gs.moveLog) > 0 else None  # Update lastMove after undo
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                        moveUndone = True

                if e.key == p.K_r: # reset the board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    # animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                        moveUndone = True


        #AI move finder
        if not gameOver and not humanTurn and not moveUndone:
           if not AIThinking:
                AIThinking = True
                print("thinking...")
                returnQueue = Queue() #used to pass data between threads
                moveFinderProcess = Process(target=ChessAI.findBestMove , args = (gs, validMoves , returnQueue))
                moveFinderProcess.start() #call findBestMove (gs, validMoves)
                # AImoves = ChessAI.findBestMove(gs, validMoves)
           if not moveFinderProcess.is_alive() :
                print("Done thinking")
                AImoves = returnQueue.get()
                if AImoves is None:
                    AImoves = ChessAI.findRandomMoves(validMoves)
                # if AImoves is not None:    
                gs.makeMove(AImoves)
                # gs.makeMove(AImove)
                moveMade = True
                p.time.delay(500)
                AIThinking = False

        # if gs.checkmate or gs.stalemate:
        #     gameOver = True
        #     if gs.checkmate:
        #         print("Checkmate!")
        #         speak_thread = threading.Thread(target=speak, args=("Checkmate!",))
        #         speak_thread.start()
        #     else:
        #         print("Stalemate!")
        #         speak_thread = threading.Thread(target=speak, args=("Stalemate!",))
        #         speak_thread.start()
      
      
        if moveMade:
            # if animate:
             # animateMove(gs.moveLog[-1], screen , gs.board , clock)
            validMoves = gs.getValidMoves()  
            # p.time.delay(300)   
            moveMade = False
            moveUndone = False
            # animate  = False    
            
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)      

        # if gs.isInCheck:
        #     drawText(screen, "Check")
        #     # speak("Check")

        # if gs.isInCheck:
        #     speak_thread = threading.Thread(target=speak, args=("Check",))
        #     speak_thread.start()
            # checkThread = threading.Thread(target=displayCheckText, args=(screen,))
            # checkThread.start()
            # gs.isInCheck = False
            

        if gs.checkmate: 
            gameOver = True
            # moveString += '#'

            # drawEndGameText(screen , "Checkmate")

            speak_thread = threading.Thread(target=speak, args=("Checkmate",))
            speak_thread.start()

            # checkMateThread = threading.Thread(target=displayStalemateText, args=(screen,))
            # checkMateThread.start()
            gs.checkmate = False

        if gs.stalemate: 
            gameOver = True
            # print("Stalemate detected")  # Check if this line is executed

            # drawEndGameText(screen , "StaleMate")
            # staleMateThread = threading.Thread(target=displayStalemateText, args=(screen,))
            # staleMateThread.start()

            speak_thread = threading.Thread(target=speak, args=("Stalemate",))
            speak_thread.start()

            gs.stalemate = False
                             
        clock.tick(MAX_FPS)
        draw_labels(screen)
        p.display.flip()

        if bot == 1:
            playerOne = True
            playerTwo = True
            drawGameState(screen, gs , validMoves , sqSelected,moveLogFont)
        if bot == 2:
            playerTwo = False
            playerOne = True
            drawGameState(screen, gs , validMoves , sqSelected,moveLogFont)          

            # if not gs.whiteToMove:  # Flip the board if it's Black's turn
            #     print(bot)
            #     flipped_board = flipBoard(gs.board)
            #     drawBoard(screen)
            #     drawPieces(screen, flipped_board)
            #     highlightLastMove(screen, gs.lastMove)
            #     highlightsSquares(screen, gs, validMoves , sqSelected)
            # else:    

    # else:  # Draw normally if it's White's turn
        # drawBoard(screen)
        # drawPieces(screen, gs.board)


def drawGameState(screen, gs , validMoves , sqSelected, moveLogFont):
    if not gs.whiteToMove:  # Flip the board if it's Black's turn        
        drawBoard(screen)
        if bot != 1:
            highlightLastMove(screen, gs.lastMove)
            highlightsSquares(screen, gs, validMoves , sqSelected)
        if bot != 2:
            flipped_board = flipBoard(gs.board)
            drawPieces(screen, flipped_board)
        else:
            drawPieces(screen, gs.board)
        drawMoveLog(screen, gs , moveLogFont)

    else:  # Draw normally if it's White's turn
        # flipped_board = flipBoard(gs.board)
        drawBoard(screen)
        # drawButtons(screen, buttons)
        if bot != 1:       
            highlightsSquares(screen, gs, validMoves , sqSelected)
            highlightLastMove(screen, gs.lastMove)
        drawPieces(screen, gs.board)
        drawMoveLog(screen, gs , moveLogFont)


def drawBoard(screen):
    ''' Draw the squares on the board. The top-left square is always light. '''
    global colors
    colors = [p.Color(240, 217, 181), p.Color(181, 136, 99)]  # Light brown and dark brown
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            x = c * SQ_SIZE
            y = r * SQ_SIZE
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, (x, y, SQ_SIZE, SQ_SIZE))

def highlightsSquares(screen, gs, validMoves,sqSelected):
    '''Highlights square selected and moves for piece selected'''
    if sqSelected != () :
        r , c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #Sqselected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE , SQ_SIZE))
            s.set_alpha(100) # transparency value == 0 means transparent and at 255 it is opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            # s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    # screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                    # Draw a dot at the center of the square
                    center = (move.endCol * SQ_SIZE + SQ_SIZE // 2, move.endRow * SQ_SIZE + SQ_SIZE // 2)
                    p.draw.circle(screen, p.Color('grey'), center, 10)  # 10 is the radius of the dot
        # p.display.update()  # Ensure the display updates to reflect changes
  


# def update_clock(time, dt):
#     # Subtract delta time from the current time
#     time -= dt
#     # Convert seconds to minutes and seconds
#     minutes = int(time / 60)
#     seconds = int(time % 60)
#     # Convert minutes to hours and minutes
#     hours = int(minutes / 60)
#     minutes %= 60
#     # Format the time string
#     time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
#     return time_str

def highlightLastMove(screen, lastMove):
    if lastMove is not None:
        # Highlight the start square
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # Transparency level
        s.fill(p.Color('yellow'))  # Color for the highlight
        screen.blit(s, (lastMove.startCol * SQ_SIZE, lastMove.startRow * SQ_SIZE))
        
        # Highlight the end square
        screen.blit(s, (lastMove.endCol * SQ_SIZE, lastMove.endRow * SQ_SIZE))
    # gs.undoMove(lastMove)


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # blit() is used to draw the image at the specified position.

def drawMoveLog(screen , gs , font):
    '''Draws the move log '''
    moveLogRect = p.Rect(BOARD_WIDTH ,0 , MoveLogPanel_WIDTH , MoveLogPanel_HEIGHT)
    p.draw.rect(screen, p.Color('black') ,moveLogRect)
    moveLog = gs.moveLog
    moveTexts = [] 
    for i in range(0 , len(moveLog) , 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + "  "
        if i + 1 < len(moveLog): #make sure that black made a move
            moveString += moveLog[i + 1].getChessNotation() + "   "
        moveTexts.append(moveString)  
    movesPerRow = 3      
    padding = 5
    textY = padding
    lineSpacing = 2  # spacing between move texts in the move log panel
    for i in range(0 , len(moveTexts) , movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j] 





 


        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject , textLocation)
        textY += textObject.get_height() + lineSpacing 

# def animateMove(move,screen, board, clock):
#     global colors
#     dR = move.endRow - move.startRow
#     dC = move.endCol - move.startCol
#     framesPerSquare = 10 #frames to move one square 
#     framesCount = (abs(dR) + abs(dC)) * framesPerSquare

#     for frame in range(framesCount + 1):
#         r,c = (move.startRow + dR*frame/framesCount, move.startCol + dC*frame/framesCount)

#         drawBoard(screen)
#         drawPieces(screen, board)

#         #erase the piece moved from its ending square   

#         color = colors[(move.endRow + move.endCol) % 2]
#         endSquare = p.Rect(move.endCol*SQ_SIZE , move.endRow*SQ_SIZE + SQ_SIZE , SQ_SIZE , SQ_SIZE)
#         p.draw.rect(screen, color ,endSquare)

#         #draw captured piece back onto rectangle
#         if move.pieceCaptured != '--':
#             screen.blit(IMAGES[move.pieceCaptured], endSquare)

#         # draw moving piece
#         screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE , r*SQ_SIZE , SQ_SIZE , SQ_SIZE))
#         p.display.flip()
#         clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 32, True , False)
    textObject = font.render(text, 0, p.Color('red'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH , BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2 , BOARD_HEIGHT / 2 - textObject.get_height()/2)
    screen.blit(textObject , textLocation)
    textObject = font.render(text, 0, p.Color('grey'))
    screen.blit(textObject , textLocation.move(2,2))


if __name__ == "__main__":   # Ensure the code runs only when this file is executed directly, not when imported
    main()
