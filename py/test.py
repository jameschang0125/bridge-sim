from system import System_1D_1S_2m
from sim import SystemSimulator
import pandas as pd
from utils import IMP, contract_str, score

def test_scoring_and_IMP():
    for i in (-3000, -450, -50, 0, 180, 250, 450, 620, 1430):
        print(f'the score {i} is equal to {IMP(i)} IMPs')
    for lvl, suit, result in (
        (1, 4, 0),
        (3, 4, 0),
        (1, 1, -7),
        (7, 3, 0),
        (6, 0, 0),
        (6, 2, 0),
        (6, 4, 0),
    ):
        print(f"{contract_str(lvl, suit)}{'+' if result >= 0 else ''}{result}'s \
            score is {score(lvl, suit, result)}")

def test_system_and_sim():
    system1, system2 = System_1D_1S_2m(), System_1D_1S_2m(allow_2C = False)
    simulator = SystemSimulator()

    with pd.option_context('display.float_format', '{:,.1f}'.format):
        print(simulator.sim(system1, 5000))
        print(simulator.sim(system2, 5000))
