""" 
Responsible for storing all the information about the current state of the game and also for determining 
 valid move at current states and also keep a move log.

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
        self.moveFunctions = {
            'p': self.getPawnMoves, 
            'R': self.getRookMoves, 
            'N': self.getKnightMoves,
            'K': self.getKingMoves, 
            'B': self.getBishopMoves, 
            'Q': self.getQueenMoves
        }
        self.reviewIndex = -1  # -1 means no review mode, otherwise it's the index of the move being reviewed
        self.whiteToMove = True
        self.moveLog = []
        self.inCheck = False
        self.checks = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.lastMove = None  # To store the last move made
        self.pins = []
        # self.moveHistory = []
        self.enpassantPossible = () #coordinates for the square where en-passant capture is possible
        self.enPassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True , True , True , True) 
        self.CastleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
        def isCheckmate(self):
            if self.isInCheck():
                validMoves = self.getValidMoves()
                if len(validMoves) == 0:  # No legal moves available
                    return True
            return False
    def makeMove(self, move):  # Make the move that is passed as a parameter
        self.lastMove = move  # To store the last move made
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        # self.moveHistory.append(move)
        self.whiteToMove = not self.whiteToMove  # swap players

         # Check for checkmate or stalemate
        self.checkmate = self.isCheckmate()
        self.stalemate = self.isStalemate()

        # Update the King's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #Pawn promotion 
        if move.isPawnPromotion:
            # promotedPiece = input("Promoted to Q,R,B or N:")
            # self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
              self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #En passant   
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn


        #Update a enpassnat variable
        if move.pieceMoved[1] == 'p'  and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advancement
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol) # we can also use startCol because column isn't changing
        else:
            self.enpassantPossible = () # reset enpassant variable

        #castle moves
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # short(KingSide) castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # moves the rook
                self.board[move.endRow][move.endCol+1] = "--" # erase old rook
            else:  # long(QueenSide) castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # moves the rook
                self.board[move.endRow][move.endCol-2] = "--"

        self.enPassantPossibleLog.append(self.enpassantPossible)

        #Updating castling right - whenever it's a rook or a King move
        self.UpdateCastleRights(move)
        self.CastleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                                 self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    # def nextMove(self):
    #     if self.reviewIndex < len(self.moveHistory) - 1:
    #         self.reviewIndex += 1
    #         self.loadMove(self.reviewIndex)

    # def previousMove(self):
    #     if self.reviewIndex > 0:
    #         self.reviewIndex -= 1
    #         self.loadMove(self.reviewIndex)

    # def loadMove(self, index):
    #     # Reset the board
    #     self.board = self.createInitialBoard()
    #     # Replay all the moves up to the given index
    #     for i in range(index + 1):
    #         move = self.moveHistory[i]
    #         self.board[move.endRow][move.endCol] = move.pieceMoved
    #         self.board[move.startRow][move.startCol] = "--"
    # def createInitialBoard(self):
    #     return [
    #         ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    #         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    #         ["--", "--", "--", "--", "--", "--", "--", "--"],
    #         ["--", "--", "--", "--", "--", "--", "--", "--"],
    #         ["--", "--", "--", "--", "--", "--", "--", "--"],
    #         ["--", "--", "--", "--", "--", "--", "--", "--"],
    #         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    #         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    #     ]
    def undoMove(self):
        '''Undoing the last move'''
        if len(self.moveLog) != 0:  # make sure that there is a last move
            move = self.moveLog.pop()
            # move = self.moveHistory.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players back
            # Update the King's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #Undo enpassant move
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'  # leave lending square blank    
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enpassantPossible = self.enPassantPossibleLog[-1]

            #Undo castling Rights
            self.CastleRightsLog.pop() #get rid of the new castling rights from the move we are undoing  
            newRights = self.CastleRightsLog[-1] #set the new castling rights to the last one in the list
            self.currentCastlingRights = CastleRights(newRights.wks , newRights.bks, newRights.wqs, newRights.bqs)

            #undo castle moves
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # short(KingSide) castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] 
                    self.board[move.endRow][move.startCol-1] = '--' 
                else:  # long(QueenSide) castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] 
                    self.board[move.endRow][move.endCol+1] = '--' 

            self.checkmate = False
            self.stalemate = False

    def UpdateCastleRights(self, move): 
        '''Update the Castle Rights given the move'''
        if move.pieceMoved == 'wk' :
            self.currentCastlingRights.wks = False 
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
              if move.startCol == 0: #left rook  
                self.currentCastlingRights.wqs = False
              elif move.startCol == 7: #right rook  
                  self.currentCastlingRights.wks = False  
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
              if move.startCol == 0: #left rook  
                self.currentCastlingRights.bqs = False
              elif move.startCol == 7: #right rook
                  self.currentCastlingRights.bks = False

        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:     
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':               
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:     
                    self.currentCastlingRights.bks = False             


    def getValidMoves(self):
        # for log in self.CastleRightsLog:
        #     print(log.wks, log.bks , log.wqs, log.bqs)
        # print()
        tempEnPassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks , self.currentCastlingRights.bks ,
                                        self.currentCastlingRights.wqs, self.currentCastlingRights.bqs) #copy the current Castling Rights
        moves = []
        if self.whiteToMove:
            self.getCastleMove(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMove(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]      
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, move King or block check
                moves = self.getAllPossibleMoves()
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # Squares that piece can move to
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare == (checkRow, checkCol):  # once you get to piece and checks
                            break
                # Get rid of any moves that don't block check or move King
                for i in range(len(moves) - 1, -1, -1): #going backwards because we are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K':  # move doesn't move King so it must block or capture
                        if (moves[i].endRow, moves[i].endCol) not in validSquares:
                            moves.remove(moves[i])
            else:  # double check, King has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        #    new_moves = self.getAllPossibleMoves()
        #    if len(moves) > 0:
        #         moves.extend(new_moves)
        #    else:
        #         moves = new_moves


        self.enpassantPossible = tempEnPassantPossible
        self.currentCastleRights = tempCastleRights
        return moves

    def isCheckmate(self):
        if self.isInCheck():
            validMoves = self.getValidMoves()
            if len(validMoves) == 0:  # No legal moves available
                return True
        return False

    def isStalemate(self):
        if not self.isInCheck():
            validMoves = self.getValidMoves()
            if len(validMoves) == 0:  # No legal moves available
                return True
        return False

    def isInCheck(self):
        '''Determines if the current player is in check'''
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        

    def squareUnderAttack(self, r, c):
        '''Determines if the enemy is attacking the square (r, c)'''
        self.whiteToMove = not self.whiteToMove  # switch to opponent's perspective
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # Square is under attack
                return True
        return False

    def getAllPossibleMoves(self):  # all moves without considering checks
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # Calls the appropriate move functions based on piece types
        return moves

    def getPawnMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            kingRow , kingCol = self.whiteKingLocation
            enemyColor = 'b'
        else:            
            kingRow , kingCol = self.blackKingLocation
            enemyColor = 'w'


        '''Get all the pawn moves for the pawn located at row, col and add these moves to the list'''
        if self.whiteToMove:  # white pawn moves
            if self.board[r-1][c] == "--":  # 1 square pawn advance
              if not piecePinned or pinDirection == (-1,0):  
                moves.append(Move((r, c), (r-1, c), self.board,self))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board,self))
                    
            # Captures
            if c-1 >= 0:  # captures to the left
                if self.board[r-1][c-1][0] == 'b':  # enemy piece to capture
                  if not piecePinned or pinDirection == (-1,-1) :  
                    moves.append(Move((r, c), (r-1, c-1), self.board,self))
                elif (r-1,c-1) == self.enpassantPossible :  
                    moves.append(Move((r, c), (r-1, c-1), self.board,self , isEnPassantMove=True))   

            if c+1 <= 7:  # captures to the right
                if self.board[r-1][c+1][0] == 'b':  # enemy piece to capture
                  if not piecePinned or pinDirection == (-1,1) :    
                    moves.append(Move((r, c), (r-1, c+1), self.board,self))
                elif (r-1,c+1) == self.enpassantPossible :  
                    moves.append(Move((r, c), (r-1, c+1), self.board,self , isEnPassantMove=True))   

        else:  # black pawn moves
            if self.board[r+1][c] == "--":  # 1 square pawn advance
              if not piecePinned or pinDirection == (1,0) :   
                moves.append(Move((r, c), (r+1, c), self.board,self))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board,self))
                    
            # Captures
            if c-1 >= 0:  # left piece to capture
                if self.board[r+1][c-1][0] == 'w':  # enemy piece to capture
                  if not piecePinned or pinDirection == (1,-1) :  
                    moves.append(Move((r, c), (r+1, c-1), self.board,self))
                elif (r+1,c-1) == self.enpassantPossible :  
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: # king is left of the pawn
                            # inside between the king and the pawn ; outside => range between pawn border
                            insideRange = range(kingCol + 1 , c-1)
                            outsideRange = range(c+1 , 8)
                        else:
                            insideRange = range(kingCol -1 , c , -1)
                            outsideRange = range(c-2 , -1 , -1)
                        for i in insideRange:
                            if self.board[r][i] != '--': #some other piece beside en-passnat pawn block
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i] 
                            if square[0]  == enemyColor and (square[1] == 'R' or square[1] == 'Q'): #attacking Piece
                                attackingPiece = True
                            elif square != '--' :
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:               
                     moves.append(Move((r, c), (r+1, c-1), self.board ,self, isEnPassantMove=True))       

            if c+1 <= 7:  # right piece to capture
                if self.board[r+1][c+1][0] == 'w':  # enemy piece to capture
                  if not piecePinned or pinDirection == (1,1) :  
                    moves.append(Move((r, c), (r+1, c+1), self.board,self))
                elif (r+1,c+1) == self.enpassantPossible :  
                     attackingPiece = blockingPiece = False
                     if kingRow == r:
                        if kingCol < c: # king is left of the pawn
                            # inside between the king and the pawn ; outside => range between pawn border
                            insideRange = range(kingCol + 1 , c)
                            outsideRange = range(c+2 , 8)
                        else:
                            insideRange = range(kingCol -1 , c + 1, -1)
                            outsideRange = range(c-1 , -1 , -1)
                        for i in insideRange:
                            if self.board[r][i] != '--': #some other piece beside en-passnat pawn block
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i] 
                            if square[0]  == enemyColor and (square[1] == 'R' or square[1] == 'Q'): #attacking Piece
                                attackingPiece = True
                            elif square != '--' :
                                blockingPiece = True
                     if not attackingPiece or blockingPiece:    
                      moves.append(Move((r, c), (r+1, c+1), self.board ,self, isEnPassantMove=True))    



    def getRookMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #can't remove queen from pin on rook moves , only removes it on bishop moves
                 self.pins.remove(self.pins[i])
                break


        '''Get rook moves given starting row and column , append the new moves to the list 'moves' '''

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Make sure move is on board
                  if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1])  :
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space is valid
                        moves.append(Move((r, c), (endRow, endCol), self.board,self))
                    elif endPiece[0] == enemyColor:  # Enemy piece valid, and stop checking in this direction
                        moves.append(Move((r, c), (endRow, endCol), self.board,self))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break

    def getKnightMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1, -1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        '''Get Knight moves given starting row and column , append the moves to the list 'moves' '''
        knightMoves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
              if not piecePinned:  
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy)
                    moves.append(Move((r, c), (endRow, endCol), self.board,self))


    def getBishopMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1, -1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        '''Get Bishop moves given starting row and column , append the moves to the list 'moves' '''
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 diagonal directions
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Bishop can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Make sure move is on board
                  if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1]) :
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space is valid
                        moves.append(Move((r, c), (endRow, endCol), self.board,self))
                    elif endPiece[0] == enemyColor:  # Enemy piece valid, and stop checking in this direction
                        moves.append(Move((r, c), (endRow, endCol), self.board,self))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)  # Queen moves like a Rook
        self.getBishopMoves(r, c, moves)  # And Queen moves like a Bishop

    def getKingMoves(self, r, c, moves):
        '''Get King moves given starting row and column , append the moves to the list 'moves' '''

        rowMoves = (-1,-1,-1, 0,0, 1,1,1)
        colMoves = (-1, 0, 1,-1,1,-1,0,1)
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy)
                    #place King for end squares and check for checks.
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow , endCol)
                    else:
                        self.blackKingLocation = (endRow , endCol)
                    inCheck , pins , checks = self.checkForPinsAndChecks()        
                    if not inCheck:
                       moves.append(Move((r, c), (endRow, endCol), self.board,self))
                    # place King back on original locations   
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

        # print("Checking for castling moves...")
        # self.getCastleMove(r, c, moves)       

    def getCastleMove(self, r, c, moves):
        '''Generate all valid moves for the King at (r , c) and add them to the list of moves'''                        
        if self.squareUnderAttack(r, c):
            return #can't castle while in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)
    
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" and \
             not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board,self , isCastleMove=True))
                


    def getQueenSideCastleMoves(self, r, c , moves ):    
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == '--' and \
         not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2) :
                moves.append(Move((r, c), (r, c-2), self.board,self , isCastleMove=True)) 
  



    def checkForPinsAndChecks(self):
        '''returns if the player is in check , a list of pins , and a list of checks'''
        pins = []  # squares where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow, startCol = self.whiteKingLocation
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow, startCol = self.blackKingLocation

        # Check outward from the king for pins and checks, keep track of pins
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():  # first allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or (4 <= j <= 7 and pieceType == 'B') or \
                            (i == 1 and pieceType == 'p' and (
                            (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            if possiblePin == ():  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off board

                # Check for knight checks
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks



class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks  # White short-sacrifice castling 
        self.bks = bks  # Black short-sacrifice castling
        self.wqs = wqs  # White long-sacrifice castling
        self.bqs = bqs  # Black long-sacrifice castling

class Move:
    # Map keys to ranks and files for chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board,game_state, isEnPassantMove = False ,  isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        #En-passant 
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #Castle Moves
        self.isCastleMove = isCastleMove
        # self.checkmate = self.isCheckmate()
        self.game_state = game_state
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # def isCheckmate(self):
    #         if self.isInCheck():
    #             validMoves = self.getValidMoves()
    #             if len(validMoves) == 0:  # No legal moves available
    #                 return True
    #         return False    

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # def getChessNotation(self):
    #     # You can add to make this like real chess notation
  
    #     return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getChessNotation(self):
    # Handle castling

    
        if self.pieceMoved == 'wK' and self.startCol == 4:
            if self.endCol == 6:
                return "O-O"  # Kingside castling
            elif self.endCol == 2:
                return "O-O-O"  # Queenside castling

        # Handle pawn promotion
        if self.pieceMoved[1] == 'p' and (self.endRow == 0 or self.endRow == 7):
            return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol) + '=Q'  # Assuming promotion to Queen
            # moveString = 'x' + self.getRankFile(self.endRow, self.endCol) + '=Q'

        moveString = ''

        # Add piece notation (e.g., N for Knight, B for Bishop)
        piece_type = self.pieceMoved[1]
        if piece_type != 'p':  # Don't add a letter for pawns
            moveString += piece_type.upper()

        # Handle captures
        if self.pieceCaptured != '--':
            if piece_type == 'p':  # For pawns, include the file of the starting square
                moveString += self.getRankFile(self.startRow, self.startCol)[0]
            moveString += 'x'  # x denotes a capture

        # Add the destination square
        moveString += self.getRankFile(self.endRow, self.endCol)

        #Handle check and checkmate
        if self.game_state.isCheckmate():
            moveString += '#'
        elif self.game_state.isInCheck():
            moveString += '+'

        return moveString

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # def isCheckmate(self):
    #         if self.isInCheck():
    #             validMoves = self.getValidMoves()
    #             if len(validMoves) == 0:  # No legal moves available
    #                 return True
    #         return False
    
    # def isInCheck(self):
    #     '''Determines if the current player is in check'''
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        