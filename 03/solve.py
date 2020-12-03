#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 3
YEAR = 2020


##########################################################################


def main(A):
    def get(i, j):
        j = j % len(A[0])
        return A[i][j]

    # Solve part 1
    def part1():
        height = len(A)
        cnt = 0
        i, j = 0, 0
        while i < height:
            if get(i, j) == '#':
                cnt += 1
            i += 1
            j += 3
        return cnt

    res = part1()
    submit_1(res)

    def go(di, dj):
        height = len(A)
        cnt = 0
        i, j = 0, 0
        while i < height:
            if get(i, j) == '#':
                cnt += 1
            i += di
            j += dj
        return cnt

    # Solve part 2
    def part2():
        out = [
            go(1, 1),
            go(1, 3),
            go(1, 5),
            go(1, 7),
            go(2, 1)
        ]
        acc = 1
        for x in out:
            acc *= x
        return acc

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    return line


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]

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
