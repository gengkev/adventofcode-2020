#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 11
YEAR = 2020


##########################################################################


DIRS = [
    (1,-1),
    (1,0),
    (1,1),
    (0,1),
    (0,-1),
    (-1,-1),
    (-1,0),
    (-1,1),
]

def main(A):
    N, M = len(A), len(A[0])

    # Solve part 1
    def part1():
        arr = [list(line) for line in A]
        next_arr = [[None for _ in range(M)] for _ in range(N)]

        def get_nbrs(pos):
            x, y = pos
            return [(xx, yy) for xx, yy in [
                (x+1,y-1),
                (x+1,y),
                (x+1,y+1),
                (x,y+1),
                (x,y-1),
                (x-1,y-1),
                (x-1,y),
                (x-1,y+1)
            ]
            if 0 <= xx < N and 0 <= yy < M
            ]

        def count_nbr_occup(pos):
            nbrs = get_nbrs(pos)
            cnt = 0
            for nbr in nbrs:
                if get(nbr) == '#':
                    cnt += 1
            return cnt

        def get(pos):
            x, y = pos
            return arr[x][y]

        rnd = 0
        while True:
            print('round', rnd)

            num_chg = 0
            for i in range(N):
                for j in range(M):
                    pos = (i, j)
                    next_arr[i][j] = get(pos)
                    if get(pos) == 'L' and count_nbr_occup(pos) == 0:
                        next_arr[i][j] = '#'
                        num_chg += 1
                    elif get(pos) == '#' and count_nbr_occup(pos) >= 4:
                        next_arr[i][j] = 'L'
                        num_chg += 1

            arr = next_arr
            next_arr = [[None for _ in range(M)] for _ in range(N)]

            #for line in arr:
            #    print(''.join(line))

            if num_chg == 0:
                break
            #print('num_chg', num_chg)
            rnd += 1

        cnt = 0
        for i in range(N):
            for j in range(M):
                pos = (i, j)
                if get(pos) == '#':
                    cnt += 1
        return cnt
    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        arr = [list(line) for line in A]
        next_arr = [[None for _ in range(M)] for _ in range(N)]

        def get_nbrs(pos):
            x, y = pos
            out = []
            for d in DIRS:
                dx, dy = d
                x1, y1 = x+dx, y+dy
                while 0 <= x1 < N and 0 <= y1 < M and get((x1, y1)) == '.':
                    x1, y1 = x1+dx, y1+dy
                if 0 <= x1 < N and 0 <= y1 < M:
                    assert get(pos) != '.'
                    out.append((x1, y1))
            return out

        def count_nbr_occup(pos):
            nbrs = get_nbrs(pos)
            cnt = 0
            for nbr in nbrs:
                if get(nbr) == '#':
                    cnt += 1
            return cnt

        def get(pos):
            x, y = pos
            return arr[x][y]

        rnd = 0
        while True:
            print('round', rnd)

            num_chg = 0
            for i in range(N):
                for j in range(M):
                    pos = (i, j)
                    next_arr[i][j] = get(pos)
                    if get(pos) == 'L' and count_nbr_occup(pos) == 0:
                        next_arr[i][j] = '#'
                        num_chg += 1
                    elif get(pos) == '#' and count_nbr_occup(pos) >= 5:
                        next_arr[i][j] = 'L'
                        num_chg += 1

            arr = next_arr
            next_arr = [[None for _ in range(M)] for _ in range(N)]

            #for line in arr:
            #    print(''.join(line))

            if num_chg == 0:
                break
            #print('num_chg', num_chg)
            rnd += 1

        cnt = 0
        for i in range(N):
            for j in range(M):
                pos = (i, j)
                if get(pos) == '#':
                    cnt += 1
        return cnt

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    #line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #m = re.fullmatch(r"<(.*), (.*), (.*)>", line)
    #line = [parse_token(x) for x in line]

    # One token per line
    #line = line[0]

    return line


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
