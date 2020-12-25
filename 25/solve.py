#!/usr/bin/env python3

import copy
import operator
import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 25
YEAR = 2020


DIRS = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1),
}

DDIRS = {
    0: (1, 0),
    1: (1, 1),
    2: (0, 1),
    3: (-1, 1),
    4: (-1, 0),
    5: (-1, -1),
    6: (0, -1),
    7: (1, -1),
}

def vec_add(*args):
    return tuple(map(sum, zip(*args)))

def vec_mul(vec, k):
    return tuple(map(lambda x: x * k, vec))

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


def guess_loop_size(pubkey):
    val = 1
    subj = 7
    loop_size = 0

    while True:
        val *= subj
        val %= 20201227
        loop_size += 1

        if val == pubkey:
            return loop_size


def transform_key(subj, loop_size):
    val = 1

    for _ in range(loop_size):
        val *= subj
        val %= 20201227
        loop_size += 1

    return val


def main(A):
    # Solve part 1
    def part1():
        apubkey, bpubkey = A
        print('apubkey', apubkey)
        print('bpubkey', bpubkey)
        aloopsz = guess_loop_size(apubkey)
        bloopsz = guess_loop_size(bpubkey)
        print('aloopsz', aloopsz)
        print('bloopsz', bloopsz)
        res = transform_key(bpubkey, aloopsz)
        print('res', res)
        res = transform_key(apubkey, bloopsz)
        print('res', res)
        return res

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        pass

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
