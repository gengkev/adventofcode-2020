#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 24
YEAR = 2020


DIRS = {
    'e': (2, 0),
    'se': (1, -1),
    'sw': (-1, -1),
    'w': (-2, 0),
    'nw': (-1, 1),
    'ne': (1, 1),
}

def vec_add(x, y):
    return tuple(a+b for a, b in zip(x,y))

def bfs(graph, start):
    visited = set()
    order = []
    q = deque([start])

    while q:
        cur = q.popleft()

        if cur in visited:
            continue
        visited.add(cur)
        order.append(cur)

        for nbr in graph[cur]:
            q.append(nbr)

    return order


##########################################################################


def main(A):
    grid = None

    # Solve part 1
    def part1():
        nonlocal grid
        grid = defaultdict(lambda: 0)
        for line in A:
            pos = (0,0)
            for token in line:
                pos = vec_add(pos, DIRS[token])
            grid[pos] = 1 - grid[pos]

        return sum(grid.values())

    res = part1()
    submit_1(res)

    orig_grid = dict(grid)

    def get_nbrs(pos):
        out = []
        for _, vec in DIRS.items():
            npos = vec_add(pos, vec)
            out.append(npos)
        return out

    # Solve part 2
    def part2():
        grid = dict(orig_grid)
        print(sum(grid.values()))
        next_grid = dict()

        # add nbrs of all existing tiles
        hack = []
        for pos in grid:
            for npos in get_nbrs(pos):
                if npos not in grid:
                    hack.append(npos)
        for npos in hack:
            grid[npos] = 0

        # run simulation
        for rnd in range(100):
            for pos in grid:
                # count num black neighbors
                pos_count = 0
                for npos in get_nbrs(pos):
                    if npos in grid:
                        pos_count += grid[npos]
                    else:
                        next_grid[npos] = 0

                # compute next value
                next_grid[pos] = grid[pos]
                if grid[pos] == 1:
                    if pos_count == 0 or pos_count > 2:
                        next_grid[pos] = 0
                elif grid[pos] == 0:
                    if pos_count == 2:
                        next_grid[pos] = 1

            grid = next_grid
            next_grid = dict()
            print('after round', rnd, sum(grid.values()))

        return sum(grid.values())



    res = part2()
    submit_2(res)


##########################################################################

def parse_line(line):
    i = 0
    tokens = []
    while i < (len(line)):
        if line[i] in 'sn':
            tokens.append(line[i:i+2])
            i += 2
        else:
            assert line[i] in 'ew'
            tokens.append(line[i])
            i += 1

    return tokens


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]

    # One line per input
    #A = A[0]

    return A


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
