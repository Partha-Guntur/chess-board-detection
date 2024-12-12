import cv2

image = cv2.imread('e:/New Folder/roboflow/chess_move.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

chessboard_size = (7, 7)
ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size, None)

if ret:
    cv2.drawChessboardCorners(image, chessboard_size, corners, ret)
    cv2.imshow('Chessboard', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
detected_pieces = {
    'a1': 'r', 'b1': 'n', 'c1': 'b', # etc.
}

positions = [
    'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
    'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
    'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'
]

def generate_fen(board_position):
    fen = ''
    empty_count = 0
    for i, piece in enumerate(board_position):
        if piece == ' ':
            empty_count += 1
        else:
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            fen += piece
        if (i + 1) % 8 == 0:
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            fen += '/'
    return fen.rstrip('/')

fen = generate_fen(positions)
print(fen)
