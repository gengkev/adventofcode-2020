#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 23
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


def main(A):
    orig_A = A[:]
    N = len(A)
    min_label = min(A)
    max_label = max(A)

    # Solve part 1
    def part1():
        A = orig_A[:]
        for move in range(1, 101):
            cur_cup = A[0]
            pick_cups = A[1:4]
            available_cups = A[4:]

            # find dest
            dest = cur_cup
            while dest not in available_cups:
                dest -= 1
                if dest < min_label:
                    dest = max_label

            # update A
            dest_idx = available_cups.index(dest)
            A = available_cups[:dest_idx+1] + pick_cups + available_cups[dest_idx+1:] + [cur_cup]

        # get output
        B = A[:]
        while B[0] != 1:
            B = B[1:] + B[:1]
        B = B[1:]
        return ''.join(map(str, B))

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        A = deque(orig_A[:] + list(range(max_label+1, 1000000+1)))
        comes_after = defaultdict(list)

        def get_next():
            next_elt = A.popleft()
            if next_elt in comes_after:
                A.extendleft(comes_after[next_elt][::-1])
                del comes_after[next_elt]
            return next_elt

        # simulate 10mil steps
        for move in range(1, 10000000+1):
            cur_cup = get_next()
            pick_cups = [get_next(), get_next(), get_next()]
            unavailable_cups = set([cur_cup] + pick_cups)

            # find dest
            dest = cur_cup
            while dest in unavailable_cups:
                dest -= 1
                if dest < 1:
                    dest = 1000000

            # update A
            comes_after[dest] += pick_cups
            A.append(cur_cup)

        # done with simulation, find where 1 is
        while (next_elt := get_next()) != 1:
            A.append(next_elt)

        uno, dos = get_next(), get_next()
        return uno * dos

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    x = int(x)
    return x


def parse_line(line):
    #line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #m = re.fullmatch(r"<(.*), (.*), (.*)>", line)
    line = [parse_token(x) for x in line]

    # One token per line
    #line = line[0]

    return line


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]

    # One line per input
    A = A[0]

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
