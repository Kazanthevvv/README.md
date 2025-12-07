import random

board = []
current_player = 'w'
game_over = False

# Сергей
def setup_board():
    global board
    board = []
    for row in range(8):
        board.append([0] * 8)
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'b'
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'w'

def get_captures(row, col, piece, captured_path):
    captures = []
    is_king = piece in ['W', 'B']
    color = piece.lower()
    directions = []
    if piece == 'w' or is_king:
        directions.append((-1, -1))
        directions.append((-1, 1))
    if piece == 'b' or is_king:
        directions.append((1, -1))
        directions.append((1, 1))
    for dr, dc in directions:
        jump_row, jump_col = row + dr, col + dc
        if 0 <= jump_row < 8 and 0 <= jump_col < 8:
            jump_piece = board[jump_row][jump_col]
            if jump_piece != 0 and jump_piece.lower() != color:
                land_row, land_col = jump_row + dr, jump_col + dc
                if 0 <= land_row < 8 and 0 <= land_col < 8:
                    if board[land_row][land_col] == 0:
                        if (jump_row, jump_col) not in captured_path:
                            new_captured = captured_path + [(jump_row, jump_col)]
                            further_captures = get_captures(land_row, land_col, piece, new_captured)
                            if further_captures:
                                for fc in further_captures:
                                    captures.append((land_row, land_col, fc[2]))
                            else:
                                captures.append((land_row, land_col, new_captured))
    return captures

def get_piece_moves(row, col):
    piece = board[row][col]
    if piece == 0:
        return [], []
    moves = []
    is_king = piece in ['W', 'B']
    color = piece.lower()
    directions = []
    if piece == 'w' or is_king:
        directions.append((-1, -1))
        directions.append((-1, 1))
    if piece == 'b' or is_king:
        directions.append((1, -1))
        directions.append((1, 1))
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == 0:
                moves.append((new_row, new_col, []))
    captures = get_captures(row, col, piece, [])
    return moves, captures

def get_all_moves():
    global current_player
    all_moves = []
    all_captures = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != 0 and piece.lower() == current_player:
                moves, captures = get_piece_moves(row, col)
                if captures:
                    for capture in captures:
                        all_captures.append(((row, col), (capture[0], capture[1]), capture[2]))
                elif not all_captures:
                    for move in moves:
                        all_moves.append(((row, col), (move[0], move[1])))
    if all_captures:
        max_captures = max(len(capture[2]) for capture in all_captures)
        best_captures = [cap for cap in all_captures if len(cap[2]) == max_captures]
        return [], best_captures
    return all_moves, []

def make_move(from_pos, to_pos, captures=[]):
    global current_player
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    piece = board[from_row][from_col]
    board[to_row][to_col] = piece
    board[from_row][from_col] = 0
    for cap_row, cap_col in captures:
        board[cap_row][cap_col] = 0
    if piece == 'w' and to_row == 0:
        board[to_row][to_col] = 'W'
    elif piece == 'b' and to_row == 7:
        board[to_row][to_col] = 'B'
    if captures:
        _, further_captures = get_piece_moves(to_row, to_col)
        valid_further = []
        for cap in further_captures:
            if any(pos not in captures for pos in cap[2]):
                valid_further.append(cap)
        if valid_further:
            max_captures = max(len(cap[2]) for cap in valid_further)
            best_captures = [cap for cap in valid_further if len(cap[2]) == max_captures]
            if best_captures:
                return best_captures
    current_player = 'b' if current_player == 'w' else 'w'
    return None

def check_game_over():
    global current_player
    white_pieces = 0
    black_pieces = 0
    original_player = current_player
    current_player = 'w'
    moves_white, captures_white = get_all_moves()
    white_moves = moves_white + captures_white
    current_player = 'b'
    moves_black, captures_black = get_all_moves()
    black_moves = moves_black + captures_black
    current_player = original_player
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != 0:
                if piece.lower() == 'w':
                    white_pieces += 1
                else:
                    black_pieces += 1
    if white_pieces == 0 or not white_moves:
        return 'b'
    elif black_pieces == 0 or not black_moves:
        return 'w'
    return None

# Рамиль
def get_ai_move():
    moves, captures = get_all_moves()
    if captures:
        return random.choice(captures)
    elif moves:
        return random.choice(moves)
    else:
        return None

def computer_turn():
    global game_over
    print("\nХод компьютера...")
    move = get_ai_move()
    if move is None:
        print("У компьютера нет ходов!")
        return False
    if len(move) == 3:
        from_pos, to_pos, captures = move
        print(f"Компьютер делает ход: {from_pos} -> {to_pos} (взято шашек: {len(captures)})")
        further_moves = make_move(from_pos, to_pos, captures)
        while further_moves:
            next_move = random.choice(further_moves)
            from_pos = to_pos
            to_pos = (next_move[0], next_move[1])
            captures = next_move[2]
            print(f"Продолжение взятия: {from_pos} -> {to_pos}")
            further_moves = make_move(from_pos, to_pos, captures)
    else:
        from_pos, to_pos = move
        print(f"Компьютер делает ход: {from_pos} -> {to_pos}")
        make_move(from_pos, to_pos)
    return True

