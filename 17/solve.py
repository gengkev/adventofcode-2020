#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 17
YEAR = 2020


def vec_add(x, y):
    return tuple(a+b for a, b in zip(x,y))

##########################################################################

def get_nbrs(pos):
    out = []
    for vec in itertools.product(range(-1, 2), repeat=len(pos)):
        if not any(vec):
            continue
        npos = vec_add(pos, vec)
        out.append(npos)
    return out

def solve(grid):
    next_grid = dict()

    for rnd in range(6):
        # add all neighbors of existing
        hack = []
        for pos in grid:
            for npos in get_nbrs(pos):
                if npos not in grid:
                    hack.append(npos)
        for npos in hack:
            grid[npos] = 0

        for pos in grid:
            # count num active neighbors
            pos_count = 0
            for npos in get_nbrs(pos):
                if npos in grid:
                    pos_count += grid[npos]

            # compute next value
            if grid[pos] == 1:
                if pos_count in (2, 3):
                    next_grid[pos] = 1
            elif grid[pos] == 0:
                if pos_count == 3:
                    next_grid[pos] = 1

        grid = next_grid
        next_grid = dict()
        print('after round', rnd, sum(grid.values()))
        #print(grid)

    return sum(grid.values())

def main(A):

    # Solve part 1
    def part1():
        grid = dict()
        for i, line in enumerate(A):
            for j, c in enumerate(line):
                if c == '#':
                    grid[(i, j, 0)] = 1
        return solve(grid)


    res = part1()
    submit_1(res)


    # Solve part 2
    def part2():
        grid = dict()
        for i, line in enumerate(A):
            for j, c in enumerate(line):
                if c == '#':
                    grid[(i, j, 0, 0)] = 1
        return solve(grid)


    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()

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
