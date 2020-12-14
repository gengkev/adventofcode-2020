#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 14
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
    # Solve part 1
    def part1():
        mem = defaultdict(int)
        set_mask = 0
        value_mask = 0
        for line in A:
            if line[0] == 'mask':
                _, set_mask, value_mask = line
            elif line[0] == 'mem':
                _, addr, value = line
                mem[addr] = (value & (set_mask)) | value_mask
                #print('in', addr, value)
                #print('set_mask', ((1 << 36)-1) & ~set_mask)
                #print('value_mask', value_mask)
                #print('mem', addr, mem[addr])
                #print('===')
            else:
                print(line)
                assert False

        out = 0
        for addr in mem:
            #print('addr', addr, 'value', mem[addr])
            out += mem[addr]
        return out

    res = part1()
    submit_1(res)

    def get_set_pos(n):
        out = []
        for i in range(36):
            if (n & (1 << i)) != 0:
                out.append(i)
        return out

    # Solve part 2
    def part2():
        mem = defaultdict(int)
        set_mask = 0
        value_mask = 0
        for line in A:
            if line[0] == 'mask':
                _, set_mask, value_mask = line
            elif line[0] == 'mem':
                _, addr, value = line
                addr = addr | value_mask  # set 1 bits to 1
                addr = addr & ~set_mask   # set floating bits to 0
                orig_addr = addr

                floating_pos = get_set_pos(set_mask)
                #print('floating_pos', floating_pos)
                for repl in itertools.product(range(2), repeat=len(floating_pos)):
                    cur_addr = addr
                    for i, val in enumerate(repl):
                        if val == 1:
                            cur_addr |= (1 << (floating_pos[i]))
                    assert (cur_addr & (~set_mask)) == orig_addr
                    mem[cur_addr] = value

        out = 0
        for addr in mem:
            #print('addr', addr, 'value', mem[addr])
            out += mem[addr]
        return out

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    line = line.split()

    if line[0] == 'mask':
        in_mask = line[2]
        set_mask = 0
        for i in range(36):
            if in_mask[35-i] == 'X':
                set_mask |= (1 << i)
        value_mask = 0
        for i in range(36):
            if in_mask[35-i] == '1':
                value_mask |= (1 << i)
        line = ('mask', set_mask, value_mask)
    elif 'mem' in line[0]:
        m = re.fullmatch(r"mem\[(\d+)\]", line[0])
        addr = int(m.group(1))
        value = int(line[2])
        line = ('mem', addr, value)

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
