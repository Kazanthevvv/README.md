from logic import CheckersGame

class CheckersUI:
    def __init__(self):
        self.game = CheckersGame()
    
    def display_board(self):
        """Красивое отображение доски"""
        print("\n   0 1 2 3 4 5 6 7")
        print("  +-+-+-+-+-+-+-+-+")
        for row in range(8):
            print(f"{row} |", end="")
            for col in range(8):
                piece = self.game.board[row][col]
                if piece == 'white':
                    print('W|', end="")
                elif piece == 'black':
                    print('B|', end="")
                else:
                    print(' |', end="")
            print("\n  +-+-+-+-+-+-+-+-+")
    
    def get_move_input(self):
        """Получение хода от игрока"""
        try:
            print(f"\nХод игрока: {self.game.current_player}")
            print("Введите координаты от 0 до 7")
            start_row = int(input("Стартовая строка: "))
            start_col = int(input("Стартовый столбец: "))
            end_row = int(input("Конечная строка: "))
            end_col = int(input("Конечный столбец: "))
            return start_row, start_col, end_row, end_col
        except ValueError:
            print("❌ Ошибка! Вводите только числа от 0 до 7.")
            return None
    
    def play_game(self):
        """Основной игровой цикл"""
        print("\n=== ИГРА В ШАШКИ ===")
        print("Белые (W) ходят первыми, Черные (B)")
        print("Ходите по диагонали: белые - вверх, черные - вниз")
        
        while True:
            self.display_board()
            
            winner = self.game.get_winner()
            if winner:
                print(f"\n🎉 Победили {winner}!")
                break
            
            move = self.get_move_input()
            if move is None:
                continue
            
            start_row, start_col, end_row, end_col = move
            
            if self.game.make_move(start_row, start_col, end_row, end_col):
                print("✅ Ход выполнен!")
            else:
                print("❌ Неверный ход! Попробуйте снова.")

if __name__ == "__main__":
    ui = CheckersUI()
    ui.play_game()
