"""
Turkish Mancala Bot (v1.0)
Made by Ege Şimşek, visit (www.smsk.one)
"""
import copy
from os import system, name
from time import sleep


def possible(p):
    return [i for i in range(1, 7) if p[i] != 0]


def status(p1, p2):
    print("\x1b[3;31;40m-----------------\x1b[0m")
    print("\x1b[1;33;40m  " + ' '.join(str(x) for x in p2[1:][::-1]))
    print(str(p2[0]) + "\x1b[0m" + ' ' * 13 + "\x1b[1;32;40m" + str(p1[0]))
    print("  " + ' '.join(str(x) for x in p1[1:][::-1]) + "\x1b[0m")


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
    extra = [0, -1]

    for j in range(v):
        cur = 8 - move + j
        last = v == j + 1
        if cur == 7 or cur == 21 or cur == 35:
            temp_p1[0] += 1
            if last or val == 1:
                again = True
        elif 28 > cur > 21:
            temp_p2[cur - 21] += 1
            if temp_p2[cur - 21] % 2 == 0 and last:
                temp_p1[0] += temp_p2[cur - 21]
                extra = [temp_p2[cur - 21], 0]
                temp_p2[cur - 21] = 0
        elif 14 > cur > 7:
            temp_p2[cur - 7] += 1
            if temp_p2[cur - 7] % 2 == 0 and last:
                temp_p1[0] += temp_p2[cur - 7]
                extra = [temp_p2[cur - 7], 0]
                temp_p2[cur - 7] = 0
        elif 35 > cur > 28:
            temp_p1[35 - cur] += 1
            if temp_p1[35 - cur] == 1 and temp_p2[35 - cur] != 0 and last:
                temp_p1[0] += temp_p1[35 - cur] + temp_p2[35 - cur]
                extra = [temp_p1[35 - cur] + temp_p2[35 - cur], 1]
                temp_p1[35 - cur] = 0
                temp_p2[35 - cur] = 0
        elif 21 > cur > 14:
            temp_p1[21 - cur] += 1
            if temp_p1[21 - cur] == 1 and temp_p2[21 - cur] != 0 and last:
                temp_p1[0] += temp_p1[21 - cur] + temp_p2[21 - cur]
                extra = [temp_p1[21 - cur] + temp_p2[21 - cur], 1]
                temp_p1[21 - cur] = 0
                temp_p2[21 - cur] = 0
        elif 7 > cur:
            temp_p1[7 - cur] += 1
            if temp_p1[7 - cur] == 1 and temp_p2[7 - cur] != 0 and last:
                temp_p1[0] += temp_p1[7 - cur] + temp_p2[7 - cur]
                extra = [temp_p1[7 - cur] + temp_p2[7 - cur], 1]
                temp_p1[7 - cur] = 0
                temp_p2[7 - cur] = 0

    if val == 1:
        temp_p1[move] = 0
    else:
        temp_p1[move] = 1

    temp_p1, temp_p2, gg = check_gg(temp_p1, temp_p2)
    return temp_p1, temp_p2, again, gg, extra


def evaluate(p1, p2):
    # Tactic 1: The less piece you have the better.
    piece_difference = sum(p2[1:]) - sum(p1[1:])

    # Tactic 2: Empty and Double Rules (Extra Gain)
    max_extra_p1 = 0
    for i in possible(p1):
        p1x = copy.copy(p1)
        p2x = copy.copy(p2)
        extra = make_move(i, p1x, p2x)[4][0]
        max_extra_p1 = extra if extra > max_extra_p1 else max_extra_p1
    max_extra_p2 = 0
    for i in possible(p2):
        p1x = copy.copy(p1)
        p2x = copy.copy(p2)
        extra = make_move(i, p2x, p1x)[4][0]
        max_extra_p2 = extra if extra > max_extra_p2 else max_extra_p2
    max_extra = max_extra_p1 - max_extra_p2 * 1.2

    # Tactic 3: Balance your stones (defense: 4, 5, 6 and attack: 1, 2, 3)
    side_difference = sum(p1[1:4]) - sum(p1[4:7])

    # Tactic 4: Enlarge your treasure to the max
    treasure_difference = sum(p1[1:]) - sum(p2[1:]) * 1.2
    board = sum(p1[1:]) + sum(p2[1:])
    if board >= 40: treasure_factor = 1.8
    elif board >= 30: treasure_factor = 2.0
    elif board >= 20: treasure_factor = 1.5
    elif board >= 15: treasure_factor = 2.0
    elif board >= 10: treasure_factor = 2.5
    elif board >= 5: treasure_factor = 3.0
    else: treasure_factor = 3.5

    # Tactic 5: Ladder Tactic
    ladder = 0
    if p1[1] in [1, 15, 29]: ladder += 1
    if p1[1] == 2: ladder += 1.5
    if p1[2] in [3, 16, 30]: ladder += 1
    if p1[3] in [4, 17, 31]: ladder += 1
    if p1[4] in [5, 18, 32]: ladder += 1
    if p1[5] in [6, 19, 33]: ladder += 1
    if p1[6] in [7, 20, 34]: ladder += 1
    if p2[1] in [1, 15, 29]: ladder -= 1.2
    if p2[1] == 2: ladder -= 2
    if p2[2] in [3, 16, 30]: ladder -= 1.2
    if p2[3] in [4, 17, 31]: ladder -= 1.2
    if p2[4] in [5, 18, 32]: ladder -= 1.2
    if p2[5] in [6, 19, 33]: ladder -= 1.2
    if p2[6] in [7, 20, 34]: ladder -= 1.2

    return (piece_difference * 0.7 + max_extra * 1.2 + side_difference * 0.5 +
            treasure_difference * treasure_factor + ladder * 0.7)


def bot(p1x, p2x):
    p1 = p1x.copy()
    p2 = p2x.copy()
    p1 = [p1[0]] + p1[1:][::-1]
    p2 = [p2[0]] + p2[1:][::-1]

    pos = possible(p2)
    best = pos[0]
    bv = None

    for i in pos:
        a, b, _, _, _ = make_move(i, p2, p1)
        ev = evaluate(a, b)
        if bv is None:
            bv = ev
        elif ev > bv:
            best = i
            bv = ev

    p2, p1, again, gg, _ = make_move(best, p2, p1)
    p1 = [p1[0]] + p1[1:][::-1]
    p2 = [p2[0]] + p2[1:][::-1]

    if again and not gg:
        status(p1, p2)
        sleep(1.5)
        return bot(p1, p2)

    return p1, p2, gg


def main():
    p1 = [0, 4, 4, 4, 4, 4, 4]
    p2 = [0, 4, 4, 4, 4, 4, 4]
    gg = False
    while True:
        status(p1, p2)
        if gg:
            print("Game Over!")
            input()

        move = int(input("\x1b[3;30;47mMove (1 to 6): "))
        while move not in possible(p1):
            move = int(input("\x1b[3;30;47mMove (1 to 6): \x1b[0m"))
        print("\x1b[0m")
        p1, p2, again, gg, _ = make_move(move, p1, p2)

        if name == 'nt':
            system('cls')
        else:
            system('clear')

        if not gg:
            if again:
                print("\x1b[0;30;44mYour Turn Again!\x1b[0m")
            else:
                status(p1, p2)
                sleep(1.5)
                p1, p2, gg = bot(p1, p2)


if __name__ == '__main__':
    main()
