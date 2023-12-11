# simple simulator
# given a "system", evaluate the results
# a "system" is a func : deal -> contract (could be None)
from loader import Loader
from utils import contract_str, all_rotation
import pandas as pd
from tqdm import tqdm

class SystemSimulator():
    '''
    currently written for non-comp
    '''

    def __init__(self, **kwargs):
        self.L = Loader(**kwargs)

    def __sim(self, sys, deal, res):
        if (tmp := sys(deal)) is None:
            return None
        suit, lvl, dealer = tmp
        result = res[suit][dealer] - (6 + lvl)
        return (suit, lvl), result

    def sim(self, sys, N = 10000):
        deals, ress = self.L.load(N)
        ans, tot = {}, 0
        for i in tqdm(range(N)):
            for deal, res in all_rotation(deals[i], ress[i]):
                tmp = self.__sim(sys, deal, res)
                if tmp is not None:
                    tot += 1
                    contract, result = tmp
                    contract = contract_str(*contract)
                    if contract not in ans:
                        ans[contract] = {}
                    ans[contract][result] = ans[contract].get(result, 0) + 1
        
        # summary
        print(f"{tot} deals analyzed")
        df = pd.DataFrame.from_dict(ans).T
        df = df.sort_index(axis = 0).sort_index(axis = 1).fillna(0) / tot * 100
        return df

