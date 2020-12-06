#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 6
YEAR = 2020


##########################################################################


def main(A):
    group_stuff = []
    cur = set()
    for line in A:
        if not line:
            group_stuff.append(cur)
            cur = set()

        cur |= set(line)
    group_stuff.append(cur)
    print(group_stuff)

    # Solve part 1
    def part1():
        out = 0
        for s in group_stuff:
            out += len(s)
        return out

    res = part1()
    submit_1(res)

    group_stuff = []
    cur = set('abcdefghijklmnopqrstuvwxyz')
    for line in A:
        if not line:
            group_stuff.append(cur)
            cur = set('abcdefghijklmnopqrstuvwxyz')

        else:
            cur &= set(line)
    group_stuff.append(cur)
    print(group_stuff)

    # Solve part 2
    def part2():
        out = 0
        for s in group_stuff:
            out += len(s)
        return out

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
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
