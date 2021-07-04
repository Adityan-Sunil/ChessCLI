import chess
import chess.engine
import chess.pgn as PGN
from os import system
import argparse

def resetBoard():
    board.reset()

board = chess.Board()
def pvp_game():
    resetBoard()
    matchOver = False
    print(board)
    player = ["White", "Black"]
    playerind = 0
    while(True):
        inValid = True 
        while inValid:
            try:
                if board.can_claim_draw():
                    move = "draw"
                else:
                    print(player[playerind]+" move: ")
                    move = input()
                if move == "resign" or move == "draw":
                    if move == "resign":
                        print(player[playerind]+" "+ move)
                    else:
                        print("\nMatch draw")
                    matchOver = True
                    break
                _ = board.parse_san(move)
                inValid = False
            except:
                print("\nIllegal Move")  
        if matchOver:
            break
        board.push_san(move)
        system('cls')
        print(board)
        playerind = (playerind + 1 )% 2
        
        if board.is_game_over():
            print("Outcome: "+ board.outcome().result());
            break



#Game pgn taken from chessgames.com
def pgn_game(path):
    resetBoard()
    with open(path) as pgn:
        first_game = PGN.read_game(pgn)
    moves = list(first_game.mainline_moves())
    for move in moves: 
        print("White Player:",first_game.headers["White"])
        print("Black Player:",first_game.headers["Black"])
        print("\n")
        board.push(move)
        print(board)
        inp = input()
        if inp == "end":
            break
        system('cls')
    print("\nResult:",first_game.headers["Result"])

def getMove(board):
    inValid = True
    while inValid:
        user_result = input("\nYour Move: ")
        if user_result == "resign":
            print("Player Resigned")
            return False
        try:
            board.parse_san(user_result)
            inValid = False
        except:
            print("Invalid Move")
    board.push_san(user_result)
    return True

#Vs Computer
def pve_game():
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    board = chess.Board()
    user = input("Choose your Color (b/w)")
    if user not in ["b", "w"]:
        print("Computer wins")
    else:
        if user == "w":
            getMove(board)
    while not board.is_game_over():
        system('cls')
        computer_result = engine.play(board, chess.engine.Limit(time=0.05))
        board.push(computer_result.move)
        print(board)
        result = getMove(board)
        if(not result):
            break;
        system('cls')
        print(board)
    engine.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ChessCLI", usage='%(prog)s [options]', description="An all in one interface for the ancient game of chess. Play against your friend, computer or analyze PGN documents using %(prog)s To play against friend use the Game Mode: pvp To analyze a PGN doc use the Game Mode: pgn To play against engine use the Game Mode: pve\n")

    parser.add_argument("Game_mode", type=str, help="[pvp, pve, pgn] Game Mode to start the application")

    parser.add_argument("-Path_to_PGN", type=str, metavar='path', help="Path to pgn file for PGN simulation mode", default = "")

    args = parser.parse_args()
    
    if args.Game_mode == "pvp":
        print("Starting a PvP Session")
        pvp_game()
    elif args.Game_mode == "pve":
        print("Starting a PvE Session")
        pve_game()
    elif args.Game_mode == "pgn":
        print("Starting a PGN Simulation Session")
        path = args.Path_to_PGN
        if args.Path_to_PGN == "":
            path = input("Enter Path to PGN file")
        pgn_game(path)