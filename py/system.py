# a very very simple example of (non-comp) system
from evals import HandEvaluator

class System_1D_1S_2m():
    def __init__(self, allow_2C = True):
        self.HE = HandEvaluator()
        self.allow_2C = allow_2C

    def __call__(self, deal):
        '''
        return lvl, suit, dealer
        '''

        # 1D - 2m
        N_suit, N_HCP = self.HE.suit(deal, 0), self.HE.HCP(deal, 0)
        if (N_suit[1] < N_suit[0]) or (N_suit[1] <= N_suit[2]) or (N_suit[1] <= N_suit[3]) or \
            (N_suit[3] >= 4) or (N_suit[1] >= 8) or \
            (not 11 <= N_HCP <= 14) or self.HE.isbal(deal, 0):
            return None
        # 1S
        S_suit, S_HCP = self.HE.suit(deal, 2), self.HE.HCP(deal, 2)
        if not 6 <= S_HCP <= 12:
            return None
        if 6 <= S_HCP <= 10:
            if (not 4 <= S_suit[3] <= 7) or \
                (S_suit[3] == 4 and S_suit[1] >= 3) or \
                (S_suit[3] >= 4 and S_suit[2] >= 4):
                return None
        if 11 <= S_HCP <= 12:
            if (not 4 <= S_suit[3] <= 7) or \
                (S_suit[3] == 4 and S_suit[2] == 4) or \
                (S_suit[3] < S_suit[2]):
                return None
        
        # 1D; 2C
        if N_suit[0] >= 4:
            if S_HCP <= 10:
                if self.allow_2C and S_suit[0] >= 4:
                    return 2, 0, 0
                if S_suit[1] >= 2:
                    return 2, 1, 0
                if self.allow_2C and S_suit[0] == 3:
                    return 2, 0, 0
                return 2, 3, 2
            else:
                if N_HCP >= 13:
                    if S_suit[3] + N_suit[3] >= 8:
                        return 4, 3, 2
                    if self.HE.stopper(deal, 2):
                        return 3, 4, 2
                    return 3, 4, 0
                else:
                    if S_suit[3] >= 5:
                        if N_suit[3] >= 3:
                            return 3, 3, 2
                        if self.HE.stopper(deal, 0):
                            return 2, 4, 0
                        if N_suit[1] >= 6:
                            return 3, 1, 0
                        if S_suit[0] >= 4:
                            return 3, 0, 0
                        if S_suit[1] >= 2:
                            return 3, 1, 0
                        if S_suit[0] == 3:
                            return 3, 0, 0
                        return 3, 3, 2
                    else:
                        if self.HE.stopper(deal, 2):
                            return 2, 4, 2
                        if S_suit[1] >= 3:
                            return 3, 1, 0
                        if S_suit[0] >= 4:
                            return 3, 0, 0
                        return 2, 4, 2
        
        # 1D; 2D
        if S_HCP <= 10:
            if S_suit[1] >= 2:
                return 2, 1, 0
            if N_suit[3] >= 5:
                return 2, 3, 2
            return 2, 1, 0
        else:
            if N_HCP >= 13:
                if S_suit[3] + N_suit[3] >= 8:
                    return 4, 3, 2
                if self.HE.stopper(deal, 2):
                    return 3, 4, 2
                return 3, 4, 0
            else:
                if S_suit[3] >= 5:
                    if N_suit[3] >= 3:
                        return 3, 3, 2
                    if self.HE.stopper(deal, 0):
                        return 2, 4, 0
                    return 3, 1, 0
                else:
                    if self.HE.stopper(deal, 2):
                        return 2, 4, 2
                    if S_suit[1] >= 3:
                        return 3, 1, 0
                    return 2, 4, 2



        

