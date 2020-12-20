#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 20
YEAR = 2020


def add_vec(a, b):
    return tuple(map(sum, zip(a, b)))


##########################################################################

# flip vertically
def flip_tile(tile):
    return tile[::-1]

# rotate left 90 deg
def rot_tile(tile, direction):
    N = len(tile)
    assert len(tile[0]) == N

    if direction == 0:
        return tile
    elif direction == 1:
        # 90 degrees left
        return tuple(
            tuple(tile[j][N-1-i] for j in range(N))
            for i in range(N)
        )
    elif direction == 2:
        # 180 degrees
        return tuple(
            tuple(tile[N-1-i][N-1-j] for j in range(N))
            for i in range(N)
        )
    elif direction == 3:
        # 90 degrees right
        return tuple(
            tuple(tile[N-1-j][i] for j in range(N))
            for i in range(N)
        )

#     0
#  3     1
#     2
def get_edge_num(tile, i):
    return rot_tile(tile, i)[0]

def get_edges(tile):
    flipped = flip_tile(tile)
    return [get_edge_num(tile, i) for i in range(4)] + \
            [get_edge_num(flipped, i) for i in range(4)]

def get_all_transforms(tile):
    flipped = flip_tile(tile)
    return [rot_tile(tile, i) for i in range(4)] + \
            [rot_tile(flipped, i) for i in range(4)]

def tile_tostr(tile):
    return '\n'.join(''.join(line) for line in tile)

