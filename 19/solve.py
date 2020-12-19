#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 19
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
    rules, msgs = A

    # matches a list of rule indexes
    # if matched completely, returns number of characters matched (nonzero)
    # otherwise, None if couldn't match
    def check_subrules(sub_rules, msg):
        idx = 0
        for sub_rule_idx in sub_rules:
            sub_rule = rules[sub_rule_idx]
            n = check_rule(sub_rule, msg[idx:])
            if n is None:
                return None
            idx += n
        return idx

    # matches a rule definition
    # if matched completely, returns number of characters matched (nonzero)
    # otherwise, None if couldn't match
    def check_rule(rule, msg):
        #print('check_rule', rule, msg)
        rule_type, rule_content = rule

        if rule_type == 'subrules':
            for sub_rules in rule_content:
                n = check_subrules(sub_rules, msg)
                if n is not None:
                    return n
            return None

        elif rule_type == 'char':
            if not msg:
                assert False
                return None
            if msg[0] == rule_content:
                return 1
            return None

        else:
            print(rule)
            assert False

    # Solve part 1
    def part1():
        cnt = 0
        for msg in msgs:
            if check_rule(rules[0], msg) == len(msg):
                #print('this one matches:', msg)
                cnt += 1
            else:
                #print('does not match:', msg)
                pass
        return cnt

    res = part1()
    submit_1(res)

    # returns true if the msg matches the entire rule list
    def check_rule_part2(rule_list, msg):
        #print('check_rule_part2', rule_list, msg)
        if len(rule_list) == 0:
            if msg:
                return False
            return True

        #print('check_rule', rule, msg)
        rule = rules[rule_list[0]]
        rule_type, rule_content = rule

        if rule_type == 'subrules':
            for sub_rules in rule_content:
                new_rules = sub_rules + rule_list[1:]
                # note: len check is important to ensure bounded recursion
                # we know that each rule must match >=1 character
                if len(new_rules) <= len(msg) and check_rule_part2(sub_rules + rule_list[1:], msg):
                    return True
            return False

        elif rule_type == 'char':
            if not msg:
                assert False
                return None
            if msg[0] == rule_content:
                return check_rule_part2(rule_list[1:], msg[1:])
            return False

        else:
            print(rule)
            assert False

    # Solve part 2
    def part2():
        rules[8] = ('subrules', [[42], [8, 42]])
        rules[11] = ('subrules', [[42, 31], [42, 11, 31]])

        cnt = 0
        for msg in msgs:
            if check_rule_part2([0], msg):
                #print('this one matches:', msg)
                cnt += 1
            else:
                #print('does not match:', msg)
                pass
        return cnt

    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = iter(A)

    # read rules
    rules = {}
    while True:
        line = next(A)
        if not line:
            break

        line = line.split()
        try:
            rule_num = int(line[0][:-1])
        except ValueError:
            print('what is wrong', line[0])
            exit(1)

        if len(line) == 2 and line[1][0] == line[1][-1] == '"':
            rules[rule_num] = ('char', line[1][1:-1])

        else:
            all_subs = []
            cur = []
            for token in line[1:] + ['|']:
                if token == '|':
                    all_subs.append(cur)
                    cur = []
                elif token.isnumeric():
                    cur.append(int(token))
                elif token[0] == token[-1] == '"':
                    cur.append(token[1:-1])
                else:
                    assert False
            assert not cur

            rules[rule_num] = ('subrules', all_subs)

    msgs = []
    try:
        while True:
            line = next(A)
            msgs.append(line)
    except StopIteration:
        pass

    return (rules, msgs)


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
