import pygame
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QSplitter, QDialog,
    QPushButton, QMessageBox, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont
import random
from board import Board

# Add parent directory to path so we can import models
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from models.alphabeta_bot import choose_move


class ColorSelectionDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Your Color')
        self.setModal(True)
        self.setGeometry(400, 300, 300, 150)
        
        layout = QVBoxLayout()
        label = QLabel('Choose which color you want to play:')
        label.setFont(QFont('Arial', 11))
        layout.addWidget(label)
        
        white_btn = QPushButton('Play as White')
        black_btn = QPushButton('Play as Black')
        
        white_btn.clicked.connect(lambda: self.select_color(1))
        black_btn.clicked.connect(lambda: self.select_color(-1))
        
        layout.addWidget(white_btn)
        layout.addWidget(black_btn)
        
        self.setLayout(layout)
        self.selected_color = None
    
    def select_color(self, color):
        self.selected_color = color
        self.accept()


class StartScreenWidget(QWidget):

    start_game = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_color = 1
        self.selected_mode = 'pvp'  # 'pvp' or 'bot'
        self.selected_time = 0
        self.white_depth = 3  # Default depth for white bot
        self.black_depth = 3  # Default depth for black bot

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('Py-Chess')
        title.setFont(QFont('Arial', 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel('Choose game mode')
        subtitle.setFont(QFont('Arial', 14))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # PvP section
        pvp_box = QVBoxLayout()
        pvp_label = QLabel('Player vs Player')
        pvp_label.setFont(QFont('Arial', 12, QFont.Bold))
        pvp_label.setAlignment(Qt.AlignCenter)
        pvp_box.addWidget(pvp_label)
        from PyQt5.QtWidgets import QComboBox
        pvp_time = QComboBox()
        pvp_time.addItems(['No clock', '1 min', '3 min', '5 min', '10 min', '15 min', '30 min'])
        pvp_time.setCurrentIndex(2)
        pvp_time.setFixedSize(300, 40)
        pvp_time.setFont(QFont('Arial', 11))
        pvp_time.setFocusPolicy(Qt.NoFocus)
        pvp_time.setStyleSheet('QComboBox:focus { outline: none; }')
        pvp_box.addWidget(pvp_time, alignment=Qt.AlignCenter)
        pvp_start = QPushButton('Start PvP')
        pvp_start.setFixedSize(240, 60)
        pvp_start.setFont(QFont('Arial', 12))
        pvp_start.clicked.connect(self._start_pvp)
        pvp_box.addWidget(pvp_start, alignment=Qt.AlignCenter)
        self.pvp_time_combo = pvp_time
        layout.addLayout(pvp_box)

        layout.addSpacing(20)

        bot_box = QVBoxLayout()
        bot_label = QLabel('Player vs Bot')
        bot_label.setFont(QFont('Arial', 12, QFont.Bold))
        bot_label.setAlignment(Qt.AlignCenter)
        bot_box.addWidget(bot_label)

        color_box = QHBoxLayout()
        white_btn = QPushButton('Play as White')
        black_btn = QPushButton('Play as Black')
        random_btn = QPushButton('Random')
        for b in (white_btn, black_btn, random_btn):
            b.setFixedSize(180, 50)
            b.setFont(QFont('Arial', 11))
        white_btn.clicked.connect(lambda: self._start_bot_with_color(1))
        black_btn.clicked.connect(lambda: self._start_bot_with_color(-1))
        random_btn.clicked.connect(lambda: self._start_bot_with_random())
        color_box.addWidget(white_btn)
        color_box.addWidget(black_btn)
        color_box.addWidget(random_btn)
        bot_box.addLayout(color_box)

        from PyQt5.QtWidgets import QComboBox
        bot_time = QComboBox()
        bot_time.addItems(['No clock', '1 min', '3 min', '5 min', '10 min', '15 min', '30 min'])
        bot_time.setCurrentIndex(2)
        bot_time.setFixedSize(300, 40)
        bot_time.setFont(QFont('Arial', 11))
        bot_time.setFocusPolicy(Qt.NoFocus)
        bot_time.setStyleSheet('QComboBox:focus { outline: none; }')
        bot_box.addWidget(bot_time, alignment=Qt.AlignCenter)
        self.bot_time_combo = bot_time

        layout.addLayout(bot_box)

        layout.addSpacing(20)

        # Bot vs Bot section
        botbot_box = QVBoxLayout()
        botbot_label = QLabel('Bot vs Bot (Debug)')
        botbot_label.setFont(QFont('Arial', 12, QFont.Bold))
        botbot_label.setAlignment(Qt.AlignCenter)
        botbot_box.addWidget(botbot_label)
        
        # Depth selectors for each bot
        depth_box = QHBoxLayout()
        depth_box.addStretch()
        
        white_depth_label = QLabel('White Depth:')
        white_depth_label.setFont(QFont('Arial', 10))
        white_depth_combo = QComboBox()
        white_depth_combo.addItems(['1', '2', '3', '4', '5', '6'])
        white_depth_combo.setCurrentIndex(2)  # Default to 3
        white_depth_combo.setFixedWidth(60)
        white_depth_combo.setFont(QFont('Arial', 10))
        white_depth_combo.setFocusPolicy(Qt.NoFocus)
        white_depth_combo.currentIndexChanged.connect(lambda idx: setattr(self, 'white_depth', int(white_depth_combo.currentText())))
        depth_box.addWidget(white_depth_label)
        depth_box.addWidget(white_depth_combo)
        
        depth_box.addSpacing(20)
        
        black_depth_label = QLabel('Black Depth:')
        black_depth_label.setFont(QFont('Arial', 10))
        black_depth_combo = QComboBox()
        black_depth_combo.addItems(['1', '2', '3', '4', '5', '6'])
        black_depth_combo.setCurrentIndex(2)  # Default to 3
        black_depth_combo.setFixedWidth(60)
        black_depth_combo.setFont(QFont('Arial', 10))
        black_depth_combo.setFocusPolicy(Qt.NoFocus)
        black_depth_combo.currentIndexChanged.connect(lambda idx: setattr(self, 'black_depth', int(black_depth_combo.currentText())))
        depth_box.addWidget(black_depth_label)
        depth_box.addWidget(black_depth_combo)
        
        depth_box.addStretch()
        botbot_box.addLayout(depth_box)
        
        botbot_start = QPushButton('Start Bot vs Bot')
        botbot_start.setFixedSize(240, 60)
        botbot_start.setFont(QFont('Arial', 12))
        botbot_start.clicked.connect(self._start_bot_vs_bot)
        botbot_box.addWidget(botbot_start, alignment=Qt.AlignCenter)
        layout.addLayout(botbot_box)

        self.setLayout(layout)

    def _emit_selection(self):
        payload = {
            'mode': self.selected_mode,
            'color': self.selected_color,
            'time': self.selected_time,
            'white_depth': self.white_depth,
            'black_depth': self.black_depth,
        }
        self.start_game.emit(payload)

    def _start_pvp(self):
        self.selected_mode = 'pvp'
        sel = getattr(self, 'pvp_time_combo', None)
        self.selected_time = 0
        if sel:
            idx = sel.currentIndex()
            minutes = [0, 1, 3, 5, 10, 15, 30][idx]
            self.selected_time = minutes * 60
        self._emit_selection()

    def _start_bot_with_color(self, color):
        self.selected_mode = 'bot'
        self.selected_color = color
        sel = getattr(self, 'bot_time_combo', None)
        self.selected_time = 0
        if sel:
            idx = sel.currentIndex()
            minutes = [0, 1, 3, 5, 10, 15, 30][idx]
            self.selected_time = minutes * 60
        self._emit_selection()

    def _start_bot_with_random(self):
        self.selected_mode = 'bot'
        self.selected_color = random.choice([1, -1])
        sel = getattr(self, 'bot_time_combo', None)
        self.selected_time = 0
        if sel:
            idx = sel.currentIndex()
            minutes = [0, 1, 3, 5, 10, 15, 30][idx]
            self.selected_time = minutes * 60
        self._emit_selection()

    def _start_bot_vs_bot(self):
        self.selected_mode = 'botbot'
        self.selected_color = 1  # Neutral
        self.selected_time = 0
        self._emit_selection()
        
    
class BoardWidget(QWidget):   
    def __init__(self, parent=None, player_color=1):
        super().__init__(parent)
        self.board = Board()
        self.player_color = player_color
        self.square_size = 80
        self.width = self.square_size * 8
        self.height = self.square_size * 8

        self.light_color = (238, 238, 210)
        self.dark_color = (118, 150, 86)

        # Piece assets
        self.assets = self.load_assets(self.square_size)

        # Drag state
        self.dragging = False
        self.initial_row = None
        self.initial_col = None
        self.valid_moves = []

        # Game state
        self.game_over = False
        self.result_msg = None

        # Move history
        self.moves = []  # List of tuples: ((from_row, from_col), (to_row, to_col))

        # Board flipped state
        self.board_flipped = (player_color == -1)
        # whether playing vs bot
        self.player_vs_bot = False
        # whether bot vs bot
        self.bot_vs_bot = False
        # when True (PvP) flip board view after each move
        self.auto_rotate = False
        
        # Bot search depths
        self.white_bot_depth = 3  # Default depth for white bot
        self.black_bot_depth = 3  # Default depth for black bot

        # Bot move highlight (visual feedback)
        self.last_move_from = None
        self.last_move_to = None
        self.highlight_timer = None

        # Pygame surface for rendering
        self.pygame_surface = pygame.Surface((self.width, self.height))

        self.setMinimumSize(QSize(self.width, self.height))
        self.setMaximumSize(QSize(self.width, self.height))
        self.setFocusPolicy(Qt.StrongFocus)

    def _is_simple_repetition(self):
        """Detect a simple repetition loop based on recent move patterns."""
        if len(self.moves) < 8:
            return False
        return self.moves[-4:] == self.moves[-8:-4]
    
    def load_assets(self, square_size):
        
        assets = {}
        piece_names = {
            1: "pawn", 2: "knight", 3: "bishop", 
            4: "rook", 5: "queen", 6: "king"
        }
        
        for piece_type, name in piece_names.items():
            for color_val in [1, -1]:
                key = piece_type * color_val
                suffix = "l" if color_val > 0 else "d"
                filename = f"{name}_{suffix}.png"
                
                try:
                    img = pygame.image.load(f"assets/images/pieces/{filename}")
                    img = pygame.transform.smoothscale(img, (square_size, square_size))
                    assets[key] = img
                except Exception:
                    print(f"Warning: Could not load {filename}")
        
        return assets
    
    def paintEvent(self, event):
        for row in range(8):
            for col in range(8):
                # Apply board flip transformation
                display_row = (7 - row) if self.board_flipped else row
                display_col = (7 - col) if self.board_flipped else col
                
                color = self.light_color if (display_row + display_col) % 2 == 0 else self.dark_color
                pygame.draw.rect(self.pygame_surface, color, 
                               (display_col * self.square_size, display_row * self.square_size, 
                                self.square_size, self.square_size))
                
                piece_value = self.board.squares[row][col]
                if piece_value != 0 and int(piece_value) in self.assets:
                    texture = self.assets[int(piece_value)]
                    self.pygame_surface.blit(texture, 
                                           (display_col * self.square_size, display_row * self.square_size))
        
        
        # Highlight bot's last move
        if self.last_move_from and self.last_move_to:
            for row, col in [self.last_move_from, self.last_move_to]:
                display_row = (7 - row) if self.board_flipped else row
                display_col = (7 - col) if self.board_flipped else col
                pygame.draw.rect(self.pygame_surface, (255, 255, 0),
                               (display_col * self.square_size, display_row * self.square_size,
                                self.square_size, self.square_size), 3)
        
        if self.valid_moves and not self.game_over:
            for move_row, move_col in self.valid_moves:
                display_row = (7 - move_row) if self.board_flipped else move_row
                display_col = (7 - move_col) if self.board_flipped else move_col
                
                center_x = display_col * self.square_size + self.square_size // 2
                center_y = display_row * self.square_size + self.square_size // 2
                pygame.draw.circle(self.pygame_surface, (100, 200, 100), (center_x, center_y), 8)
        
        
        if self.game_over and self.result_msg:
            font = pygame.font.SysFont(None, max(24, self.square_size // 2))
            text_surf = font.render(self.result_msg, True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
            self.pygame_surface.blit(text_surf, text_rect)
        
        # Convert pygame surface to QPixmap
        pygame_data = pygame.image.tostring(self.pygame_surface, "RGB", False)
        qimg = QImage(pygame_data, self.width, self.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        
        # Draw on widget
        painter = event.painter() if hasattr(event, 'painter') else None
        if painter:
            painter.drawPixmap(0, 0, pixmap)
        else:
            from PyQt5.QtGui import QPainter
            painter = QPainter(self)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
    
    def mousePressEvent(self, event):
        
        if self.game_over:
            return
        
        x = event.x()
        y = event.y()
        
        # Reverse coordinates if board is flipped
        if self.board_flipped:
            x = self.width - x
            y = self.height - y
        
        col = x // self.square_size
        row = y // self.square_size
        
        if 0 <= row < 8 and 0 <= col < 8:
            if self.board.squares[row][col] != 0:
                self.dragging = True
                self.initial_row = row
                self.initial_col = col
                self.valid_moves = self.board.get_valid_moves(row, col)
                self.update()
    
    def mouseReleaseEvent(self, event):
        if not self.dragging or self.game_over:
            self.dragging = False
            return
        
        x = event.x()
        y = event.y()
        
        # Reverse coordinates if board is flipped
        if self.board_flipped:
            x = self.width - x
            y = self.height - y
        
        final_col = x // self.square_size
        final_row = y // self.square_size
        
        if 0 <= final_row < 8 and 0 <= final_col < 8:
            final_pos = (final_row, final_col)
            
            if final_pos in self.valid_moves:
                # Record move before making it
                self.moves.append(((self.initial_row, self.initial_col), final_pos))
                self.board.move_piece((self.initial_row, self.initial_col), final_pos)
                
                # Check for draws first (repetition and fifty-move rule)
                if self.board.is_fifty_move_rule():
                    self.result_msg = 'Draw (fifty-move rule)'
                    self.game_over = True
                elif self._is_simple_repetition():
                    self.result_msg = 'Draw (repetition loop)'
                    self.game_over = True
                # Check for mate/stalemate
                elif not self.board.has_any_legal_moves(self.board.side_to_move):
                    if self.board.is_in_check(self.board.side_to_move):
                        winner = 'White' if self.board.side_to_move == -1 else 'Black'
                        self.result_msg = f"{winner} wins by checkmate"
                    else:
                        self.result_msg = 'Draw (stalemate)'
                    self.game_over = True
                # Auto-rotate board view for PvP games after each successful move
                if self.auto_rotate:
                    self.board_flipped = not self.board_flipped
                    self.update()

                if self.player_vs_bot and not self.game_over:
                    self.make_bot_move()
        
        self.dragging = False
        self.initial_row = None
        self.initial_col = None
        self.valid_moves = []
        self.update()
    
    def _execute_bot_move(self):
        """Actually execute the bot's chosen move (called after visual delay)."""
        if self.game_over:
            return

        if self.player_vs_bot:
            bot_color = -self.player_color
            if self.board.side_to_move != bot_color:
                return
        elif self.bot_vs_bot:
            # Bot vs bot: just play the current side
            pass
        else:
            return

        # Use the appropriate depth based on whose turn it is
        if self.bot_vs_bot:
            depth = self.white_bot_depth if self.board.side_to_move == 1 else self.black_bot_depth
        else:
            depth = 1  # Player vs bot uses depth 1 for the bot
        
        move = choose_move(self.board, self.board.side_to_move, depth=depth)
        if move is None:
            return

        (sr, sc), (fr, fc) = move
        self.last_move_from = (sr, sc)
        self.last_move_to = (fr, fc)
        
        self.moves.append(((sr, sc), (fr, fc)))
        # Store bot move clock - ensure consistent tracking
        # Get the move_clocks list from MainWindow parent
        from_parent = self.parentWidget()
        while from_parent and not isinstance(from_parent, QMainWindow):
            from_parent = from_parent.parentWidget()
        
        # Track clock time if available, otherwise append None for consistency
        if from_parent:
            if hasattr(from_parent, 'white_time') and hasattr(from_parent, 'black_time') and \
               from_parent.white_time is not None and from_parent.black_time is not None:
                # Append the appropriate real clock based on whose turn it was
                clock_time = from_parent.white_time if self.board.side_to_move == 1 else from_parent.black_time
                from_parent.move_clocks.append(clock_time)
            elif hasattr(from_parent, 'bot_white_time') and hasattr(from_parent, 'bot_black_time') and \
                 from_parent.bot_white_time is not None and from_parent.bot_black_time is not None:
                # Use artificial bot clocks for PGN timestamps
                if self.board.side_to_move == 1:
                    clock_time = from_parent.bot_white_time
                    from_parent.bot_white_time = max(0, from_parent.bot_white_time - 1)
                else:
                    clock_time = from_parent.bot_black_time
                    from_parent.bot_black_time = max(0, from_parent.bot_black_time - 1)
                from_parent.move_clocks.append(clock_time)
            else:
                # No clock available - append None to maintain list consistency
                from_parent.move_clocks.append(None)
        
        self.board.move_piece((sr, sc), (fr, fc))

        # Check for draws first (repetition and fifty-move rule)
        if self.board.is_fifty_move_rule():
            self.result_msg = 'Draw (fifty-move rule)'
            self.game_over = True
        elif self._is_simple_repetition():
            self.result_msg = 'Draw (repetition loop)'
            self.game_over = True
        elif not self.board.has_any_legal_moves(self.board.side_to_move):
            if self.board.is_in_check(self.board.side_to_move):
                winner = 'White' if self.board.side_to_move == -1 else 'Black'
                self.result_msg = f"{winner} wins by checkmate"
            else:
                self.result_msg = 'Draw (stalemate)'
            self.game_over = True
        else:
            # Clear highlight after 1 second
            if self.highlight_timer:
                self.highlight_timer.stop()
            self.highlight_timer = QTimer()
            self.highlight_timer.setSingleShot(True)
            self.highlight_timer.timeout.connect(self._clear_move_highlight)
            self.highlight_timer.start(1000)
            
            # Continue bot vs bot automatically with 0,1 second delay
            if self.bot_vs_bot and not self.game_over:
                QTimer.singleShot(100, self._execute_bot_move)

        self.update()

    def make_bot_move(self, depth=3):
        """Defer bot move to next event loop to avoid blocking UI."""
        if self.game_over:
            return
        if not (self.player_vs_bot or self.bot_vs_bot):
            return
        
        # Schedule bot move on the event loop to keep UI responsive
        QTimer.singleShot(100, self._execute_bot_move)

    def _clear_move_highlight(self):
        """Clear the bot move highlight."""
        self.last_move_from = None
        self.last_move_to = None
        self.update()

    def reset_game(self):
        self.board = Board()
        self.dragging = False
        self.game_over = False
        self.result_msg = None
        self.valid_moves = []
        self.moves = []
        self.update()

    def pos_to_algebraic(self, row, col):
        
        files = 'abcdefgh'
        ranks = '87654321'
        return files[col] + ranks[row]
    
    def get_move_notation(self, from_pos, to_pos):
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        return f"{self.pos_to_algebraic(from_row, from_col)}->{self.pos_to_algebraic(to_row, to_col)}"


class MainWindow(QMainWindow):
   
    def __init__(self, player_color=1):
        super().__init__()
        self.player_color = player_color
        self.setWindowTitle('Py-Chess')
        self.setGeometry(100, 100, 1200, 650)

        
        self.start_screen = StartScreenWidget(self)
        self.start_screen.start_game.connect(self._apply_start_settings)

        
        self.board_widget = BoardWidget(player_color=self.player_color)
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        title = QLabel('Game Info')
        title.setFont(QFont('Arial', 12, QFont.Bold))
        sidebar_layout.addWidget(title)

        color_text = 'Playing as White' if self.player_color == 1 else 'Playing as Black'
        self.color_label = QLabel(color_text)
        self.color_label.setFont(QFont('Arial', 10, QFont.Bold))
        sidebar_layout.addWidget(self.color_label)

        self.turn_label = QLabel('White to move')
        self.turn_label.setFont(QFont('Arial', 10))
        sidebar_layout.addWidget(self.turn_label)

        history_title = QLabel('Move History')
        history_title.setFont(QFont('Arial', 12, QFont.Bold))
        sidebar_layout.addWidget(history_title)

        self.move_list = QListWidget()
        self.move_list.setFont(QFont('Courier', 9))
        sidebar_layout.addWidget(self.move_list)
        self.processed_half_moves = 0

        self.white_timer_label = QLabel('White: --:--')
        self.white_timer_label.setFont(QFont('Courier', 11, QFont.Bold))
        sidebar_layout.addWidget(self.white_timer_label)
        self.black_timer_label = QLabel('Black: --:--')
        self.black_timer_label.setFont(QFont('Courier', 11, QFont.Bold))
        sidebar_layout.addWidget(self.black_timer_label)

        self.sidebar.setLayout(sidebar_layout)
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(300)

        game_page = QWidget()
        game_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.board_widget)
        splitter.addWidget(self.sidebar)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        game_layout.addWidget(splitter)
        game_page.setLayout(game_layout)

        
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.start_screen)
        self.stacked.addWidget(game_page)
        self.setCentralWidget(self.stacked)
        self.stacked.setCurrentWidget(self.start_screen)
        
        
        self.create_menus()
        
        
        self.statusBar().showMessage('Ready!')
        
        
        self.load_stylesheet()
        
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_game_state)
        self.update_timer.start(100)

        
        self.white_time = None
        self.black_time = None
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._on_clock_tick)

        self.time_control_seconds = 0
        self.move_clocks = []

        # Artificial clocks for bot vs bot when no real time control is used
        self.bot_white_time = None
        self.bot_black_time = None

        self._game_over_shown = False
    
    def create_menus(self):
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('Menu')
        file_menu.addAction('New Game', self.new_game)
        file_menu.addAction('Save Game', self.save_game)
        file_menu.addAction('Load Game', self.load_game)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)
        
        
        edit_menu = menubar.addMenu('Action')
        edit_menu.addAction('Undo', self.undo_move)
        edit_menu.addAction('Reset Board', self.reset_board)
        edit_menu.addAction('Flip Board', self.flip_board_view)
                
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About', self.show_about)
    
    def load_stylesheet(self):
        try:
            with open('src/style.qss', 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception:
            print("Warning: Could not load stylesheet")
    
    def new_game(self):
        if self.clock_timer.isActive():
            self.clock_timer.stop()
        self.board_widget.hide()
        self.stacked.setCurrentWidget(self.start_screen)
        self.statusBar().showMessage('New game - choose options')

    def _apply_start_settings(self, selection):
        sel_color = selection.get('color', 1)
        sel_mode = selection.get('mode', 'pvp')
        sel_time = selection.get('time', 0)
        white_depth = selection.get('white_depth', 3)
        black_depth = selection.get('black_depth', 3)

        self.time_control_seconds = sel_time

        self.player_color = sel_color
        self.board_widget.player_color = sel_color
        self.board_widget.board_flipped = (sel_color == -1)
        self.board_widget.player_vs_bot = (sel_mode == 'bot')
        self.board_widget.bot_vs_bot = (sel_mode == 'botbot')
        self.board_widget.auto_rotate = (sel_mode == 'pvp')
        self.board_widget.white_bot_depth = white_depth
        self.board_widget.black_bot_depth = black_depth
        self.color_label.setText('Playing as White' if self.player_color == 1 else 'Playing as Black')
        self.board_widget.update()

        if sel_time and sel_time > 0:
            self.white_time = sel_time
            self.black_time = sel_time
            self.white_timer_label.setText(f'White: {self._format_time(self.white_time)}')
            self.black_timer_label.setText(f'Black: {self._format_time(self.black_time)}')
            if not self.clock_timer.isActive():
                self.clock_timer.start(1000)
        else:
            self.white_time = None
            self.black_time = None
            self.white_timer_label.setText('White: --:--')
            self.black_timer_label.setText('Black: --:--')

        # Initialize artificial bot clocks (used for PGN timestamps in bot vs bot)
        if sel_mode == 'botbot':
            base_time = sel_time if sel_time and sel_time > 0 else 300
            self.bot_white_time = base_time
            self.bot_black_time = base_time
        else:
            self.bot_white_time = None
            self.bot_black_time = None

        self.board_widget.reset_game()
        self.move_list.clear()
        self.processed_half_moves = 0
        self.move_clocks = []
        self.update_turn_label()
        self.board_widget.show()
        self.stacked.setCurrentIndex(1)
        self.setFocus()
        self._game_over_shown = False

        if self.board_widget.bot_vs_bot:
            # Start with white bot move
            self.board_widget.make_bot_move()
        elif self.board_widget.player_vs_bot and self.board_widget.board.side_to_move == -self.player_color:
            self.board_widget.make_bot_move()

    def save_game(self):
        self._save_game_to_pgn(auto=False)

    def _save_game_to_pgn(self, auto=False):
        if not self.board_widget.moves:
            if not auto:
                self.statusBar().showMessage('No moves to save')
            return

        pgn_text = self._build_pgn_text()
        if not pgn_text:
            if not auto:
                self.statusBar().showMessage('Could not build PGN')
            return

        pgn_path = os.path.join(ROOT_DIR, 'data', 'games.pgn')
        os.makedirs(os.path.dirname(pgn_path), exist_ok=True)

        try:
            with open(pgn_path, 'a', encoding='utf-8') as f:
                f.write(pgn_text)
                if not pgn_text.endswith('\n'):
                    f.write('\n')
                f.write('\n')
            if not auto:
                self.statusBar().showMessage('Game saved to games.pgn')
        except Exception as e:
            if not auto:
                self.statusBar().showMessage(f'Failed to save game: {str(e)}')

    def _build_pgn_text(self):
        result = self._get_pgn_result()
        white_name, black_name = self._get_player_names()

        try:
            import chess
            import chess.pgn
        except Exception as e:
            print(f"Chess import error: {e}")
            return None

        game = chess.pgn.Game()
        game.headers["Event"] = "Py-chess"
        game.headers["Site"] = "custom app"
        game.headers["Date"] = self._current_date()
        game.headers["Round"] = "?"
        game.headers["White"] = white_name
        game.headers["Black"] = black_name
        game.headers["Result"] = result
        game.headers["ECO"] = "?"
        game.headers["WhiteElo"] = "?"
        game.headers["BlackElo"] = "?"
        game.headers["TimeControl"] = str(self.time_control_seconds or 0)
        game.headers["EndTime"] = self._current_time_with_tz()
        game.headers["Termination"] = self._get_termination_text(white_name, black_name)

        board = chess.Board()
        node = game
        moves = self.board_widget.moves
        
        for idx, move in enumerate(moves):
            uci = self._to_uci(board, move)
            if not uci:
                return None
            try:
                chess_move = chess.Move.from_uci(uci)
                if chess_move not in board.legal_moves:
                    return None
                node = node.add_variation(chess_move)
                node.comment = self._clock_comment(idx)
                board.push(chess_move)
            except Exception as e:
                return None

        # Use columns parameter to ensure consistent multi-line formatting for all games
        exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=True, columns=80)
        pgn = game.accept(exporter).strip()
        return pgn

    def _current_date(self):
        from datetime import datetime
        return datetime.now().strftime('%Y.%m.%d')

    def _current_time_with_tz(self):
        from datetime import datetime
        now = datetime.now().astimezone()
        tz = now.strftime('%z')
        return now.strftime('%H:%M:%S ') + f"GMT{tz}"

    def _get_player_names(self):
        if self.board_widget.player_vs_bot:
            if self.player_color == 1:
                return 'Player', 'Bot'
            return 'Bot', 'Player'
        return 'White', 'Black'

    def _get_pgn_result(self):
        msg = (self.board_widget.result_msg or '').lower()
        if 'white wins' in msg:
            return '1-0'
        if 'black wins' in msg:
            return '0-1'
        if 'draw' in msg or 'stalemate' in msg:
            return '1/2-1/2'
        return '*'

    def _get_termination_text(self, white_name, black_name):
        msg = (self.board_widget.result_msg or '').lower()
        if 'white wins' in msg:
            return f"{white_name} won by checkmate"
        if 'black wins' in msg:
            return f"{black_name} won by checkmate"
        if 'time' in msg:
            if 'black wins' in msg:
                return f"{black_name} won on time"
            return f"{white_name} won on time"
        if 'stalemate' in msg or 'draw' in msg:
            return "Game drawn"
        return "Game ended"

    def _to_uci(self, board, move):
        try:
            from_pos, to_pos = move
            from_sq = self.board_widget.pos_to_algebraic(*from_pos)
            to_sq = self.board_widget.pos_to_algebraic(*to_pos)
            uci = f"{from_sq}{to_sq}"
            import chess
            from_square = chess.parse_square(from_sq)
            piece = board.piece_at(from_square)
            if piece and piece.piece_type == 1:
                # Promotion to queen by default when reaching last rank
                if to_sq[1] in ('8', '1'):
                    uci += 'q'
            return uci
        except Exception as e:
            return None

    def _clock_comment(self, move_idx):
        if not self.move_clocks or move_idx >= len(self.move_clocks):
            return ''
        secs = self.move_clocks[move_idx]
        if secs is None:
            return ''
        # Don't add clock comments if the value is 0 or None (for bot vs bot games)
        if secs == 0:
            return ''
        return f"[%clk {self._format_clock_comment(secs)}]"

    def _format_clock_comment(self, seconds):
        total = max(0, int(seconds))
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}.0"
        return f"0:{m:02d}:{s:02d}.0"

    def _format_pgn_moves(self):
        moves = self.board_widget.moves
        if moves is None:
            return None

        tokens = []
        for idx in range(0, len(moves), 2):
            move_num = (idx // 2) + 1
            w_move = self._coord_move(moves[idx]) if idx < len(moves) else None
            b_move = self._coord_move(moves[idx + 1]) if idx + 1 < len(moves) else None
            if w_move is None:
                return None
            if b_move:
                tokens.append(f"{move_num}. {w_move} {b_move}")
            else:
                tokens.append(f"{move_num}. {w_move}")
        return " ".join(tokens)

    def _coord_move(self, move):
        try:
            from_pos, to_pos = move
            return f"{self.board_widget.pos_to_algebraic(*from_pos)}{self.board_widget.pos_to_algebraic(*to_pos)}"
        except Exception:
            return None
    
    def load_game(self):
        
        self.statusBar().showMessage('Load game feature not yet implemented')
    
    def undo_move(self):
        
        self.statusBar().showMessage('Undo feature not yet implemented')
    
    def reset_board(self):
        
        self.new_game()
    
    def flip_board_view(self):
        
        self.board_widget.board_flipped = not self.board_widget.board_flipped
        self.board_widget.update()
        self.statusBar().showMessage('Board flipped')
    
    def show_about(self):
        
        self.statusBar().showMessage('Py-Chess - A simple chess game built with PyQt5 and Pygame')
    
    def update_game_state(self):
        
        self.update_turn_label()
        self.update_move_history()
        
        if self.board_widget.game_over and not self._game_over_shown:
            self._game_over_shown = True
            msg = self.board_widget.result_msg or 'Game over'
            if self.board_widget.player_vs_bot or self.board_widget.bot_vs_bot:
                self._save_game_to_pgn(auto=True)
            QMessageBox.information(self, 'Game Over', msg)
            # After acknowledging, go back to start screen
            self.new_game()

    def _format_time(self, seconds):
        if seconds is None:
            return '--:--'
        if seconds < 0:
            seconds = 0
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"

    def _on_clock_tick(self):
        
        if self.board_widget.game_over:
            self.clock_timer.stop()
            return

        if self.white_time is None or self.black_time is None:
            return

        
        if self.board_widget.board.side_to_move == 1:
            self.white_time -= 1
            if self.white_time <= 0:
                self.white_time = 0
                self.clock_timer.stop()
                self.board_widget.game_over = True
                self.board_widget.result_msg = 'Black wins on time'
        else:
            self.black_time -= 1
            if self.black_time <= 0:
                self.black_time = 0
                self.clock_timer.stop()
                self.board_widget.game_over = True
                self.board_widget.result_msg = 'White wins on time'

        
        self.white_timer_label.setText(f'White: {self._format_time(self.white_time)}')
        self.black_timer_label.setText(f'Black: {self._format_time(self.black_time)}')

    def closeEvent(self, event):
        
        try:
            if self.clock_timer.isActive():
                self.clock_timer.stop()
        except Exception:
            pass
        return super().closeEvent(event)

    def show_color_dialog(self):
        
        dialog = ColorSelectionDialog(self)
        if dialog.exec_() == dialog.Accepted:
            selected = dialog.selected_color or 1
            self.player_color = selected
            self.board_widget.board_flipped = (self.player_color == -1)
            self.color_label.setText('Playing as White' if self.player_color == 1 else 'Playing as Black')
            self.board_widget.update()
        
    def update_move_history(self):
        
        moves = self.board_widget.moves
        total = len(moves)
        if self.processed_half_moves >= total:
            return

        for move_idx in range(self.processed_half_moves, total):
            from_pos, to_pos = moves[move_idx]
            notation = self.board_widget.get_move_notation(from_pos, to_pos)
            is_white = (move_idx % 2 == 0)
            move_num = (move_idx // 2) + 1

            if move_idx >= len(self.move_clocks):
                if self.white_time is None or self.black_time is None:
                    self.move_clocks.append(None)
                else:
                    self.move_clocks.append(self.white_time if is_white else self.black_time)

            if is_white:
                text = f"{move_num}. {notation}"
                self.move_list.addItem(text)
            else:
                # Append black's move to the last added item (same move number)
                item = self.move_list.item(self.move_list.count() - 1)
                if item:
                    prev_text = item.text()
                    item.setText(f"{prev_text}  {notation}")

        
        self.processed_half_moves = total
    
    def update_turn_label(self):
        
        color = 'White' if self.board_widget.board.side_to_move == 1 else 'Black'
        in_check = ' (Check!)' if self.board_widget.board.is_in_check(self.board_widget.board.side_to_move) else ''
        self.turn_label.setText(f'{color} to move{in_check}')
