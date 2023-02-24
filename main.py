# Author: Jacob Hess

import json
from rl_incidnt_j import RlIncidents, dataInc, errorInc

workInc = 0

while True:

    if RlIncidents():
        rdataInc = json.loads(dataInc)
        workInc = True
    elif workInc == True:
        print(errorInc)
        workInc = False
    elif workInc == 0:
        print(errorInc)
    
    
