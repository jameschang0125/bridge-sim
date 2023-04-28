from stats import Analyzer
from evals import CombEvaluator, ResEvaluator

AN, CE, RE = Analyzer(), CombEvaluator(), ResEvaluator()
X       =  [CE.A, CE.K, CE.Q, CE.J, 
            CE.clipHCPdiff, CE.moreTrump, CE.doubleFit, CE.wasteHS, CE.SS,
            CE.SSWA, CE.SSWK, CE.SSWQ, CE.SSWJ]
Xname   =  ['A', 'K', 'Q', 'J',
            'Imbal', 'Trump', '2Fit', 'HSwst', 'SS',
            'Awst', 'Kwst', 'Qwst', 'Jwst']
Y       =  RE.is4X
Yname   =  ['game']
N       = 100000
filt    = CE.isFit

AN.logit(X, Y, Xname, Yname, N, filt)