
def label_board_voronoi(board, snake_dict):
    queue = []

    #init que and voironoi info
    for s_id, snake in snake_dict.iteritems():
        x, y = snake['coords'][0]
        tile = board.get_tile(x, y)
        tile.set_voronoi_tile(s_id, 0)
        queue.append([x, y])

    while queue:
        
        cur = queue.pop()
        p_x, p_y =  cur
        parent_tile = board.get_tile(p_x, p_y)
        parent_info = tile.get_voronoi_data()

        for move in ['up', 'down', 'left', 'right']:
            pos = board.get_pos_from_move(cur, move)
            if pos != None:
                x, y = pos
                tile = board.get_tile(x, y)
                tile.set_voronoi_tile(parent_info['snake_ids'], parent_info['path_len']+1)
                queue.append([x, y])


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
