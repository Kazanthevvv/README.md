class ConsoleCheckersGame:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        
        # Черные шашки
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'b'
        
        # Белые шашки
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'w'
        
        self.current_player = 'white'
        self.game_over = False
    
    def get_board(self):
        return self.board
    
    def get_current_player(self):
        return self.current_player
    
    def is_game_over(self):
        return self.game_over
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        if self.game_over:
            return False
            
        # Простая проверка хода
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False
            
        piece = self.board[from_row][from_col]
        if piece == ' ':
            return False
            
        # Проверяем что ходят своей шашкой
        if (self.current_player == 'white' and piece != 'w') or \
           (self.current_player == 'black' and piece != 'b'):
            return False
        
        # Простой ход (только вперед на 1 клетку)
        if self.current_player == 'white':
            if to_row != from_row - 1 or abs(to_col - from_col) != 1:
                return False
        else:  # black
            if to_row != from_row + 1 or abs(to_col - from_col) != 1:
                return False
        
        # Проверяем что целевая клетка пуста
        if self.board[to_row][to_col] != ' ':
            return False
        
        # Выполняем ход
        self.board[from_row][from_col] = ' '
        self.board[to_row][to_col] = piece
        
        # Смена игрока
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
