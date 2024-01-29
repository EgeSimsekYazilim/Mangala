"""
Turkish Mancala Bot (v2)
Made by Ege Şimşek, visit (www.smsk.one)
"""
from os import system, name
from random import choice
from time import sleep
import math

seq = [[[[1], [1], [3], [1], [2, 4, 5]], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]],
       [[[3], [4]], [3], [1]]]
opening = True


def possible(p):
    return [i for i in range(1, 7) if p[i] != 0]


def status(p1, p2):
    print("\x1b[3;31;40m-----------------\x1b[0m")
    print("\x1b[1;33;40m  " + ' '.join(str(x) for x in p2[1:][::-1]))
    print(str(p2[0]) + "\x1b[0m" + ' ' * 13 + "\x1b[1;32;40m" + str(p1[0]))
    print("  " + ' '.join(str(x) for x in p1[1:][::-1]) + "\x1b[0m")


def cls():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def check_gg(p1, p2):
    temp_p1 = p1.copy()
    temp_p2 = p2.copy()
    gg = False

    if sum(temp_p1[1:]) == 0:
        gg = True
        temp_p1[0] += sum(temp_p2[1:])
        temp_p2 = [temp_p2[0], 0, 0, 0, 0, 0, 0]
    elif sum(temp_p2[1:]) == 0:
        gg = True
        temp_p2[0] += sum(temp_p1[1:])
        temp_p1 = [temp_p1[0], 0, 0, 0, 0, 0, 0]

    return temp_p1, temp_p2, gg


def make_move(move, p1, p2):
    temp_p1 = p1.copy()
    temp_p2 = p2.copy()

    val = temp_p1[move]
    v = max(1, val - 1)
    again = False

    for j in range(v):
        cur = 8 - move + j
        last = v == j + 1
        if cur in [7, 20, 33]:
            temp_p1[0] += 1
            if last or val == 1:
                again = True
        elif 27 > cur > 20:
            temp_p2[cur - 20] += 1
            if temp_p2[cur - 20] % 2 == 0 and last:
                temp_p1[0] += temp_p2[cur - 20]
                temp_p2[cur - 20] = 0
        elif 14 > cur > 7:
            temp_p2[cur - 7] += 1
            if temp_p2[cur - 7] % 2 == 0 and last:
                temp_p1[0] += temp_p2[cur - 7]
                temp_p2[cur - 7] = 0
        elif 33 > cur > 26:
            temp_p1[33 - cur] += 1
            if temp_p1[33 - cur] == 1 and temp_p2[33 - cur] != 0 and last:
                temp_p1[0] += temp_p1[33 - cur] + temp_p2[33 - cur]
                temp_p1[33 - cur] = 0
                temp_p2[33 - cur] = 0
        elif 20 > cur > 13:
            temp_p1[20 - cur] += 1
            if temp_p1[20 - cur] == 1 and temp_p2[20 - cur] != 0 and last:
                temp_p1[0] += temp_p1[20 - cur] + temp_p2[20 - cur]
                temp_p1[20 - cur] = 0
                temp_p2[20 - cur] = 0
        elif 7 > cur:
            temp_p1[7 - cur] += 1
            if temp_p1[7 - cur] == 1 and temp_p2[7 - cur] != 0 and last:
                temp_p1[0] += temp_p1[7 - cur] + temp_p2[7 - cur]
                temp_p1[7 - cur] = 0
                temp_p2[7 - cur] = 0

    if val == 1:
        temp_p1[move] = 0
    else:
        temp_p1[move] = 1

    temp_p1, temp_p2, gg = check_gg(temp_p1, temp_p2)
    return temp_p1, temp_p2, again, gg


def evaluate(b, o):
    board = sum(b[1:]) + sum(o[1:])

    piece = (b[0] - o[0]) * 0.495
    active = (sum(o[1:]) - sum(b[1:])) * (0.245 if board <= 15 else 0)
    balance = (sum(b[1:4]) - sum(b[4:7]) - (sum(o[1:4]) - sum(o[4:7]))) * (0.095 if 15 < board < 30 else 0)
    return piece + active + balance


