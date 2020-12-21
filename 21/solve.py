#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 21
YEAR = 2020


##########################################################################


def main(A):
    all_ingred = set()
    all_allerg = set()
    for ingred_list, allerg_list in A:
        all_ingred |= set(ingred_list)
        all_allerg |= set(allerg_list)

    allerg_possible_map = {}
    for allerg in all_allerg:
        allerg_possible_map[allerg] = set(all_ingred)

    for ingred_list, allerg_list in A:
        for allerg in allerg_list:
            allerg_possible_map[allerg] &= set(ingred_list)
    #print(allerg_possible_map)

    # Solve part 1
    def part1():
        ingred_non_allerg = set(all_ingred)
        for _, ingred_set in allerg_possible_map.items():
            ingred_non_allerg -= ingred_set
        #print(ingred_non_allerg)

        cnt = 0
        for ingred_list, allerg_list in A:
            for ingred in ingred_list:
                if ingred in ingred_non_allerg:
                    cnt += 1
        return cnt

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        allerg_result = {}
        def red_allerg_possible():
            for allerg, ingred_set in allerg_possible_map.items():
                if len(ingred_set) == 1:
                    ingred = list(ingred_set)[0]
                    break
            else:
                assert False

            allerg_result[allerg] = ingred
            del allerg_possible_map[allerg]
            for allerg, ingred_set in allerg_possible_map.items():
                ingred_set -= set([ingred])
            return

        while allerg_possible_map:
            red_allerg_possible()
        #print(allerg_result)

        allerg_result_l = list(allerg_result.items())
        allerg_result_l.sort()
        allerg_result_l = [ingred for (_, ingred) in allerg_result_l]
        return ','.join(allerg_result_l)

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    m = re.fullmatch(r"(.+) \(contains (.+)\)", line)
    a, b = m.group(1, 2)
    a = a.split(' ')
    b = b.split(', ')
    return (a, b)


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
