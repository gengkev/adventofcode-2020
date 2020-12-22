#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 22
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

def compute_score(win_cards):
    score = 0
    for i, card in enumerate(win_cards[::-1]):
        score += (i+1) * card
    return score

def main(A):

    # Solve part 1
    def part1():
        nonlocal A
        p1_cards, p2_cards = A
        p1_cards = p1_cards[:]
        p2_cards = p2_cards[:]

        while p1_cards and p2_cards:
            p1c = p1_cards.pop(0)
            p2c = p2_cards.pop(0)

            if p1c > p2c:
                p1_cards += [p1c, p2c]
            elif p2c > p1c:
                p2_cards += [p2c, p1c]

        win_cards = p1_cards if p1_cards else p2_cards
        score = compute_score(win_cards)
        return score

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        big_memo = {}
        game_counter = 0

        def play_game(p1_cards, p2_cards):
            nonlocal game_counter
            cur_game = game_counter
            game_counter += 1
            print('Game #{}'.format(cur_game))

            big_memo_item = (tuple(p1_cards), tuple(p2_cards))
            if big_memo_item in big_memo:
                #print('using memo!')
                return big_memo[big_memo_item]

            #print('playing game', p1_cards, p2_cards)
            p1_cards = p1_cards[:]
            p2_cards = p2_cards[:]
            memo_cards = set()

            while p1_cards and p2_cards:
                winner = None

                # would repeat infinitely, p1 wins
                memo_item = (tuple(p1_cards), tuple(p2_cards))
                if memo_item in memo_cards:
                    #print(' ==> repeating, oh no')
                    winner = 'p1'
                else:
                    memo_cards.add(memo_item)

                # draw top of both decks
                p1c = p1_cards.pop(0)
                p2c = p2_cards.pop(0)

                if winner is None:
                    # not enough cards to recurse
                    if p1c > len(p1_cards) or p2c > len(p2_cards):
                        #print(' ==> not enough cards to recurse')
                        if p1c > p2c:
                            winner = 'p1'
                        elif p2c > p1c:
                            winner = 'p2'
                        else:
                            1/0

                if winner is None:
                    # ok, play a new game
                    #print(' ==> recurse')
                    p1_new_cards = p1_cards[:p1c]
                    p2_new_cards = p2_cards[:p2c]
                    winner, _ = play_game(p1_new_cards, p2_new_cards)

                # based on who won
                if winner == 'p1':
                    p1_cards += [p1c, p2c]
                elif winner == 'p2':
                    p2_cards += [p2c, p1c]
                else:
                    1/0

            if p1_cards:
                #print('p1 wins', p1_cards)
                res = ('p1', p1_cards)
            elif p2_cards:
                #print('p2 wins', p2_cards)
                res = ('p2', p2_cards)
            else:
                1/0

            big_memo[big_memo_item] = res
            print('-> done with game', cur_game)
            return res

        p1_cards, p2_cards = A
        p1_cards = p1_cards[:]
        p2_cards = p2_cards[:]
        _, win_cards = play_game(*A)
        score = compute_score(win_cards)
        return score

    res = part2()
    submit_2(res)


##########################################################################


def parse_input(A):
    A = A.strip()
    A = A.splitlines()

    p1_cards = []
    p2_cards = []

    p = 0
    for line in A:
        line = line.strip()
        if line == 'Player 1:':
            p = 1
        elif line == 'Player 2:':
            p = 2
        elif line:
            if p == 1:
                p1_cards.append(int(line))
            elif p == 2:
                p2_cards.append(int(line))
            else:
                1/0

    return (p1_cards, p2_cards)


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
