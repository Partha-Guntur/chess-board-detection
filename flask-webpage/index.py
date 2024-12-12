import requests
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image #type: ignore
import numpy as np
import os
from ultralytics import YOLO
from PIL import Image
import cv2
import chess
import chess.pgn
import chess.engine

app = Flask(__name__)

board_model = load_model('e:/New Folder/roboflow/my_model.keras')
pieces_model = YOLO('e:/New Folder/roboflow/runs/detect/train/weights/best.pt')

UPLOAD_FOLDER = 'uploads'
DETECTED_FOLDER = 'static/detected'
PGN_FOLDER = 'static/pgn'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTED_FOLDER, exist_ok=True)
os.makedirs(PGN_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_pgn(fen):
    # Initialize the chess board from the given FEN
    board = chess.Board(fen)

    # Path to Stockfish engine
    stockfish_path = "e:/New Folder/roboflow/stockfish-windows-x86-64/stockfish/stockfish-windows-x86-64.exe"
    
    try:
        # Start Stockfish UCI engine
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    except PermissionError as e:
        print(f"PermissionError: {e}")
        print("Check if the path to Stockfish is correct and if you have execute permissions.")
        return
    except chess.engine.EngineTerminatedError as e:
        print(f"EngineTerminatedError: {e}")
        print("Check if Stockfish binary is compatible with your system and architecture.")
        return

    # Create a new PGN game object and set it up with the initial board position
    game = chess.pgn.Game()
    game.setup(board)
    node = game

    try:
        while not board.is_game_over():
            # Request a move from Stockfish with a reduced time limit (0.5 seconds) and depth limit (optional)
            result = engine.play(board, chess.engine.Limit(time=0.5, depth=12))
            move = result.move
            node = node.add_main_variation(move)
            board.push(move)

            # Early exit if a decisive game state is reached
            if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                break
    finally:
        # Quit the engine
        engine.quit()

    # Save the PGN to a file
    with open("output.pgn", "w") as pgn_file:
        pgn_file.write(str(game))

    print("PGN saved to output.pgn")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url), 400

    file = request.files['image']
 
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process image for chessboard detection
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        prediction = board_model.predict(img_array)

        # PIL image to NumPy array for OpenCV
        img_np = np.array(img)

        gray_image = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        chessboard_size = (7, 7)
        ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size, None)

        if ret:
            cv2.drawChessboardCorners(img_np, chessboard_size, corners, ret)
            cv2.imshow('Chessboard', img_np)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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

        if prediction[0][0] < 0.5:
            result = 'Chessboard detected'
            img_for_detection = Image.open(filepath)
            detection_results = pieces_model(img_for_detection, save=False)
            output_image_filename = 'detected_' + filename
            output_image_path = os.path.join(DETECTED_FOLDER, output_image_filename)
            detection_results[0].save(output_image_path)
            relative_image_path = os.path.join('detected', output_image_filename).replace("\\", "/")
            generate_pgn(fen)
            with open('output.pgn', 'r') as file:
                content = file.read()

            return render_template('index.html', 
                                   prediction=result, 
                                   detection_result='Chess pieces detected', 
                                   image_path=relative_image_path,  # Corrected relative path
                                   pgn=content), 200
        else:
            result = 'No chessboard detected'
            return render_template('index.html', prediction=result), 200
    return redirect(request.url), 400

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        chessboard_images = [img for img in os.listdir(DETECTED_FOLDER) if img.endswith('.png')]

        return render_template('index.html', chessboards=chessboard_images)

    return redirect(request.url)

@app.route('/open_lichess', methods=['POST'])
def open_lichess():
    pgn = request.form['pgn']
    token = "lip_2iDezTw9JBnTfDxxxmyZ" # API token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'pgn': pgn
    }
    response = requests.post('https://lichess.org/api/import', headers=headers, json=data)
    if response.status_code == 200:
        json_response = response.json()
        lichess_url = json_response['url']
        return redirect(lichess_url)
    else:
        return f"Error: Could not open Lichess playground. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
