import numpy as np
from itertools import permutations

SUIT_MAP = "CDHSN"

def contract_str(lvl, suit = None):
    if suit is None:
        lvl, suit = lvl
    return str(lvl) + SUIT_MAP[suit]

def all_rotation(deal, res):
    return [rotate(deal, res, dealer, suit_order) for dealer in range(4) for suit_order in permutations(np.arange(4))]

def rotate(deal, res, dealer = 0, suit_order = np.arange(4)):
    player_order = (np.arange(4) + dealer) % 4
    # equivalent to deal[player_order, :][:, suit_order]
    return deal[np.ix_(player_order, suit_order)], res[np.ix_(np.append(suit_order, 4), player_order)]

PARTIAL_BONUS = [50, 50]
GAME_BONUS = [300, 500]
SLAM_BONUS = [500 + 300, 750 + 500]
GRAND_SLAM_BONUS = [1000 + 300, 1500 + 500]

def score(lvl, suit, result = 0, vul = True, double = 0):
    # TODO: double
    vul = int(vul)
    if result >= 0:
        pt_per_trick = 20 if suit <= 1 else 30
        add_contract_pt = 10 if suit == 4 else 0
        contract_pt = (pt_per_trick * lvl + add_contract_pt) * (2 ** double)
        overtrick_pt = pt_per_trick * result if double == 0 else 50 * (2 ** (double + vul))
        double_bonus = 50 * double
        if lvl == 7:
            bonus = GRAND_SLAM_BONUS[vul]
        elif lvl == 6:
            bonus = SLAM_BONUS[vul]
        elif contract_pt >= 100:
            bonus = GAME_BONUS[vul]
        else:
            bonus = PARTIAL_BONUS[vul]
        return contract_pt + overtrick_pt + double_bonus + bonus
    else:
        if double == 0:
            return 50 * (1 + vul) * result
        if double == 1:
            if vul:
                return 300 * result + 100
            if result >= -3:
                return 200 * result + 100
            return 300 * result + 400

IMP_BREAKPOINTS = np.array([
    20, 50, 90, 130, 170, 220, 270, 320, 370, 430, 500, 600, 750, 900, 1100, 
    1300, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000
])

def IMP(score):
    if score < 0:
        return -IMP(-score)
    return np.searchsorted(IMP_BREAKPOINTS, score, 'right')

