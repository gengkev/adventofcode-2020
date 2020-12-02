#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 2
YEAR = 2020


##########################################################################


def main(A):
    def solve(line):
        start, end, c, pwd = line
        cnt = pwd.count(c)
        return start <= cnt <= end

    # Solve part 1
    def part1():
        return sum(bool(solve(line)) for line in A)

    res = part1()
    submit_1(res)

    def solve(line):
        start, end, c, pwd = line
        good = [bool(start-1 < len(pwd) and pwd[start-1] == c), bool(end-1 < len(pwd) and pwd[end-1] == c)]
        return sum(good) == 1

    # Solve part 2
    def part2():
        return sum(bool(solve(line)) for line in A)

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    line = line.split()
    start, end = line[0].split('-')
    start = int(start)
    end = int(end)
    c = line[1][0]
    pwd = line[2]
    return (start, end, c, pwd)


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
