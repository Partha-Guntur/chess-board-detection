import chess.pgn # type: ignore
pgn = open("/New Folder/roboflow/chess-board.pgn")

game = chess.pgn.read_game(pgn)

print(game.headers["White"], "vs", game.headers["Black"])
print(game)

board = game.board()
for move in game.mainline_moves():
    board.push(move)
    print(board)
