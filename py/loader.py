import sys
import numpy as np

class Loader:
    def __init__(self, dealp = "../data/deal", resp = "../data/res", **unused):
        self.fd = open(dealp, "rb")
        self.fr = open(resp, "rb")

    def __loadres(self, N):
        '''
        WARN: no boundary check
        '''
        x = self.fr.read(80 * N)
        return np.array([[[int.from_bytes(x[80 * n + 4 * (i * 4 + j) : 80 * n + 4 * (i * 4 + j + 1)], sys.byteorder) 
            for j in range(4)] for i in range(5)] for n in range(N)])

    def __loaddeal(self, N):
        '''
        WARN: no boundary check
        '''
        x = self.fd.read(64 * N)
        return np.array([[[int.from_bytes(x[64 * n + 4 * (i * 4 + j) : 64 * n + 4 * (i * 4 + j + 1)], sys.byteorder) 
            for j in range(4)] for i in range(4)] for n in range(N)])
    
    def load(self, N = 1):
        '''
        deal[dir][suit], res[suit][dir]
        '''
        return self.__loaddeal(N), self.__loadres(N)
        