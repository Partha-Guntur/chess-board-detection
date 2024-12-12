import chess
import chess.pgn
import chess.engine

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board = chess.Board(fen)

stockfish_path = "e:/New Folder/roboflow/stockfish-windows-x86-64/stockfish/stockfish-windows-x86-64.exe"
try:
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
except PermissionError as e:
    print(f"PermissionError: {e}")
    print("Check if the path to Stockfish is correct and if you have execute permissions.")
    exit()
except chess.engine.EngineTerminatedError as e:
    print(f"EngineTerminatedError: {e}")
    print("Check if Stockfish binary is compatible with your system and architecture.")
    exit()

game = chess.pgn.Game()
game.setup(board)
node = game
try:
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=2.0))
        move = result.move
        node = node.add_main_variation(move)
        board.push(move)
finally:
    engine.quit()

with open("output.pgn", "w") as pgn_file:
    pgn_file.write(str(game))

print("PGN saved to output.pgn")
