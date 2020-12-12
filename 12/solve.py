#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 12
YEAR = 2020


##########################################################################

DIRS = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1),
}

def add_pos(a, b):
    return (a[0]+b[0], a[1]+b[1])

def mul_pos(a, mul):
    return (a[0]*mul, a[1]*mul)

def main(A):
    # Solve part 1
    def part1():
        my_d = 0  # east
        my_pos = (0, 0)

        for d, n in A:
            if d == 'E':
                my_pos = add_pos(my_pos, mul_pos(DIRS[0], n))
            if d == 'N':
                my_pos = add_pos(my_pos, mul_pos(DIRS[1], n))
            if d == 'W':
                my_pos = add_pos(my_pos, mul_pos(DIRS[2], n))
            if d == 'S':
                my_pos = add_pos(my_pos, mul_pos(DIRS[3], n))
            if d == 'F':
                my_pos = add_pos(my_pos, mul_pos(DIRS[my_d], n))
            if d == 'L':
                assert n % 90 == 0
                my_d = (my_d + (n // 90)) % 4
            if d == 'R':
                assert n % 90 == 0
                my_d = (my_d - (n // 90)) % 4

        return abs(my_pos[0]) + abs(my_pos[1])

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        my_d = 0  # east
        wp_pos = (10, 1)
        my_pos = (0, 0)

        def rotate_wp(wp_pos, d):
            x, y = wp_pos
            if d == 0:
                return (x, y)
            elif d == 1:
                return (-y, x)
            elif d == 2:
                return (-x, -y)
            elif d == 3:
                return (y, -x)

        for d, n in A:
            if d == 'E':
                wp_pos = add_pos(wp_pos, mul_pos(DIRS[0], n))
            if d == 'N':
                wp_pos = add_pos(wp_pos, mul_pos(DIRS[1], n))
            if d == 'W':
                wp_pos = add_pos(wp_pos, mul_pos(DIRS[2], n))
            if d == 'S':
                wp_pos = add_pos(wp_pos, mul_pos(DIRS[3], n))
            if d == 'F':
                my_pos = add_pos(my_pos, mul_pos(wp_pos, n))
            if d == 'L':
                assert n % 90 == 0
                wp_pos = rotate_wp(wp_pos, (n // 90) % 4)
            if d == 'R':
                assert n % 90 == 0
                wp_pos = rotate_wp(wp_pos, (-(n // 90)) % 4)

            #print('my_d', my_d)
            #print('wp_pos', wp_pos)
            #print('my_pos', my_pos)

        return abs(my_pos[0]) + abs(my_pos[1])

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

    d, n = line[0], line[1:]
    n = int(n)
    return (d, n)

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
