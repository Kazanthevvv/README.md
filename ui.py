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
