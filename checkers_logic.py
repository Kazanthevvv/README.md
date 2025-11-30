class CheckersGame:
    def __init__(self):
        self.board = []
        self.current_player = 'white'
        self.initialize_board()
    
    def initialize_board(self):
        """Создаем начальную расстановку шашек"""
        self.board = []
        for row in range(8):
            self.board.append([' '] * 8)
        
        # Черные шашки (вверху)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'black'
        
        # Белые шашки (внизу)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'white'
    
    def get_board(self):
        """Возвращает текущее состояние доски"""
        return self.board
    
    def get_current_player(self):
        """Возвращает текущего игрока"""
        return self.current_player
    
    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка валидности хода"""
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and
                0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        
        if self.board[start_row][start_col] != self.current_player:
            return False
        
        if self.board[end_row][end_col] != ' ':
            return False
        
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
        
        # Простой ход на одну клетку
        if abs(end_row - start_row) == 1:
            if self.current_player == 'white' and end_row == start_row - 1:
                return True
            elif self.current_player == 'black' and end_row == start_row + 1:
                return True
        
        # Взятие шашки
        if abs(end_row - start_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            opponent = 'black' if self.current_player == 'white' else 'white'
            if self.board[middle_row][middle_col] == opponent:
                return True
        
        return False
    
    def make_move(self, start_row, start_col, end_row, end_col):
        """Выполнение хода"""
        if self.is_valid_move(start_row, start_col, end_row, end_col):
            # Перемещаем шашку
            self.board[end_row][end_col] = self.current_player
            self.board[start_row][start_col] = ' '
            
            # Если это взятие, убираем шашку противника
            if abs(end_row - start_row) == 2:
                middle_row = (start_row + end_row) // 2
                middle_col = (start_col + end_col) // 2
                self.board[middle_row][middle_col] = ' '
            
            # Меняем игрока
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False
    
    def get_winner(self):
        """Проверка на победу"""
        white_count = sum(row.count('white') for row in self.board)
        black_count = sum(row.count('black') for row in self.board)
        
        if white_count == 0:
            return 'black'
        elif black_count == 0:
            return 'white'
        return None
    
    def get_valid_moves(self, row, col):
        """Получить все возможные ходы для шашки"""
        valid_moves = []
        if self.board[row][col] == self.current_player:
            for end_row in range(8):
                for end_col in range(8):
                    if self.is_valid_move(row, col, end_row, end_col):
                        valid_moves.append((end_row, end_col))
        return valid_moves
