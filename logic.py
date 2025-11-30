"""
Модуль игровой логики шашек
"""
class CheckersGame:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 'white'
        self.game_over = False
        self.winner = None
    
    def create_board(self):
        """Создание начальной доски"""
        board = [[' ' for _ in range(8)] for _ in range(8)]
        
        # Расстановка черных шашек
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'black'
        
        # Расстановка белых шашек
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'white'
        
        return board
    
    def get_valid_moves(self, row, col):
        """Получение допустимых ходов для шашки"""
        if not self.is_valid_position(row, col) or self.board[row][col] == ' ':
            return []
        
        piece = self.board[row][col]
        moves = []
        
        # Определение направления движения
        if piece == 'white':
            directions = [(-1, -1), (-1, 1)]
        elif piece == 'black':
            directions = [(1, -1), (1, 1)]
        else:
            return moves
        
        # Проверка простых ходов
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col) and self.board[new_row][new_col] == ' ':
                moves.append((new_row, new_col, False))
        
        # Проверка взятий
        for dr, dc in directions:
            new_row, new_col = row + 2*dr, col + 2*dc
            jump_row, jump_col = row + dr, col + dc
            
            if (self.is_valid_position(new_row, new_col) and 
                self.board[new_row][new_col] == ' ' and
                self.is_valid_position(jump_row, jump_col) and
                self.board[jump_row][jump_col] != ' ' and
                self.board[jump_row][jump_col] != piece):
                moves.append((new_row, new_col, True))
        
        return moves
    
    def is_valid_position(self, row, col):
        """Проверка валидности позиции на доске"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Выполнение хода"""
        if self.game_over:
            return False
        
        valid_moves = self.get_valid_moves(from_row, from_col)
        move_made = False
        is_capture = False
        
        for move in valid_moves:
            if move[0] == to_row and move[1] == to_col:
                move_made = True
                is_capture = move[2]
                break
        
        if not move_made:
            return False
        
        # Выполнение хода
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '
        self.board[to_row][to_col] = piece
        
        # Удаление взятой шашки
        if is_capture:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            self.board[mid_row][mid_col] = ' '
        
        # Проверка на превращение в дамку
        if (piece == 'white' and to_row == 0) or (piece == 'black' and to_row == 7):
            self.board[to_row][to_col] = piece + '_king'
        
        # Проверка окончания игры
        self.check_game_over()
        
        # Смена игрока
        if not is_capture or not self.get_capture_moves(to_row, to_col):
            self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True
    
    def get_capture_moves(self, row, col):
        """Получение ходов со взятием для шашки"""
        moves = self.get_valid_moves(row, col)
        return [move for move in moves if move[2]]
    
    def check_game_over(self):
        """Проверка окончания игры"""
        white_pieces = 0
        black_pieces = 0
        white_moves = 0
        black_moves = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if 'white' in piece:
                    white_pieces += 1
                    if self.current_player == 'white':
                        white_moves += len(self.get_valid_moves(row, col))
                elif 'black' in piece:
                    black_pieces += 1
                    if self.current_player == 'black':
                        black_moves += len(self.get_valid_moves(row, col))
        
        if white_pieces == 0 or (self.current_player == 'white' and white_moves == 0):
            self.game_over = True
            self.winner = 'black'
        elif black_pieces == 0 or (self.current_player == 'black' and black_moves == 0):
            self.game_over = True
            self.winner = 'white'
    
    def get_board(self):
        """Получение текущего состояния доски"""
        return self.board
    
    def get_current_player(self):
        """Получение текущего игрока"""
        return self.current_player
    
    def is_game_over(self):
        """Проверка окончания игры"""
        return self.game_over
    
    def get_winner(self):
        """Получение победителя"""
        return self.winner
