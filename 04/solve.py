#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 4
YEAR = 2020


##########################################################################

def validate_field(k, v):
    v = v.strip()
    if k == 'byr':
        return len(v) == 4 and 1920 <= int(v) <= 2002
    if k == 'iyr':
        return len(v) == 4 and 2010 <= int(v) <= 2020
    if k == 'eyr':
        return len(v) == 4 and 2020 <= int(v) <= 2030
    if k == 'hgt':
        m = re.match(r'(\d+)(cm|in)', v)
        if m is None:
            return False
        num, unit = m.group(1, 2)
        if unit == 'cm':
            return 150 <= int(num) <= 193
        if unit == 'in':
            return 59 <= int(num) <= 76
        assert False
    if k == 'hcl':
        if v[0] != '#':
            return False
        m = re.match(r'#([0-9a-fA-F]{6})', v)
        return m is not None
    if k == 'ecl':
        return v in ['amb','blu','brn','gry','grn','hzl','oth']
    if k == 'pid':
        m = re.match(r'[0-9]{9}$', v)
        return m is not None
    if k == 'cid':
        return True
    assert False


def validate_passport(p):
    p = dict(p)
    if 'cid' in p:
        del p['cid']

    if len(p) != 7:
        #print('invalid because len is wrong', len(p))
        return False

    if p.keys() != set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']):
        print('bad keys', p.keys())
        return False

    for k, v in p.items():
        if not validate_field(k, v):
            #print('invalid because', k, v)
            return False

    return True


def main(A):
    passports = []
    cur_passport = {}

    for line in A:
        if not line:
            # new passport
            passports.append(cur_passport)
            cur_passport = {}

        for token in line:
            k, v = token.split(':')
            cur_passport[k] = v

    passports.append(cur_passport)
    print(len(passports))

    # Solve part 1
    def part1():
        cnt = 0
        for p in passports:
            if len(p) == 8 or (len(p) == 7 and 'cid' not in p):
                cnt += 1
        return cnt

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        cnt = 0
        for p in passports:
            if validate_passport(p):
                cnt += 1
                #print('valid', [v for k, v in sorted(p.items()) if k != 'cid'])
                print(' '.join(f'{k}:{v}' for k, v in sorted(p.items())))
                print()

        return cnt

    res = part2()
    submit_2(res)


##########################################################################

def parse_line(line):
    line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #x, y, z = re.match(r"<(.*), (.*), (.*)>", line).group(1, 2, 3)

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