# Иван
def print_board():
    print("\n  " + " ".join(str(i) for i in range(8)))
    print("  " + "-" * 17)
    for row in range(8):
        print(f"{row}|", end=" ")
        for col in range(8):
            cell = board[row][col]
            if cell == 0:
                print(".", end=" ")
            elif cell == 'w':
                print("○", end=" ")
            elif cell == 'b':
                print("●", end=" ")
            elif cell == 'W':
                print("◎", end=" ")
            elif cell == 'B':
                print("◉", end=" ")
        print(f"|{row}")
    print("  " + "-" * 17)
    print("  " + " ".join(str(i) for i in range(8)))
    print(f"\nХод: {'Белых' if current_player == 'w' else 'Черных'}")

def get_player_input(moves, captures):
    while True:
        try:
            if captures:
                choice = input("Выберите номер взятия (или введите координаты вручную): ")
                if choice.isdigit():
                    idx = int(choice)
                    if 0 <= idx < len(captures):
                        from_pos, to_pos, cap_list = captures[idx]
                        return (from_pos, to_pos, cap_list)
            else:
                choice = input("Выберите номер хода (или введите координаты вручную): ")
                if choice.isdigit():
                    idx = int(choice)
                    if 0 <= idx < len(moves):
                        from_pos, to_pos = moves[idx]
                        return (from_pos, to_pos)
            coords = list(map(int, choice.split()))
            if len(coords) == 4:
                from_pos = (coords[0], coords[1])
                to_pos = (coords[2], coords[3])
                if captures:
                    for cap_from, cap_to, cap_list in captures:
                        if from_pos == cap_from and to_pos == cap_to:
                            return (from_pos, to_pos, cap_list)
                elif moves:
                    for move_from, move_to in moves:
                        if from_pos == move_from and to_pos == move_to:
                            return (from_pos, to_pos)
            print("Недопустимый ход. Попробуйте снова.")
        except (ValueError, IndexError):
            print("Некорректный ввод. Попробуйте снова.")

def handle_further_captures(further_moves, from_pos, captured):
    while further_moves:
        print_board()
        print(f"Продолжение взятия! Вы взяли {len(captured)} шашек.")
        print("Возможные продолжения:")
        for i, (_, next_to, next_caps) in enumerate(further_moves):
            additional = len(next_caps) - len(captured)
            print(f"  {i}: {from_pos} -> {next_to} (дополнительно берет {additional} шашек)")
        while True:
            try:
                choice = input("Выберите продолжение (или 0 чтобы закончить ход): ")
                if choice == '0':
                    return
                idx = int(choice)
                if 0 <= idx < len(further_moves):
                    next_move = further_moves[idx]
                    new_to = (next_move[0], next_move[1])
                    new_caps = next_move[2]
                    make_move(from_pos, new_to, new_caps)
                    from_pos = new_to
                    captured = new_caps
                    further_moves = get_piece_moves(from_pos[0], from_pos[1])[1]
                    break
                else:
                    print("Неверный выбор.")
            except ValueError:
                print("Введите число.")

def human_turn():
    global game_over
    moves, captures = get_all_moves()
    if not moves and not captures:
        print(f"У игрока нет ходов!")
        return False
    print(f"\nВозможные ходы:")
    if captures:
        print("Обязательные взятия:")
        for i, (from_pos, to_pos, cap_list) in enumerate(captures):
            print(f"  {i}: {from_pos} -> {to_pos} (берет {len(cap_list)} шашек)")
    elif moves:
        print("Простые ходы:")
        for i, (from_pos, to_pos) in enumerate(moves):
            print(f"  {i}: {from_pos} -> {to_pos}")
    move_data = get_player_input(moves, captures)
    if not move_data:
        return False
    if captures:
        from_pos, to_pos, cap_list = move_data
        further_moves = make_move(from_pos, to_pos, cap_list)
        handle_further_captures(further_moves, to_pos, cap_list)
    else:
        from_pos, to_pos = move_data
        make_move(from_pos, to_pos)
    return True

def play_game(vs_computer=False):
    global game_over, current_player
    setup_board()
    current_player = 'w'
    game_over = False
    print("=" * 50)
    print("ШАШКИ")
    print("=" * 50)
    print("Правила:")
    print("1. Первыми ходят белые (○)")
    print("2. Взятие обязательно")
    print("3. При нескольких вариантах взятия выбирается тот, где берется больше шашек")
    print("4. Дамки обозначаются: ◎ (белая) и ◉ (черная)")
    print("5. Для хода вводите координаты в формате: row col (например: 5 4)")
    print("=" * 50)
    computer_color = 'b' if vs_computer else None
    while not game_over:
        print_board()
        if vs_computer and current_player == computer_color:
            if not computer_turn():
                break
        else:
            if not human_turn():
                break
        winner = check_game_over()
        if winner:
            print_board()
            if winner == 'w':
                print("\n" + "=" * 50)
                print("ПОБЕДА БЕЛЫХ!")
                print("=" * 50)
            else:
                print("\n" + "=" * 50)
                print("ПОБЕДА ЧЕРНЫХ!")
                print("=" * 50)
            game_over = True
    print("\nИгра окончена!")

def main():
    print("Добро пожаловать в игру ШАШКИ!")
    print("\nВыберите режим игры:")
    print("1. Игра против человека")
    print("2. Игра против компьютера")
    while True:
        choice = input("Ваш выбор (1-2): ")
        if choice == '1':
            play_game(vs_computer=False)
            break
        elif choice == '2':
            play_game(vs_computer=True)
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
