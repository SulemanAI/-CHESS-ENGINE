# import random

# pieceScore = {
#     "K": 0,
#     "Q": 9,
#     "R": 5,
#     "N": 3,
#     "B": 3,
#     "p": 1,
# }

# knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],
#                [1, 2, 3, 3, 3, 3, 2, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 3, 3, 3, 2, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],
#                [1, 1, 1, 1, 1, 1, 1, 1]]

# bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
#                 [3, 4, 3, 2, 2, 3, 4, 3],
#                 [2, 3, 4, 3, 3, 4, 3, 2],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [2, 3, 4, 3, 3, 4, 3, 2],
#                 [3, 4, 3, 2, 2, 3, 4, 3],
#                 [4, 3, 2, 1, 1, 2, 3, 4]]

# queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
#                [1, 2, 3, 3, 3, 1, 1, 1],
#                [1, 4, 3, 3, 3, 4, 2, 1],
#                [1, 2, 3, 3, 3, 2, 2, 1],
#                [1, 2, 3, 3, 3, 2, 2, 1],
#                [1, 4, 3, 3, 3, 4, 2, 1],
#                [1, 1, 2, 3, 3, 1, 1, 1],
#                [1, 1, 1, 3, 1, 1, 1, 1]]
  
# #probably better to try to place rooks on open files , or on same file as other rook/queen
# rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
#               [4, 4, 4, 4, 4, 4, 4, 4],
#               [1, 1, 2, 3, 3, 2, 1, 1],
#               [1, 2, 3, 4, 4, 3, 2, 1],
#               [1, 2, 3, 4, 4, 3, 2, 1],
#               [1, 1, 2, 2, 2, 2, 1, 1],
#               [4, 4, 4, 4, 4, 4, 4, 4],
#               [4, 3, 4, 4, 4, 4, 3, 4]]

# whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
#                    [8, 8, 8, 8, 8, 8, 8, 8],
#                    [5, 6, 6, 7, 7, 6, 6, 5],
#                    [2, 3, 3, 5, 5, 3, 3, 2],
#                    [1, 2, 3, 4, 4, 3, 2, 1],
#                    [1, 1, 2, 3, 3, 2, 1, 1],
#                    [1, 1, 1, 0, 0, 1, 1, 1],
#                    [0, 0, 0, 0, 0, 0, 0, 0]]

# blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
#                    [1, 1, 1, 0, 0, 1, 1, 1],
#                    [1, 1, 2, 3, 3, 2, 1, 1],
#                    [1, 2, 3, 4, 4, 3, 2, 1],
#                    [2, 3, 3, 5, 5, 3, 3, 2],
#                    [5, 6, 6, 7, 7, 6, 6, 5],
#                    [8, 8, 8, 8, 8, 8, 8, 8],
#                    [8, 8, 8, 8, 8, 8, 8, 8]]


# piecePositionScores = {"N":knightScores , "Q":queenScores , "B" : bishopScores , "R" : rookScores , "bp" : blackPawnScores , "wp" : whitePawnScores}

# CHECKMATE = 1000
# STALEMATE = 0
# DEPTH = 3  # Increased depth for better decision-making

# def findRandomMoves(validMoves):
#     '''Picks and returns a random move'''
#     return validMoves[random.randint(0, len(validMoves) - 1)]

# def findBestMove(gs, validMoves, returnQueue):
#     '''Helper method to make the first call to Minimax algorithm with Alpha-Beta Pruning'''
#     global nextMove  
#     nextMove = None
#     random.shuffle(validMoves)  # Slight randomization to vary AI behavior
#     findMoveAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, gs.whiteToMove)
#     returnQueue.put( nextMove )

# def findMoveAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
#     global nextMove
#     if depth == 0 or gs.checkmate or gs.stalemate:
#         return scoreBoard(gs)

#     if whiteToMove:
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#                     print(move , score)
#             gs.undoMove()
#             alpha = max(alpha, score)
#             if beta <= alpha:
#                 break  # Beta cutoff
#         return maxScore

#     else:  # Black to move
#         minScore = CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)
#             if score < minScore:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#             beta = min(beta, score)
#             if beta <= alpha:
#                 break  # Alpha cutoff
#         return minScore

# def scoreBoard(gs):
#     # A positive score is good for white , a negative score is bad for black.
#     if gs.checkmate:
#         if gs.whiteToMove:
#           return -CHECKMATE #black wins
#         else:
#             return CHECKMATE #white wins     
#     elif gs.stalemate:
#         return STALEMATE 

