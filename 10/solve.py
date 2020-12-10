#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 10
YEAR = 2020


##########################################################################


def main(A):
    target = max(A) + 3
    A = sorted(A)

    # Solve part 1
    def part1():
        cnts = [0, 0, 0, 0]
        cur = 0
        for x in A:
            d = x - cur
            if d > 3:
                print('what', d)
            cnts[d] += 1
            cur = x
        d = target - cur
        cnts[d] += 1

        return cnts[1] * cnts[3]

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        sack = [0 for _ in range(target+1)]
        sack[0] = 1

        for adp in A:
            for i in range(max(adp-3, 0), adp):
                sack[adp] += sack[i]

        for i in range(target-3, target):
            sack[target] += sack[i]

        return sack[target]

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    return int(line)


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
