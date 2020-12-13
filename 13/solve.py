#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 13
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

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def main(A):
    # Solve part 1
    def part1():
        earliest_ts, bus_ids = A
        bus_ids = [int(x) for x in bus_ids if x != 'x']

        next_occur = [((earliest_ts + x - 1) // x) * x for x in bus_ids]
        ts = min(next_occur)
        idx = next_occur.index(ts)
        bus_id = bus_ids[idx]
        # print('found', ts, bus_id)
        return (ts - earliest_ts) * bus_id

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        _, bus_ids = A
        # t + i == 0 mod N
        eqns = [((-i) % int(N), int(N)) for i, N in enumerate(bus_ids) if N != 'x']

        def red(a1, n1, a2, n2):
            #a1, n1 = eqns[0]
            #a2, n2 = eqns[1]
            g, m1, m2 = xgcd(n1, n2)
            x = a1 * m2 * n2 + a2 * m1 * n1
            #print('a1, n1 =', a1, n1)
            #print('a2, n2 =', a2, n2)
            #print('g, m1, m2 =', g, m1, m2)
            #print('x =', x)
            #print('x % n1 =', x % n1)

            #print('hello', x)
            assert x % n1 == a1 % n1
            assert x % n2 == a2 % n2

            lcm = n1 * n2 // g
            return x % lcm, lcm

        a1, n1 = eqns[0]
        for a2, n2 in eqns[1:]:
            a1, n1 = red(a1, n1, a2, n2)
            #print('=====>', a1, n1)

        for a, n in eqns:
            #print(f'{a1} % {n} == {a}')
            assert a1 % n == a

        return a1

    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    earliest_ts = int(A[0])
    bus_ids = A[1].split(',')
    return (earliest_ts, bus_ids)


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
