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
