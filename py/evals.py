import numpy as np
from functools import partialmethod

def isSet(x, b):
    # bin(x)[b] == '1'
    return 1 if x & (1 << b) else 0

class HandEvaluator:
    def __init__(self):
        pass

    def _bitCount(self, deal, dir = 0, suit = 0, bit = 0):
        return isSet(deal[dir][suit], bit)

    def _bitCounts(self, deal, dir = 0, bit = 0):
        return sum([self._bitCount(deal, dir, i, bit) for i in range(4)])

    def HCP(self, deal, dir = None):
        if dir is None:
            return [self.HCP(deal, i) for i in range(4)]
        return sum([sum([self._bitCount(deal, dir, i, 10 + j) * j for j in range(1, 5)]) for i in range(4)])

    def isbal(self, deal, dir = 0): # strict
        x = sorted(self.suit(deal, dir))
        if x[3] == 4:
            return x[0] > 1
        if x[3] == 5:
            return x[0] == 2 and x[1] == 3  # 5332
        return False

    def stopper(self, deal, dir = 0, suit = 0):
        # A, Kx, Qxx+, Jxxx+
        length = self._suit(deal, dir, suit)
        return self._bitCount(deal, dir, suit, 14) or \
            (self._bitCount(deal, dir, suit, 13) and length >= 2) or \
            (self._bitCount(deal, dir, suit, 12) and length >= 3) or \
            (self._bitCount(deal, dir, suit, 11) and length >= 4)

    def suit(self, deal, dir = None):
        if dir is None:
            return np.array([self.suit(deal, i, suit) for i in range(4)])
        return np.array([self._suit(deal, dir, i) for i in range(4)])

    def _suit(self, deal, dir = 0, suit = 0):
        return bin(deal[dir][suit]).count("1")

    def isSS(self, deal, dir = 0):
        x = self.suit(deal, dir)
        return np.array([x[i] <= 1 for i in range(4)])
    
    def needHS(self, deal, dir = 0):
        return np.array([self.__needHS(deal, dir, i) for i in range(4)])

    def __needHS(self, deal, dir = 0, suit = 0):
        '''
        no AK, exactly 3rd ctrl
        '''
        return self._bitCount(deal, dir, suit, 14) + self._bitCount(deal, dir, suit, 13) == 0 and \
            (self._suit(deal, dir, suit) == 2 or self._bitCount(deal, dir, suit, 12) == 0)

    def isHS(self, deal, dir = 0):
        return np.array([self.__isHS(deal, dir, i) for i in range(4)])

    def notHS(self, deal, dir = 0):
        return np.logical_not(self.isHS(deal, dir))

    def __isHS(self, deal, dir = 0, suit = 0):
        return self._suit(deal, dir, suit) <= 1 or self._bitCount(deal, dir, suit, 14) or self._bitCount(deal, dir, suit, 13)


class CombEvaluator(HandEvaluator):
    '''
    f   : (deal, dir, suit) -> R
    dir : 0 represents NS, else 1
    suit: TrumpSuit
    *unused is used to catch TrumpSuit
    '''
    def __init__(self):
        super().__init__()

    def HCPdiff(self, deal, dir = 0, *unused):
        return abs(self.HCP(deal, dir) - self.HCP(deal, dir + 2))
    
    def clipHCPdiff(self, deal, dir = 0, *unused):
        return max(0, self.HCPdiff(deal, dir) - 10)
 
    def suit2(self, deal, dir = 0, suit = None):
        if suit is None:
            return np.array([self.suit2(deal, dir, i) for i in range(4)])
        return self._suit(deal, dir, suit) + self._suit(deal, dir + 2, suit)

    def isFit(self, deal, dir = None, suit = None):
        if dir is None:
            return np.array([self.isFit(deal, i, suit) for i in range(2)])
        if suit is None:
            return np.array([self.isFit(deal, dir, j) for j in range(5)])
        if suit == 4: return 0
        return int(self.suit2(deal, dir, suit) >= 8)

    def moreTrump(self, deal, dir = 0, suit = 0):
        return self.suit2(deal, dir, suit) - 8

    def __bitCount2(self, deal, dir = 0, *unused, bit = 0):
        return self._bitCounts(deal, dir, bit) + self._bitCounts(deal, dir + 2, bit)

    A = partialmethod(__bitCount2, bit = 14)
    K = partialmethod(__bitCount2, bit = 13)
    Q = partialmethod(__bitCount2, bit = 12)
    J = partialmethod(__bitCount2, bit = 11)
    T = partialmethod(__bitCount2, bit = 10)

    def SS(self, deal, dir = 0, *unused):
        return min(1, sum(self.isSS(deal, dir))) + min(1, sum(self.isSS(deal, dir + 2)))

    def __bitWasteSS(self, deal, dir = 0, *unused, bit = 0):
        ans = 0
        for x, y in [self.isSS(deal, dir), dir + 2], [self.isSS(deal, dir + 2), dir]:
            ans += sum([self._bitCount(deal, y, i, bit) if x[i] else 0 for i in range(4)])
        return ans

    SSWA = partialmethod(__bitWasteSS, bit = 14)
    SSWK = partialmethod(__bitWasteSS, bit = 13)
    SSWQ = partialmethod(__bitWasteSS, bit = 12)
    SSWJ = partialmethod(__bitWasteSS, bit = 11)
    SSWT = partialmethod(__bitWasteSS, bit = 10)

    def doubleFit(self, deal, dir = 0, *unused):
        return (self.suit2(deal, dir) >= 8).sum() >= 2

    def rawasteHS(self, deal, dir = 0, *unused):
        return np.sum(self.needHS(deal, dir) * self.notHS(deal, dir + 2) + \
                    self.needHS(deal, dir + 2) * self.notHS(deal, dir))
    
    def wasteHS(self, deal, dir = 0, *unused):
        return min(1, self.rawasteHS(deal, dir))

class ResEvaluator:
    '''
    f   : (deal, res, dir, suit) -> R
    '''
    def __init__(self):
        pass

    def is4X(self, deal, res, dir, suit):
        return (int(res[suit][dir] >= 10) + int(res[suit][dir + 2] >= 10)) / 2
        