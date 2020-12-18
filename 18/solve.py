#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 18
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


def eval_op(a, op, b):
    if op == '+':
        return (a)+(b)
    elif op == '*':
        return (a)*(b)
    else:
        assert False

# Evaluates an expr from left to right
def eval_expr(line):
    line = re.sub(r' ', '', line)
    #print('line', line)

    save_stack = []
    stack = []

    def collapse_stack():
        while len(stack) > 1:
            assert len(stack) > 2
            b, op, a = stack.pop(), stack.pop(), stack.pop()
            res = eval_op(a, op, b)
            stack.append(res)

    for c in line:
        if c.isnumeric():
            stack.append(int(c))
            collapse_stack()

        elif c in '*+':
            stack.append(c)

        elif c == '(':
            save_stack.append(stack)
            stack = []

        elif c == ')':
            if len(stack) != 1:
                print(save_stack)
                print(stack)
            assert len(stack) == 1
            val = stack[0]
            stack = save_stack.pop()
            stack.append(val)
            collapse_stack()

        else:
            assert False

    if len(stack) != 1:
        print(save_stack)
        print(stack)
    assert len(stack) == 1
    return stack[0]

# Disambiguates an expression with "addition precedence" by adding parentheses
# Returns result, index of first character not processed
def transform_expr(line):
    line = re.sub(r' ', '', line)
    out = []
    op_stack = []
    level = 0

    def reduce_out():
        while len(out) >= 2 and op_stack and op_stack[-1] == '+':
            op_stack.pop()
            b, a = out.pop(), out.pop()
            out.append('({}+{})'.format(a, b))

    i = 0
    while i < len(line):
        c = line[i]
        #print('i =', i, 'next c', c)
        #print('out =', out)
        #print('op_stack =', op_stack)

        if c.isnumeric():
            out.append(c)
            i += 1
            reduce_out()

        elif c in '*+':
            op_stack.append(c)
            i += 1

        elif c == '(':
            res, nrem = transform_expr(line[i+1:])
            out.append('(' + res + ')')
            i = (i+1) + nrem + 1
            reduce_out()

        elif c == ')':
            break

        else:
            print(c)
            assert False

    #print('returning', op_stack, out, i)
    assert all(x == '*' for x in op_stack)
    return ('*'.join(out), i)

def main(A):
    # Solve part 1
    def part1():
        res = 0
        for line in A:
            val = eval_expr(line)
            res += val
        return res

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        res = 0
        for line in A:
            new_line, _ = transform_expr(line)
            val = eval_expr(new_line)
            #print('line:', line)
            #print('line2:', new_line)
            #print('res', val)
            #print()
            res += val
        return res

    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()

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
