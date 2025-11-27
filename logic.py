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
        
        # Расставляем черные шашки (вверху)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'black'
        
        # Расставляем белые шашки (внизу)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'white'
    
    def print_board(self):
        """Простой вывод доски для тестирования"""
        print("  0 1 2 3 4 5 6 7")
        for row in range(8):
            print(row, end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece == 'white':
                    print('W', end=" ")
                elif piece == 'black':
                    print('B', end=" ")
                else:
                    print('.', end=" ")
            print()
    
    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка валидности хода"""
        # Проверяем границы доски
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and
                0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        
        # Проверяем, что начальная клетка содержит шашку текущего игрока
        if self.board[start_row][start_col] != self.current_player:
            return False
        
        # Проверяем, что конечная клетка пуста
        if self.board[end_row][end_col] != ' ':
            return False
        
        # Проверяем, что ход по диагонали
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
        
        # Простой ход на одну клетку вперед
        if abs(end_row - start_row) == 1:
            if self.current_player == 'white' and end_row == start_row - 1:
                return True
            elif self.current_player == 'black' and end_row == start_row + 1:
                return True
        
        # Взятие шашки (ход на две клетки)
        if abs(end_row - start_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            
            # Проверяем, что между клетками шашка противника
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

# Тестирование логики
if __name__ == "__main__":
    game = CheckersGame()
    print("Начальная доска:")
    game.print_board()
    
    # Тестовый ход белых
    print("\nХод белых с 5,1 на 4,2:")
    if game.make_move(5, 1, 4, 2):
        print("Ход успешен!")
    else:
        print("Неверный ход!")
    
    game.print_board()
