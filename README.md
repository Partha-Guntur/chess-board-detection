# Detecting Chess Pieces and Completing the Game with YOLOv8 and Stockfish

## Overview
This project enables users to detect chess pieces and their positions on a chessboard image using YOLOv8, then continues the game using the Stockfish chess engine. The application is built using Flask, providing a user-friendly interface to upload chessboard images and view results interactively.

## Features
- Upload chessboard images for analysis.
- Detect chess pieces and their positions using a YOLOv8 model.
- Generate the chess position in PGN (Portable Game Notation) format.
- Integrate Stockfish to suggest the best moves and complete the game.
- Option to open the detected position directly in Lichess for further analysis or play.

## Technologies Used
- **YOLOv8**: For detecting chess pieces and their positions on the board.
- **Flask**: To create a web application for image uploads and displaying results.
- **Stockfish**: To calculate optimal moves and continue the game from the detected position.
- **Lichess API**: To enable users to explore positions on Lichess.

## How It Works
1. **Image Upload**: Users upload a chessboard image via the Flask web interface.
2. **Chess Piece Detection**: The YOLOv8 model detects chess pieces and identifies their positions on the board.
3. **PGN Generation**: The detected board position is converted into PGN format.
4. **Game Completion**: Stockfish processes the position and suggests the next move(s).
5. **Integration with Lichess**: Users can analyze the game further by opening the position in Lichess.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Virtual environment tool (e.g., `venv` or `conda`)
- Flask
- YOLOv8 model (pre-trained weights)
- Stockfish chess engine

### Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Partha-Guntur/chess-piece-detection.git
    cd chess-piece-detection
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Download YOLOv8 Weights**:
    Place the YOLOv8 pre-trained weights file in the `models/` directory.

5. **Set Up Stockfish**

6. **Run the Application**:
    ```bash
    flask run
    ```

### Directory Structure
```
chess-piece-detection/
├── static/
├── templates/
├── models/
│   └── yolov8-weights.pt
├── app.py
├── requirements.txt
├── README.md
└── stockfish.exe
```

## Usage
1. Start the Flask application:
    ```bash
    flask run
    ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.
3. Upload a chessboard image.
4. View the detected chess position and suggested Stockfish moves.
5. Use the "Open in Lichess" button to analyze the position on Lichess.

## Contact
For questions or feedback, please contact:
- **Name**: Partha Guntur
- **Email**: parthagunturu2003@gmail.com
- **GitHub**: [your-username](https://github.com/Partha-Guntur)