def get_best_from(plr1, plr2, pos, depth, alpha, beta):
    if len(pos) < 1: pos = possible(plr1)
    best_move = pos[0]
    best_eval = -math.inf
    best_win = 0
    for move in pos:
        new_plr1, new_plr2, _, gg = make_move(move, plr1, plr2)
        if gg:
            ev = math.inf
        else:
            ev = minimax_alpha_beta(new_plr1, new_plr2, depth, True, evaluate, alpha, beta)

            factor = 0.995
            b = sum(plr1[1:] + plr2[1:])
            if b <= 10: factor = math.inf
            elif b <= 20: factor = 1.395
            elif b <= 30: factor = 1.145

            if sum(plr1[1:]) <= 15: factor += 1.005

            xv = plr1[move]
            if move == 1 and xv in [1, 2, 15, 29]: ev += 1.25 * factor
            elif move == 2 and xv in [3, 16, 30]: ev += 1.1 * factor
            elif move == 3 and xv in [4, 17, 31]: ev += 0.95 * factor
            elif move == 4 and xv in [5, 18, 32]: ev += 0.85 * factor
            elif move == 5 and xv in [6, 19, 33]: ev += 0.75 * factor
            elif move == 6 and xv in [7, 20, 34]: ev += 0.65 * factor
            elif math.isinf(factor): return pos[0]

        if ev > best_eval:
            best_eval = ev
            best_move = move
            best_win = new_plr1[0] - plr1[0]
        elif ev + (new_plr1[0] - plr1[0]) / 2 >= best_eval + best_win / 2:
            best_eval = ev
            best_move = move
            best_win = new_plr1[0] - plr1[0]
    return best_move


def find_best_move(op, plr1, plr2, depth, alpha=-math.inf, beta=math.inf):
    pos = possible(plr1)
    global opening
    if sum(plr1[1:] + plr2[1:]) <= 20: opening = False
    if opening:
        plan = None
        if op is None and len(seq[0][0]) != 0:
            plan = seq[0][0].pop(0)
            seq[0].pop(1)
        else:
            for s in seq:
                if len(s[0]) == 0:
                    opening = False
                    break
                if opening:
                    req = []
                    if len(s) != 1: req = s.pop(1)
                    if op in req or req == []:
                        plan = s[0].pop(0)
                        break
        if plan is not None:
            sleep(1.5)
            return get_best_from(plr1, plr2, [i for i in plan if i in pos], 3, alpha, beta)

    return get_best_from(plr1, plr2, pos, depth - 1, alpha, beta)


def minimax_alpha_beta(plr1, plr2, depth, maximizing_player, evaluate_function, alpha, beta):
    if depth == 0 or check_gg(plr1, plr2)[2]:
        return evaluate_function(plr1, plr2)

    if maximizing_player:
        max_eval = -math.inf
        for move in possible(plr1):
            new_plr1, new_plr2, _, _ = make_move(move, plr1, plr2)
            ev = minimax_alpha_beta(new_plr1, new_plr2, depth - 1, False, evaluate_function, alpha, beta)
            max_eval = max(max_eval, ev)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in possible(plr2):
            new_plr2, new_plr1, _, _ = make_move(move, plr2, plr1)
            ev = minimax_alpha_beta(new_plr1, new_plr2, depth - 1, True, evaluate_function, alpha, beta)
            min_eval = min(min_eval, ev)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval


def bot(p1, p2, op):
    status(p1, p2)
    if p1[0] + p2[0] >= 30: sleep(1.5)
    p1 = [p1[0]] + p1[1:][::-1]
    p2 = [p2[0]] + p2[1:][::-1]
    p2, p1, again, gg = make_move(find_best_move(op, p2, p1, 12), p2, p1)
    p1 = [p1[0]] + p1[1:][::-1]
    p2 = [p2[0]] + p2[1:][::-1]
    return p1, p2, again, gg


def player(p1, p2):
    status(p1, p2)
    move = int(input("\x1b[3;30;47mMove (1 to 6): "))
    while move not in possible(p1):
        move = int(input("\x1b[3;30;47mMove (1 to 6): "))
    print("\x1b[0m")

    return make_move(move, p1, p2) + tuple([move])


def main():
    while True:
        p1 = [0, 4, 4, 4, 4, 4, 4]
        p2 = [0, 4, 4, 4, 4, 4, 4]
        start = choice([True, False])
        game = True
        pm = None
        while game:
            p1, p2, gg = check_gg(p1, p2)
            if gg:
                status(p1, p2)
                print("Game Over!")
                sleep(0.5)
                input("Press 'Enter' for a new match.")
                sleep(0.5)
                game = False

            if game:
                if start:
                    p1, p2, again, gg, pm = player(p1, p2)
                    while again and not gg:
                        print("\x1b[0;30;44mYour Turn Again!\x1b[0m")
                        p1, p2, again, gg, pm = player(p1, p2)

                    cls()

                    if not gg:
                        p1, p2, again, gg = bot(p1, p2, pm)
                        while again and not gg: p1, p2, again, gg = bot(p1, p2, pm)
                else:
                    cls()
                    p1, p2, again, gg = bot(p1, p2, pm)
                    while again and not gg: p1, p2, again, gg = bot(p1, p2, pm)

                    if not gg:
                        p1, p2, again, gg, pm = player(p1, p2)
                        while again and not gg:
                            print("\x1b[0;30;44mYour Turn Again!\x1b[0m")
                            p1, p2, again, gg, pm = player(p1, p2)
        cls()


if __name__ == '__main__':
    main()
