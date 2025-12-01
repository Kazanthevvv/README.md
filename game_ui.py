from logic import ConsoleCheckersGame

class ConsoleCheckersUI:
    def __init__(self):
        self.game = ConsoleCheckersGame()
    
    def display_board(self):
        board = self.game.get_board()
        
        print("\n   " + " ".join(str(i) for i in range(8)))
        print("  " + "+" + "-" * 15 + "+")
        
        for row in range(8):
            print(f"{row} |", end=" ")
            for col in range(8):
                piece = board[row][col]
                if piece == ' ':
                    symbol = '.' if (row + col) % 2 == 0 else ' '
                elif piece == 'w':
                    symbol = 'O'
                elif piece == 'b':
                    symbol = 'X'
                print(symbol, end=" ")
            print("|")
        
        print("  " + "+" + "-" * 15 + "+")
    
    def run(self):
        print("ШАШКИ ЗАПУЩЕНЫ!")
        print("Формат: строка столбец строка столбец")
        print("Пример: 5 2 4 3")
        
        while True:
            self.display_board()
            print(f"\nХод: {self.game.get_current_player()}")
            
            try:
                input_str = input("Ваш ход: ").strip()
                
                if input_str.lower() == 'quit':
                    break
                
                coords = list(map(int, input_str.split()))
                if len(coords) == 4:
                    from_row, from_col, to_row, to_col = coords
                    if self.game.move_piece(from_row, from_col, to_row, to_col):
                        print("ХОД УСПЕШЕН!")
                    else:
                        print("НЕВЕРНЫЙ ХОД!")
                else:
                    print("НУЖНО 4 ЧИСЛА!")
                    
            except ValueError:
                print("ВВОДИТЕ ТОЛЬКО ЧИСЛА!")
            except KeyboardInterrupt:
                break
        
        print("ИГРА ОКОНЧЕНА!")

if __name__ == "__main__":
    game = ConsoleCheckersUI()
    game.run()
