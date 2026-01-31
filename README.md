# Py-Chess: A Python-Based Chess Application

A feature-rich chess game built with Python, PyQt5, and Pygame. Play against friends locally or challenge an intelligent AI bot with customizable time controls.

## Features

### Core Gameplay
- **Two Game Modes:**
  - **Player vs Player (PvP):** Local multiplayer chess with two players on the same computer
  - **Player vs Bot:** Challenge an AI opponent at various skill levels
  
- **Intelligent Move Validation:** Full chess rule implementation including:
  - Standard piece movements (pawns, rooks, bishops, knights, queens, kings)
  - Castling (kingside and queenside)
  - En passant pawn captures
  - Pawn promotion
  - Check and checkmate detection
  - Stalemate detection

- **Time Controls:** Multiple time formats to choose from:
  - No clock (unlimited time)
  - Blitz: 1, 3, 5 minutes
  - Rapid: 10, 15 minutes
  - Classical: 30 minutes

- **Board Interaction:**
  - Intuitive drag-and-drop piece movement
  - Real-time display of valid moves (green indicators)
  - Move history tracking
  - Board perspective toggle (play as White or Black)
  - Auto-rotating board in PvP mode for player convenience

- **Visual Polish:**
  - Professional chess board with alternating square colors
  - High-quality piece graphics
  - Clean PyQt5-based user interface
  - Start screen with easy game mode selection
  - Game status indicators (check, checkmate, game over messages)

## Project Structure

```
Chess/
├── assets/                    # Game assets
│   ├── images/
│   │   └── pieces/           # Chess piece sprites
│   └── sounds/               # Sound effects
├── src/                       # Main source code
│   ├── main.py               # Application entry point
│   ├── ui.py                 # PyQt5 GUI and game interface
│   ├── board.py              # Chess board logic and piece management
│   ├── piece.py              # Piece class definitions
│   ├── style.qss             # Qt stylesheet for UI customization
│   └── __pycache__/          # Compiled Python files
├── models/                    # AI model files (if applicable)
├── data/                      # Game data storage
├── tests/                     # Unit tests
├── requirements.txt           # Python package dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Chess
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
```

#### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## How to Play

### Starting the Game

```bash
python src/main.py
```

The application will launch with a start screen showing your game options.

### Game Mode Selection

**Player vs Player:**
1. Click "Start PvP" on the main menu
2. Select your preferred time control (or "No clock" for unlimited)
3. Take turns moving pieces with another player using the mouse

**Player vs Bot:**
1. Select "Player vs Bot" mode
2. Choose your color:
   - **Play as White:** You move first
   - **Play as Black:** Bot moves first
   - **Random:** Randomly assigned at game start
3. Choose your preferred time control
4. Make your moves by dragging pieces; the bot will respond automatically

### Making Moves

1. **Select a Piece:** Click on one of your pieces
2. **View Valid Moves:** Green dots appear showing all legal moves for that piece
3. **Move the Piece:** Click on a valid destination square to complete your move
4. **Confirm Move:** The move is executed immediately

### Game Features During Play

- **Move Indicators:** Green circles show all valid moves for the selected piece
- **Game Status:** The board displays when you're in check and announces checkmate or stalemate
- **Move History:** Your game moves are tracked throughout the session
- **Board Perspective:** In PvP mode, the board automatically rotates after each move
- **Time Clock:** If enabled, the game tracks remaining time for each player

### Game End

The game ends when:
- **Checkmate:** One player's king is in check with no legal moves
- **Stalemate:** A player to move is not in check but has no legal moves (draw)
- **Resignation:** A player gives up (via the interface)

## Dependencies

The application requires the following Python packages:

- **pygame** (2.5.2+) - Graphics and event handling
- **PyQt5** - GUI framework
- **numpy** (1.24.0+) - Numerical computations for board representation
- **pandas** (2.0.0+) - Data manipulation (for future analytics)
- **python-chess** (1.10.0+) - Chess rules validation and utilities

All dependencies are listed in `requirements.txt` and installed via pip.

## Gameplay Tips

- **Think Ahead:** Consider your opponent's possible responses to your moves
- **Protect Your Pieces:** Avoid leaving pieces undefended
- **Control the Center:** Occupying central squares gives pieces more mobility
- **Use Time Wisely:** In timed games, manage your clock carefully
- **Learn from the Bot:** Playing against the AI bot helps improve your chess skills

## Troubleshooting

**Game won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you've activated the virtual environment
- Verify Python version is 3.7 or higher: `python --version`

**Pieces images not displaying:**
- Confirm the `assets/images/pieces/` directory contains all PNG files
- Check file names match the expected format (e.g., `pawn_l.png`, `knight_d.png`)

**Time controls not working:**
- Ensure numpy and PyQt5 are properly installed
- Check system clock is accurate

## Future Enhancements

Potential features for future versions:
- Advanced bot difficulty levels
- Game replay and analysis features
- Online multiplayer support
- Opening book integration
- Move suggestions and analysis
- Save/load game functionality

## Getting Started

To run the chess application:
```bash
python src/main.py
```

## Development Phases

- **Phase 1:** GUI setup with Pygame
- **Phase 2:** Chess logic and move validation
- **Phase 3:** AI bot development (Minimax + Alpha-Beta pruning)
- **Phase 4:** Model training and analysis

## Dependencies

- **pygame:** GUI and graphics rendering
- **numpy:** Numerical computations
- **pandas:** Data handling
- **torch:** Deep learning framework
- **python-chess:** Chess logic utilities


