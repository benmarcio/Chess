# Py-Chess: A Python-Based Chess Application

A comprehensive chess game built with Python and Pygame, featuring AI bot capabilities and game analysis tools.

## Project Structure

```
chess-app/
├── assets/              # Game assets (images, sounds)
│   ├── images/
│   │   └── pieces/      # Chess piece sprites
│   └── sounds/          # Sound effects
├── src/                 # Main source code
│   ├── board.py         # Chess board logic
│   ├── pieces.py        # Piece definitions
│   ├── moves.py         # Move validation
│   ├── bot.py           # AI bot logic
│   ├── game.py          # Game controller
│   └── main.py          # Entry point
├── models/              # Trained ML models
├── data/                # Game data (PGN files)
├── tests/               # Unit tests
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

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

## License

MIT License