#     score = 0
#     for row in range(len(gs.board)):
#         for col in range(len(gs.board[row])):
#             square = gs.board[row][col]
#             if square != '--':
#                 # Score is positionally
#                 piecePositionScore = 0
#                 if square[1] != "K": #no position table for King
#                     if square[1] == 'p' : #for pawns
#                         piecePositionScore = piecePositionScores[square][row][col]  
#                     else: #for other pieces
#                         piecePositionScore = piecePositionScores[square[1]][row][col]

#                 if square[0] == "w":
#                     score += pieceScore[square[1]] + piecePositionScore * .1
#                 elif square[0] == "b":      
#                     score -= pieceScore[square[1]] + piecePositionScore * .1

#     return score 

# def scoreMaterial(board):
#     '''Score the board based on material alone.'''
#     score = 0
#     for row in board:
#         for square in row:
#             if square != "--":  # Skip empty squares
#                 if square[0] == "w":
#                     score += pieceScore[square[1]]
#                 elif square[0] == "b":
#                     score -= pieceScore[square[1]]
#     return score

# ''''''
import random 

pieceScore = {
    "K" : 0 ,  
    "Q" : 10 ,
    "R" : 5 ,
    "N" : 3 ,
    "B" : 3 ,
    "p" : 1 ,
}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]


bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]
  
#probably better to try to place rooks on open files , or on same file as other rook/queen
rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N":knightScores , "Q":queenScores , "B" : bishopScores , "R" : rookScores , "bp" : blackPawnScores , "wp" : whitePawnScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMoves(validMoves):    
   '''Picks and find a random moves'''
   return validMoves[random.randint(0, len(validMoves)-1)] 


def findBestMovesMinMaxNoRecursion(gs, validMoves):
    '''Find the best move , min max without recursion.'''

    turnMultiplier = 1 if gs.whiteToMove else -1 
    opponentMinMaxScore = CHECKMATE    
    bestPlayerMove = None  # Initialize best move to None
    random.shuffle(validMoves)
    
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE  
        
        if gs.stalemate:
          opponentMaxScore = STALEMATE
        elif gs.checkmate:
          opponentMaxScore = -CHECKMATE
        else:
          opponentMaxScore = -CHECKMATE

          for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            gs.getValidMoves()
            
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:        
                score = -turnMultiplier * scoreMaterial(gs.board)
                
            if score > opponentMaxScore:
                opponentMaxScore = score
                
            gs.undoMove()    
        
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
            
        gs.undoMove()    
    
    return bestPlayerMove

def findBestMove(gs , validMoves , returnQueue):
    ''''Helper method to make first recursive call to findBestMove'''
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    # counter = 0  
    # findMoveMinMax(gs, validMoves, DEPTH , gs.whiteToMove)

    # findMoveNegaMax(gs, validMoves, DEPTH,  1 if gs.whiteToMove else -1)

    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE , CHECKMATE, 1 if gs.whiteToMove else -1)
    # print(counter)
    returnQueue.put( nextMove )

def findMoveMinMax(gs , validMoves , depth , whiteToMove):
    global nextMove 
    if depth == 0: #or (gs.stalemate or gs.checkmate):
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)

            nextMoves = gs.getValidMoves() 
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()    
        return maxScore
        
    else:   
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True) 
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()    
        return minScore



def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove 
    # global counter
    # counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore    

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth,alpha ,beta ,turnMultiplier):
    global nextMove , counter
    # counter += 1  
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)


    #move ordering - implement later 
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1,-beta , -alpha , -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()

        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >=  beta:
            break    

    return maxScore    



def scoreBoard(gs):
    # A positive score is good for white , a negative score is bad for black.
    if gs.checkmate:
        if gs.whiteToMove:
          return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins     
    elif gs.stalemate:
        return STALEMATE 

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                # Score is positionally
                piecePositionScore = 0
                if square[1] != "K": #no position table for King
                    if square[1] == 'p' : #for pawns
                        piecePositionScore = piecePositionScores[square][row][col]  
                    else: #for other pieces
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == "w":
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == "b":      
                    score -= pieceScore[square[1]] + piecePositionScore * .1

    return score 
 

def scoreMaterial(board):
    '''Score the board based on materials.'''
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":      
                score -= pieceScore[square[1]]

    return score            
