#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 5
YEAR = 2020


##########################################################################


def get_seat_pos(line):
    vert = line[:7]
    lo, hi = 0, 128
    for c in vert:
        if c == 'F':
            hi = lo + (hi - lo) // 2
        elif c == 'B':
            lo = lo + (hi - lo) // 2
        else:
            print(c)
            assert False
    assert lo + 1 == hi
    row = lo

    horz = line[-3:]
    lo, hi = 0, 8
    for c in horz:
        if c == 'L':
            hi = lo + (hi - lo) // 2
        elif c == 'R':
            lo = lo + (hi - lo) // 2
        else:
            print(c)
            assert False
    assert lo + 1 == hi
    col = lo

    return (row, col)


def get_seat_id(line):
    row, col = get_seat_pos(line)
    return row * 8 + col


def main(A):
    # Solve part 1
    def part1():
        all_ids = []
        for line in A:
            x = get_seat_id(line)
            #print(line, x)
            all_ids.append(x)
        return max(all_ids)


    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        all_rows = set()
        row_cols = defaultdict(set)

        for line in A:
            row, col = get_seat_pos(line)
            all_rows.add(row)
            row_cols[row].add(col)

        for row in sorted(all_rows):
            if len(row_cols[row]) != 8 and row-1 in all_rows and row+1 in all_rows:
                s = row_cols[row]
                diff = set(range(8)) - s
                assert len(diff) == 1

                col = list(diff)[0]
                print('returning', row, col)
                return row * 8 + col

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #m = re.fullmatch(r"<(.*), (.*), (.*)>", line)
    line = [parse_token(x) for x in line]

    # One token per line
    line = line[0]

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
