import random
from copy import deepcopy
from TetrisSettings import *


###########################
# Board Helper Algorithms #
###########################

def check_collision(board, tile_shape, offsets):
    for cy, row in enumerate(tile_shape):
        for cx, val in enumerate(row):
            if val == 0:
                continue
            try:
                if board[cy + offsets[1]][cx + offsets[0]]:
                    return True
            except IndexError:
                return True
    return False

def get_effective_height(board, tile, offsets):
    offset_x, offset_y = offsets
    #as long as no piece overlap occurs, effective heigh increases by one
    while not check_collision(board, tile, (offset_x, offset_y)):
        offset_y += 1
    return offset_y - 1


def get_rotated_tile(tile):
    return list(zip(*reversed(tile)))