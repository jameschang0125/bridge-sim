import numpy as np
from itertools import permutations

SUIT_MAP = "CDHSN"

def contract_str(suit, lvl):
    return str(lvl) + SUIT_MAP[suit]

def all_rotation(deal, res):
    return [rotate(deal, res, dealer, suit_order) for dealer in range(4) for suit_order in permutations(np.arange(4))]

def rotate(deal, res, dealer = 0, suit_order = np.arange(4)):
    player_order = (np.arange(4) + dealer) % 4
    # equivalent to deal[player_order, :][:, suit_order]
    return deal[np.ix_(player_order, suit_order)], res[np.ix_(np.append(suit_order, 4), player_order)]