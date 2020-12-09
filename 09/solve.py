#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 9
YEAR = 2020


##########################################################################


def main(A):
    LEN = 5 if is_sample else 25

    # Solve part 1
    def part1():
        rolling = deque()

        def check(x):
            for a in rolling:
                for b in rolling:
                    if x == a + b:
                        return True
            return False

        for x in A:
            # check
            if len(rolling) >= LEN and not check(x):
                return x

            # update
            rolling.append(x)
            if len(rolling) > LEN:
                rolling.popleft()

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        Alen = len(A)
        for i in range(0, Alen - 2):
            running = A[i] + A[i+1]
            for j in range(i + 2, Alen):
                if running == res:
                    #print('hello', i, j)
                    sub = A[i:j]
                    return min(sub) + max(sub)
                running += A[j]

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    return int(line)
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
