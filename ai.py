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
