#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 7
YEAR = 2020


##########################################################################


def main(A):
    A2 = []
    for this, others in A:
        others2 = []
        for other in others:
            if other == 'no other bags':
                continue
            m = re.match(r"(\d+) ([a-z]+ [a-z]+) bag", other)
            if m is None:
                print('bad', other)
            num, desc = m.group(1, 2)
            others2.append((int(num), desc))
        A2.append((this, others2))

    # Solve part 1
    def part1():
        graph = defaultdict(set)
        for this, others in A2:
            for num, desc in others:
                graph[this].add(desc)

        visited = {}
        visited['shiny gold'] = True
        def recur(desc):
            if desc in visited:
                return
            visited[desc] = False
            for other_desc in graph[desc]:
                recur(other_desc)
                if visited[other_desc]:
                    visited[desc] = True

        keys = [this for this, _ in A2]
        for this in keys:
            recur(this)

        #print(visited)
        count = 0
        for desc in visited:
            if visited[desc]:
                if desc == 'shiny gold':
                    continue
                #print('good:', desc)
                count += 1
        return count


    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        graph = dict(A2)

        visited = {}
        def recur(desc):
            if desc in visited:
                return
            if not graph[desc]:
                visited[desc] = 1
                return
            res = 1
            for other_num, other_desc in graph[desc]:
                recur(other_desc)
                res += other_num * visited[other_desc]
            visited[desc] = res

        keys = [this for this, _ in A2]
        for this in keys:
            recur(this)

        #print(visited)
        return visited['shiny gold'] - 1


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
    m = re.fullmatch(r"(.*) bags contain (.*).", line)
    uno = m.group(1)
    dos = m.group(2)
    return (uno, dos.split(', '))


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
