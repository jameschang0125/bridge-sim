import numpy as np
from loader import Loader
import itertools
# from sklearn.linear_model import LogisticRegression as LR
import statsmodels.api as sm
import pandas as pd
from tqdm import tqdm

class Analyzer:
    def __init__(self, **kwargs):
        self.L = Loader(**kwargs)
    
    def __preprocess(self, X, Y, N, filt):
        '''
        X   : a collection of functions f(deal, dir, suit)
        Y   : deal, res, dir, suit -> R
        N   : # of deals analyzed
        filt: deal -> bool[2][5], indicates which contracts are analyzed
        ret : x, y

        NOTE: this might be a bit inefficient when X is suit-invariant and ft gives many True values
        '''
        deals, ress = self.L.load(N)
        print("[PROGRESS] __preprocess: Finish loading deal")
        x, y = [], []
        for n in tqdm(range(N)):
            deal, res = deals[n], ress[n]
            ft = filt(deal)
            for i, j in itertools.product(range(2), range(5)):
                if ft[i][j]:
                    tmpx = [f(deal, i, j) for f in X]
                    tmpy = Y(deal, res, i, j)
                    x.append(tmpx), y.append(tmpy)
        return np.array(x), np.array(y)
    
    def logit(self, X, Y, Xname, Yname, N, filt, addConst = True):
        '''
        X       : a collection of functions f(deal, dir, suit)
        Y       : deal, res -> R
        Xname   : names of the variables
        Yname   : name of dependent variable # NOTE: [name]
        N       : # of deals analyzed
        filt    : deal -> bool[2][5], indicates which contracts are analyzed
        addConst: whether constant term is added during the regression
        '''
        x, y = self.__preprocess(X, Y, N, filt)
        x = pd.DataFrame(x, columns = Xname)
        y = pd.DataFrame(y, columns = Yname)
        if addConst:
            x = sm.add_constant(x)
        print("[PROGRESS] Logit: fitting...")
        reg = sm.Logit(y, x).fit(cov_type = 'HC3', tol = 1e-10)
        print(reg.summary())
    

                

