import numpy as np
from state import UltimateTTT_Move
import copy
import time

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    # print(cur_state.count_O)
    # if cur_state.count_O < 5:
    #     print("Random choise")
    #     return np.random.choice(valid_moves)
    count_O = len(np.where(cur_state.blocks == cur_state.O)[0])
    depth = 1
    if count_O < 5:
        # print("Random choice")
        return np.random.choice(valid_moves)

    utility, action = minimax(cur_state,cur_state.player_to_move, 1, -float('inf'), +float('inf'))
    # print(utility)
    if action:
        # print("=================================================================")
        return action
    else:
        # print("Random choice")
        if len(valid_moves) != 0:
            return np.random.choice(valid_moves)
    # return np.random.choice(valid_moves)

# def find_win_positions(block, player):
#     best = -float('inf')
#     pos = []
#     for i in range (0,3):
#         for j in range(0,3):
#             previous_move = UltimateTTT_Move(2, i, j, player)
#             if (block[i,j] != 0):
#                 continue
#             new_block = copy.deepcopy(block)
#             new_block[i,j] = player
#             # print("x: ", i, " y:", j)
#             score = evaluate_block(new_block, player, previous_move)
#             if (score > best):
#                 best = score
#                 pos = (i,j)
#             # print("Score: ", score)
#     return pos
def reduce_moves(cur_state, moves):
    # winable_block = []
    print("Waiting to reduces move.........")
    # time.sleep(10)
    winable_block_indices = []
    for i in range(9):
        block = cur_state.blocks[i]
        if cur_state.global_cells[i] == 0 and count_positions_can_win(block, cur_state.player_to_move) >= 1:
            # winable_block.append(block)
            winable_block_indices.append(i)
    
    if len(winable_block_indices) == 0:
        random_local_index = np.random.choice(np.array(range(9)))
        filter_func = lambda move: move.index_local_board == random_local_index
        return list(filter(filter_func, moves))
    
    best_block_idx = -1
    max_score = -float('inf')
    win_pos = []
    # for local_index in winable_block_indices:
    #     # Evaluate global board
    #     new_global_cells = copy.deepcopy(np.reshape(cur_state.global_cells, (3, 3)))
    #     pos_x = local_index // 3
    #     pos_y = local_index % 3
    #     new_global_cells[pos_x, pos_y]
    #     score = evaluate_block(new_global_cells, cur_state.player_to_move, 
    #                             UltimateTTT_Move(local_index, pos_x, pos_y
    #                                             , cur_state.player_to_move ))

    #     if (score > max_score):
    #         max_score = score
    #         best_block_idx = local_index


    #     # Find win pos
    #     pos = find_win_positions(cur_state.blocks[local_index], cur_state.player_to_move)

    filter_func = lambda move: move.index_local_board in winable_block_indices
    ret = list(filter(filter_func, moves))
    return ret

def minimax(gameState, player, depth, alpha, beta):
    if gameState.game_over or depth == 0:
        # print(gameState.previous_move.value)
        # print("Value", evaluate(gameState))
        return (evaluate(gameState), UltimateTTT_Move(-1, -1, -1, 0))

    moves = gameState.get_valid_moves
    # if gameState.free_move:
    #     print("before reduce, moves: ", len(moves))
    #     moves = reduce_moves(gameState, moves)
    #     print("after reduce, moves: ", len(moves))

    # For maximize plyer
    if player == 1:
        value = float('-inf')
        best_move = None 
        for action in moves:
            new_state = copy.deepcopy(gameState)
            new_state.act_move(action)
            # print(f"Max({action.x},{action.y})")
            score, _ = minimax(new_state, -player, depth - 1, alpha, beta)
            # print(f"Max({action.x},{action.y}) - board {action.index_local_board} Value: {score}")
            if score > value    :
                value = score
                best_move = action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return value, best_move
    
    # For minimize player
    else:
        # print("TỚi lượt min", "Trước khi tìm kiếm", "Depth: ", depth)
        # print("Alpha: ", alpha, "Beta: ", beta)
        value = float('inf')
        best_move = None
        for action in moves:
            new_state = copy.deepcopy(gameState)
            new_state.act_move(action)
            # print(f"Min({action.x},{action.y})")
            score, _ = minimax(new_state, -player, depth - 1, alpha, beta)
            # print ("Value: ", score, "at depth", depth)
            # print(f"Min({action.x},{action.y}) - board {action.index_local_board} - Value: {result[0]}")
            if score < value:
               value = score
               best_move = action
            beta = min(beta, score)
            if beta <= alpha:
                break
        return value, best_move

