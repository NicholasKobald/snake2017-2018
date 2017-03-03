from shared import get_pos_from_move


def label_board(board, snake_info):
    for s_id, snake in snake_info.iteritems():
        head = snake['coords'][0]
        label_near_cells(head, board)

        #label the tails
        s_len = len(snake['coords'])
        for dist, head in enumerate(snake['coords']):
            x, y = head
            print "Set component", x, y, "val", s_len - dist
            board.get_tile(x, y).dist_down_snake(s_len - dist)

def score_components(board, head):
    pass


def label_near_cells(head, board, depth=1):
    if depth==3:
        return
    x, y = head
    valid_moves = board.get_valid_moves(x, y)
    for move in valid_moves:
        x, y = get_pos_from_move([x, y], move)
        board.get_tile(x, y).set_threat_time(depth)
        label_near_cells([x, y], board, depth+1)

#uses bfs to determine the coordinates of a component
def get_reachable(board, head):
    visited = [0] * board.width * board.height
    count, que = 0, [head]
    while que:
        head, count = que.pop(), count+1
        valid_moves = board.get_valid_moves(head[0], head[1])
        for move in valid_moves:
            tile = get_pos_from_move(head, move)
            if not visited[board.width * tile[0] + tile[1]]:
                visited[board.width * tile[0] + tile[1]] = True
                que.append(tile)

    return visited

def is_component_safe(board, head):
    my_component = get_reachable(board, head)
    count = my_component.count(True) #size of component
    visited = [False] * board.width * board.height
    visited[board.width * head[0] + head[1]] = True
    return find_path_out(board, head[0], head[1], visited, 0, component)

def find_path_out(board, x, y, visited, depth, component):
    if check_exit(board, x, y, component, depth):
        return True


    for move in ['up', 'down', 'left', 'right']:
        to_x, to_y = get_pos_from_move(head, move)
        if not visited[board.width * to_x + to_y]:
            visited[board.width * to_x + to_y] = True
            find_path_out(board, to_x, to_y, visited, depth+1)

def check_exit(board, x, y, component, depth):
    s = set()
    for move in ['up', 'down', 'left', 'right']:
        m = board.get_pos_from_move([x, y], move)
        if m:
            s.add(m)

    for x, y in s:
        if not component[board.width * x + y] and board.get_tile(x, y).turns_till_safe() < depth:
            return True