def main(A):
    def find_adj(cur_idx):
        adj = {}
        cur_edges = get_edges(A[cur_idx])
        for other_idx in A:
            if cur_idx == other_idx:
                continue
            other_edges = set(get_edges(A[other_idx]))
            for edge_idx in range(4):
                if cur_edges[edge_idx] in other_edges:
                    adj[edge_idx] = other_idx
                    break
        return adj

    all_adj = {}

    # Solve part 1
    def part1():
        nonlocal all_adj
        out = 1
        for tile_idx in A:
            adj = find_adj(tile_idx)
            print('adj', tile_idx, adj)
            all_adj[tile_idx] = adj
            if len(adj) == 2:
                print('this one has two adj!')
                out *= tile_idx
        return out

    res = part1()
    submit_1(res)

    def find_first_tile():
        for tile_idx in A:
            if len(all_adj[tile_idx]) == 2:
                break
        else:
            assert False
        print('the first tile will be', tile_idx)
        tile = A[tile_idx]

        # find the two edge numbers that are adjacent
        edges = [get_edge_num(A[tile_idx], i) for i in range(4)]
        edge_idx_0, edge_idx_1 = all_adj[tile_idx].keys()
        print('the golden edges are', edge_idx_0, edges[edge_idx_0])
        print('the golden edges are', edge_idx_1, edges[edge_idx_1])
        assert (edge_idx_0 - edge_idx_1) % 4 in [1, 3]

        # we want the edges to be at locations 1 and 2
        # so we need to rotate this tile until that is true
        for i in range(4):
            if set([(edge_idx_0 - i) % 4, (edge_idx_1 - i) % 4]) == set([1, 2]):
                break
        else:
            assert False

        new_tile = rot_tile(tile, i)
        print('the new tile will be rotated by this many steps', i)
        print(tile_tostr(new_tile))

        new_tile_adj = dict(((k-i)%4, v) for k, v in all_adj[tile_idx].items())
        print('the new tile adj is', new_tile_adj)
        return (new_tile, new_tile_adj)


    # Solve part 2
    def part2():
        # find width of big image
        N = 1
        while N * N < len(A):
            N += 1
        assert N * N == len(A)
        print('found N', N)

        # need to reconstruct the actual image
        # first, find a tile with two edges
        first_tile, first_tile_adj = find_first_tile()

        # construct out image
        out_img = [[None for _ in range(N)] for _ in range(N)]
        out_img[0][0] = (first_tile, first_tile_adj)

        # start a queue
        q = deque([(0, 0)])

        def edge_idx_to_vec(edge_idx):
            if edge_idx == 0: return (-1, 0)
            if edge_idx == 1: return (0, 1)
            if edge_idx == 2: return (1, 0)
            if edge_idx == 3: return (0, -1)
            assert False

        def edge_idx_opp(edge_idx):
            return (edge_idx + 2) % 4

        def edge_idx_flip_vert(edge_idx):
            if edge_idx == 0: return 2
            if edge_idx == 1: return 1
            if edge_idx == 2: return 0
            if edge_idx == 3: return 3
            assert False

        # go
        visited = set()
        while q:
            grid_i, grid_j = q.popleft()
            if (grid_i, grid_j) in visited:
                continue
            visited.add((grid_i, grid_j))

            print('visiting', grid_i, grid_j)

            # read out_img
            cur_tile, cur_tile_adj = out_img[grid_i][grid_j]

            for edge_idx, next_tile_idx in cur_tile_adj.items():
                next_i, next_j = add_vec((grid_i, grid_j), edge_idx_to_vec(edge_idx))
                print('going in directionedge_idx', edge_idx, 'we get', next_i, next_j)
                assert 0 <= next_i < N
                assert 0 <= next_j < N

                next_edge = get_edge_num(cur_tile, edge_idx)[::-1]
                next_edge_idx = edge_idx_opp(edge_idx)

                for rot_id, next_tile in enumerate(get_all_transforms(A[next_tile_idx])):
                    if get_edge_num(next_tile, next_edge_idx) == next_edge:
                        break
                else:
                    print('the edge we are looking for is', ''.join(next_edge))
                    print('the tile we are looking at is')
                    print(tile_tostr(A[next_tile_idx]))
                    assert False

                # compute new adj
                next_tile_adj = all_adj[next_tile_idx]
                if rot_id >= 4:
                    next_tile_adj = dict((edge_idx_flip_vert(k), v) for k, v in next_tile_adj.items())
                next_tile_adj = dict(((k-rot_id)%4, v) for k, v in next_tile_adj.items())

                # put it in the map
                out_img[next_i][next_j] = (next_tile, next_tile_adj)
                print('putting in next tile at coords', next_i, next_j)
                print('the next tile, rotated:')
                print(tile_tostr(next_tile))
                print('the next tile adj:')
                print(next_tile_adj)
                print('==========')

                q.append((next_i, next_j))

        # print the big grid
        big_grid = [[ None for _ in range(N*10) ] for _ in range(N*10)]
        for grid_i in range(N):
            for grid_j in range(N):
                tile = out_img[grid_i][grid_j][0]
                for i in range(10):
                    for j in range(10):
                        big_grid[grid_i*10+i][grid_j*10+j] = tile[i][j]

        print(tile_tostr(big_grid))

        # now get rid of borders
        big_grid = [[ None for _ in range(N*8) ] for _ in range(N*8)]
        for grid_i in range(N):
            for grid_j in range(N):
                tile = out_img[grid_i][grid_j][0]
                for i in range(8):
                    for j in range(8):
                        big_grid[grid_i*8+i][grid_j*8+j] = tile[i+1][j+1]

        print(tile_tostr(big_grid))

        BIGGRID_N = len(big_grid)
        SEAMON_PATT = (
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ',
        )
        SEAMON_N = len(SEAMON_PATT)
        SEAMON_M = len(SEAMON_PATT[0])

        def matches_seamon(grid, in_i, in_j):
            for i in range(SEAMON_N):
                for j in range(SEAMON_M):
                    if SEAMON_PATT[i][j] == '#':
                        if grid[in_i+i][in_j+j] != '#':
                            return False
            return True

        def get_orig_pos(i, j, rot_id):
            # un-rotate
            if rot_id%4 == 0:
                pass
            elif rot_id%4 == 1:
                i, j = j, BIGGRID_N-1-i
            elif rot_id%4 == 2:
                i, j = BIGGRID_N-1-i, BIGGRID_N-1-j
            elif rot_id%4 == 3:
                i, j = BIGGRID_N-1-j, i
            else:
                assert False

            # un-flip
            if rot_id >= 4:
                i = BIGGRID_N-1-i
            return i, j

        seamon_set = set()
        for rot_id, big_grid_rot in enumerate(get_all_transforms(big_grid)):
            for i in range(BIGGRID_N - SEAMON_N):
                for j in range(BIGGRID_N - SEAMON_M):
                    if matches_seamon(big_grid_rot, i, j):
                        print('found seamon', rot_id, i, j)
                        # mark the seamon
                        for si in range(SEAMON_N):
                            for sj in range(SEAMON_M):
                                if SEAMON_PATT[si][sj] == '#':
                                    assert big_grid_rot[i+si][j+sj] == '#'
                                    orig_i, orig_j = get_orig_pos(i+si, j+sj, rot_id)
                                    seamon_set.add((orig_i, orig_j))

        # find all # not in seamon_set
        cnt = 0
        for i in range(BIGGRID_N):
            for j in range(BIGGRID_N):
                if big_grid[i][j] == '#' and (i, j) not in seamon_set:
                    cnt += 1
        return cnt



    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()

    i = 0
    tiles = {}
    while i < len(A):
        tile_num = int(A[i].split()[1][:-1])
        tile_val = A[i+1:i+11]
        tile_val = tuple(map(tuple, tile_val))
        tiles[tile_num] = tile_val
        i += 12

    return tiles


##########################################################################


def submit_1(res):
    print('Part 1', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_a = res


def submit_2(res):
    print('Part 2', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_b = res


##########################################################################


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1].startswith('s'):
        A = open('sample.txt').read()
        is_sample = True
    else:
        puzzle = aocd.models.Puzzle(day=DAY, year=YEAR)
        A = puzzle.input_data
    main(parse_input(A))
