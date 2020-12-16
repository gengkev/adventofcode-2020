#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 16
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


def check_range(value, rnge):
    s, e = rnge
    return s <= value <= e

def main(A):
    valid_tickets = []

    # Solve part 1
    def part1():
        field_list, _, nearby_tickets = A

        def check_all_ranges(value):
            for field_name, r1, r2 in field_list:
                if check_range(value, r1) or check_range(value, r2):
                    return True
            return False

        invalid_values = []
        for ticket in nearby_tickets:
            for idx, value in enumerate(ticket):
                if not check_all_ranges(value):
                    #print('invalid', value)
                    invalid_values.append(value)
        return sum(invalid_values)

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        field_list, your_ticket, nearby_tickets = A
        #print('field_list', field_list)

        def check_all_ranges(value):
            for field_name, r1, r2 in field_list:
                if check_range(value, r1) or check_range(value, r2):
                    return True
            return False

        valid_tickets = []
        for ticket in nearby_tickets:
            valid = True
            for idx, value in enumerate(ticket):
                if not check_all_ranges(value):
                    valid = False
            if valid:
                valid_tickets.append(ticket)

        #print('# valid tickets', len(valid_tickets), len(nearby_tickets))

        field_cand_idx_map = {}
        for field_name, r1, r2 in field_list:
            #print('considering', field_name, r1, r2)
            candidate_idx = set()

            for idx in range(len(field_list)):
                idx_valid = True
                for ticket in valid_tickets:
                    value = ticket[idx]
                    if not(check_range(value, r1) or check_range(value, r2)):
                        idx_valid = False
                        break
                if idx_valid:
                    candidate_idx.add(idx)

            field_cand_idx_map[field_name] = candidate_idx
            #print('field candidate idx', field_name, candidate_idx)

        # eliminate candidates
        #print('===============')
        field_idx_map = {}
        rounds = 0
        while field_cand_idx_map:
            for field_name, candidate_idx in field_cand_idx_map.items():
                assert len(candidate_idx) > 0
                if len(candidate_idx) == 1:
                    idx = list(candidate_idx)[0]
                    field_idx_map[field_name] = idx
                    del field_cand_idx_map[field_name]
                    #print('found assignment', field_name, idx)

                    for field_name, candidate_idx in field_cand_idx_map.items():
                        candidate_idx.remove(idx)
                    rounds += 1
                    break
            else:
                assert False

        #print('done, rounds', rounds)
        #print('map', field_idx_map)

        acc = 1
        for field_name, r1, r2 in field_list:
            idx = field_idx_map[field_name]
            #print('in your ticket', field_name, your_ticket[idx])
            if field_name.startswith('departure'):
                #print('multiply by', your_ticket[idx])
                acc *= your_ticket[idx]
        return acc

    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = iter(A)

    field_list = []
    while True:
        line = next(A)
        if not line:
            break
        m = re.fullmatch("(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
        field = m.group(1)
        r1s, r1e = int(m.group(2)), int(m.group(3))
        r2s, r2e = int(m.group(4)), int(m.group(5))
        field_list.append((field, (r1s,r1e), (r2s,r2e)))

    assert next(A) == 'your ticket:'
    your_ticket = list(map(int, next(A).split(',')))

    assert not next(A)
    assert next(A) == 'nearby tickets:'

    nearby_tickets = []
    while True:
        try:
            line = next(A)
            ticket = list(map(int, line.split(',')))
            nearby_tickets.append(ticket)
        except StopIteration:
            break

    return (field_list, your_ticket, nearby_tickets)


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
