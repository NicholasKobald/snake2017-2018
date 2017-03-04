import random

def init_voronoi(board):
    for i in range(board.width):
        for j in range(board.height):
            tile = board.get_tile(i, j)
            tile.init_voronoi_list()

def label_board_voronoi(board, snake_dict):
    init_voronoi(board)
    queue = []

    voronoi_data = dict()

    for s_id, snake in snake_dict.iteritems():
        voronoi_data[s_id] = dict()
        for m in ['up', 'down', 'left', 'right']:
            voronoi_data[s_id][m] = 0

    #init que and voironoi info
    for s_id, snake in snake_dict.iteritems():
        x, y = snake['coords'][0]
        tile = board.get_tile(x, y)
        tile.set_voronoi_tile(s_id, 0)
        my_tup = [x, y]
        queue.append(dict(from_tuple=my_tup, dist=0, s_id=s_id, move=None))

    #jumpstart the que values.
    for i in range(len(snake_dict)):
        cur = queue.pop(0)
        p_x, p_y =  cur['from_tuple']
        dist = cur['dist']
        init_mov = cur['move']
        parent_tile = board.get_tile(p_x, p_y)
        parent_list = tile.get_voronoi_data() #this is a list of dicts
        parent_info = parent_list[0]
        parent_id = cur['s_id']
        children_list, moves_used = get_children(board, dist+1, [p_x, p_y], parent_info['snake_id'])
        for index, child in enumerate(children_list):
            init_mov = moves_used[index]
            x, y = child
            tile = board.get_tile(x, y)
            tile.set_voronoi_tile(parent_id, dist+1, init_mov)
            voronoi_data[parent_id][init_mov] += 1
            queue.append(dict(from_tuple=[x, y], dist=dist+1, s_id=parent_id, move=init_mov))

    while queue:
        cur = queue.pop(0)
        p_x, p_y =  cur['from_tuple']
        dist = cur['dist']
        init_mov = cur['move']
        parent_tile = board.get_tile(p_x, p_y)
        parent_list = tile.get_voronoi_data() #this is a list of dicts
        parent_info = parent_list[0]
        parent_id = cur['s_id']
        children_list, moves_used = get_children(board, dist+1, [p_x, p_y], parent_info['snake_id'])
        for index, child in enumerate(children_list):
            x, y = child
            tile = board.get_tile(x, y)
            tile.set_voronoi_tile(parent_id, dist+1, init_mov)
            voronoi_data[parent_id][init_mov] += 1
            queue.append(dict(from_tuple=[x, y], dist=dist+1, s_id=parent_id, move=init_mov))

    return voronoi_data

def get_children(board, path_len, cur, snake_id):
    children_list = []
    moves_used = []
    my_move_list =  ['up', 'down', 'left', 'right']
    random.shuffle(my_move_list)
    for move in my_move_list:
        pos = board.get_pos_from_move(cur, move)
        if pos != None and safe_in_time(board, pos, path_len):
            x, y = pos
            tile = board.get_tile(x, y)
            #has been set.
            v_data = tile.get_voronoi_data()
            if len(v_data) > 0:
                v_data = v_data[0]
                cur_best = v_data['path_len']
                assert(path_len >= cur_best)
                if path_len == cur_best and snake_id != v_data['snake_id']:
                    children_list.append(pos)
                    moves_used.append(move)
            else:
                children_list.append(pos)
                moves_used.append(move)

    return children_list, moves_used

def safe_in_time(board, pos, path_len):
    tile = board.get_tile(pos[0], pos[1])
    if not tile.is_snake():
        return True

    #off by 1?
    return path_len > tile.turns_till_safe() + 5




def find_closest_snakes(board, snake_dict):
    '''
    We are building two dictionaries:
    1) 'by_dest': { coord_key_str: [{
                        snake_id: 'snake-007',
                        path_len: 7,
                        coords: [0,7]
                    },
                    ...
                    ]
        }
    2) 'by_snake': { snake_id: [{
                        dest_info: {
                            coords: [1,1],
                            path_len: 7,
                            tied_with: ['snake-006']
                        },
                        coords: [0, 7]
                    },
                    ...
                    ]
        }
    '''
    by_dest, by_snake = dict(), dict()
    for dest_coord in coords_list:
        dest_coord_key_str = coords_to_key_str(dest_coord)
        by_dest[dest_coord_key_str] = []

        visited = [ [False]*board.width for i in range(board.height) ]
        queue = [dict(coords=dest_coord, path_len=0)]
        working_min_path_len = float('inf') # we stop our search once beyond this
        while len(queue) > 0:
            cur_info = queue.pop(0)
            cur_pos, cur_path_len = cur_info['coords'], cur_info['path_len']
            # cancels need for path_len comparison when we find snake_head
            if cur_path_len > working_min_path_len: continue
            cur_col, cur_row = cur_pos[0], cur_pos[1]

            # have we reached our dest?
            if board.get_tile(cur_col, cur_row).is_head():
                working_min_path_len = cur_path_len
                cur_snake_id = board.get_tile(cur_col, cur_row).get_snake_id()
                by_dest = get_new_bydest_dict(dest_coord_key_str,
                                              by_dest,
                                              cur_info,
                                              cur_snake_id)
                by_snake = get_new_bysnake_dict(cur_snake_id,
                                                by_snake,
                                                cur_info['coords'],
                                                dest_coord,
                                                cur_path_len,
                                                by_dest[dest_coord_key_str])
                continue # at working_min_path_len, anything from here is longer

            valid_moves = board.get_valid_moves(cur_col, cur_row)
            for move in ['up', 'down', 'right', 'left']:
                pos = board.get_pos_from_move(cur_pos, move)
                if pos == None or visited[pos[0]][pos[1]]: continue
                # enqueue cell if unoccupied or containing snake head
                if move in valid_moves or board.get_tile(pos[0], pos[1]).is_head():
                    if cur_path_len+1 <= working_min_path_len:
                        queue.append(dict(coords=pos, path_len=(cur_path_len+1)))
                        visited[pos[0]][pos[1]] = True
    return dict(by_dest=by_dest, by_snake=by_snake)
