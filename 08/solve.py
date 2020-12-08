#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 8
YEAR = 2020


##########################################################################


def main(A):
    # Solve part 1
    def part1():
        visited = set()
        acc = 0
        i = 0
        while True:
            if i in visited:
                return acc
            visited.add(i)
            cmd, offset = A[i]
            if cmd == 'acc':
                acc += offset
                i += 1
            elif cmd == 'jmp':
                i += offset
            elif cmd == 'nop':
                i += 1
            else:
                assert False

    res = part1()
    submit_1(res)

    def get_succ(i):
        cmd, offset = A[i]
        if cmd == 'acc':
            return i + 1
        elif cmd == 'jmp':
            return i + offset
        elif cmd == 'nop':
            return i + 1
        else:
            assert False

    def get_succ_alt(i):
        cmd, offset = A[i]
        if cmd == 'acc':
            return i + 1
        elif cmd == 'jmp':
            return i + 1
        elif cmd == 'nop':
            return i + offset
        else:
            assert False

    # Solve part 2
    def part2():
        start = 0
        end = len(A)

        fwd_graph = defaultdict(set)
        bck_graph = defaultdict(set)
        for i, (cmd, offset) in enumerate(A):
            succ = get_succ(i)
            fwd_graph[i].add(succ)
            bck_graph[succ].add(i)

        #print('fwd_graph', fwd_graph)
        #print('bck_graph', bck_graph)

        def dfs(graph, visited, i):
            #print('visiting', i)
            if i in visited:
                return
            visited.add(i)
            for nxt in graph[i]:
                dfs(graph, visited, nxt)

        # Determine forward reachability
        fwd_visited = set()
        dfs(fwd_graph, fwd_visited, start)
        #print(fwd_visited)

        bck_visited = set()
        dfs(bck_graph, bck_visited, end)
        #print(bck_visited)

        for i in range(len(A)):
            if i in fwd_visited and get_succ_alt(i) in bck_visited:
                #print('HELLO WORLD', i, A[i])
                cmd, offset = A[i]
                if cmd == 'jmp':
                    A[i] = ('nop', offset)
                else:
                    A[i] = ('jmp', offset)
                break
        else:
            assert False

        acc = 0
        i = 0
        while i < len(A):
            cmd, offset = A[i]
            if cmd == 'acc':
                acc += offset
                i += 1
            elif cmd == 'jmp':
                i += offset
            elif cmd == 'nop':
                i += 1
            else:
                assert False

        return acc

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    cmd, offset = line.split()
    offset = int(offset)
    return (cmd, offset)


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