def evaluate(cur_state):
    game_result = cur_state.game_result(np.reshape(cur_state.global_cells, (3, 3)))

    score = 0 
    previous_move = cur_state.previous_move
    cur_block = cur_state.blocks[previous_move.index_local_board]
    cur_player = cur_state.previous_move.value
    if game_result is None:
        game_result = 0 
    elif game_result != 0 :
        return float('inf')*game_result
    
    # Win block + 100 điểm
    # Nếu ở win ở nhiều vị trí => + bonus nếu vị trí đó thuận lợi
    cur_block_result = cur_state.game_result(cur_block)
    if cur_block_result is not None:
        # print("Win the curent block", previous_move.index_local_board)
        # print(cur_state.blocks[previous_move.index_local_board])
        score += 100 * cur_block_result
        local_board_pos = previous_move.index_local_board // 3, previous_move.index_local_board % 3
        score += cur_block_result * evaluate_block(np.reshape(cur_state.global_cells, (3,3)), 
                                        cur_player, UltimateTTT_Move(-1,local_board_pos[0], local_board_pos[1] , cur_player))
    

    # Chọn vị trí tốt nhất trong block hiện tại
    else: 
        score += cur_player * evaluate_block(cur_block, cur_player, previous_move)
    
    # print(cur_state.global_cells, "Globals_cell", np.sum(cur_state.global_cells))
    return (score + np.sum(cur_state.global_cells) * 100)

def count_player_in_block(cur_block, player):
    return np.count_nonzero(cur_block == player)

def evaluate_block(block, player_maker, previous_move):
    # print(block)
    count_opponent_wins_pos = count_positions_can_win(block, player_maker * -1)
    count_owner_wins_pos = count_positions_can_win(block, player_maker)
    score = 0

    count_opponent_pos = count_player_in_block(block, player_maker * -1)
    count_owner_pos = count_player_in_block(block, player_maker)

    if count_opponent_pos == 0:
        # print("Đối thủ chưa có quân nào")
        if count_owner_pos == 1:
            # print("Quân đầu tiên đánh ở góc")
            score += 2 if (previous_move.x, previous_move.y) in [(0, 0), (0, 2), (2, 0), (2, 2)] else 0
        elif count_owner_pos == 2:
            # print("Quân thứ 2 đánh ở trung tâm")
            score += 2 if (previous_move.x, previous_move.y) in [(1, 1)] else 0
    else:
        # print("Nếu đối thủ đánh ở góc")
        if count_owner_pos == 1 and count_opponent_pos == 1:
            # print("phải đánh ở ô trung tâm")
            position = np.where(block == player_maker * -1)
            if (position[0][0], position[1][0]) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                score += 3 if (previous_move.x, previous_move.y) == (1, 1) else 0
            else:
                score += 2 if (previous_move.x, previous_move.y) in [(0, 0), (0, 2), (2, 0), (2, 2)] else 0
        else:
            score += 1 if (previous_move.x, previous_move.y) in [(1, 1)] else 0
            score += 1 if (previous_move.x, previous_move.y) in [(0, 0), (0, 2), (2, 0), (2, 2)] else 0

    if count_opponent_wins_pos >= 2:
        score -= (11)

    if count_opponent_wins_pos >= 1:
        score -= 6

    if count_owner_wins_pos >= 2:
        score += 10  # Ưu tiên chặn đối thủ nếu đánh sau

    if count_owner_wins_pos >= 1:
        score += 5  # Ưu tiên chặn đối thủ nếu đánh sau
    # print (score)
    return score


def count_positions_can_win(cur_block, player_maker):
    # Kiểm tra theo hàng
    row_wins = np.sum((np.count_nonzero(cur_block == player_maker, axis=1) == 2) & (np.count_nonzero(cur_block == 0, axis=1) == 1))

    # Kiểm tra theo cột
    col_wins = np.sum((np.count_nonzero(cur_block == player_maker, axis=0) == 2) & (np.count_nonzero(cur_block == 0, axis=0) == 1))

    # Kiểm tra trường hợp dấu +
    if (cur_block[0][1] == cur_block[2][1] == cur_block[1][0] == cur_block[1][2] == player_maker) and cur_block[1][1] == 0:
        row_wins -= 1

    # Kiểm tra theo đường chéo chính
    diag1_win = 1 if (  cur_block[0][0] == cur_block[1][1] == player_maker and cur_block[2][2] == 0) or (
                        cur_block[0][0] == cur_block[2][2] == player_maker and cur_block[1][1] == 0) or (
                        cur_block[1][1] == cur_block[2][2] == player_maker and cur_block[0][0] == 0) else 0

    # Kiểm tra theo đường chéo phụ
    diag2_win = 1 if (  cur_block[0][2] == cur_block[1][1] == player_maker and cur_block[2][0] == 0) or (
                        cur_block[0][2] == cur_block[2][0] == player_maker and cur_block[1][1] == 0) or (
                        cur_block[2][0] == cur_block[1][1] == player_maker and cur_block[0][2] == 0) else 0

    # Kiểm tra trường hợp dấu nhân
    if (cur_block[0][0] == cur_block[2][2] == cur_block[0][2] == cur_block[2][0] == player_maker) and cur_block[1][1] != player_maker:
        diag1_win -= 1

    total_wins = row_wins + col_wins + diag1_win + diag2_win
    return total_wins


