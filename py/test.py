from system import System_1D_1S_2m
from sim import SystemSimulator
import pandas as pd

system = System_1D_1S_2m()
simulator = SystemSimulator()

result = simulator.sim(system)
with pd.option_context('display.precision', 1):
    print(result)
