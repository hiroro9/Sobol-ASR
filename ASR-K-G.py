#!/usr/bin/env python
# coding: utf-8

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import pandas as pd

n1 = int(input("please input n1: "))
n2 = int(input("please input n2: "))
n3 = int(input("please input n3: "))

#====== input parameter ====================#
nn = np.matrix([[n1],[n2],[n3]])  #cosine vector
sampling = 5000  # sampling number for saltelli sampling
time = 100  # time for ASR measurement
#================================================#


dirc = str(nn[0,0]) + str(nn[1,0])+str(nn[2,0])
print(dirc)


def ASR(t, s11, s22, s33, s12, s13, s23, p0, ts, tv):
    #n = np.matrix([[n11,n12,n13,n14,n15,n16, n17, n18, n19],[n21,n22,n23,n24,n25,n26, n27, n28, n29],[n31,n32,n33,n34,n35,n36, n37, n38, n39]])
    K = 50
    G = 30
    
    n = nn / np.linalg.norm(nn)

    Jav = (1-np.exp(-t/tv))/(3*K*10**3)
    Jas = (1-np.exp(-t/ts))/(2*G*10**3)
    
    nTn = (s11*n[0]*n[0] + s22*n[1]*n[1] + s33*n[2]*n[2]
           + 2*s12*n[0]*n[1] + 2*s23*n[1]*n[2] + 2*s13*n[0]*n[2]
          )
    
    sm = (1.0/3.0)*(s11 + s22 + s33)
  
    es = (nTn - sm)*Jas
    ev = (sm - p0)*Jav
    
    e = es + ev
    
    return e*10**6


problem = {
    'num_vars': 9,
    'names': [ 's11', 's22', 's33', 's12', 's13', 's23', 'p0', 'ts', 'tv'],
    'bounds': [[0, 100]*9,
#              [0, 100],
#              [35, 45],
#              [0, 100],
#              [0, 100],
#              [0, 100],
#              [2, 12],
#              [0, 100],
#              [0, 100],
               ]
}



param_values = saltelli.sample(problem, sampling)


def S(t):
    Y = np.zeros([param_values.shape[0]])
    
    for i, (s11, s22, s33, s12, s13, s23, p0, ts, tv) in enumerate(param_values):
        Y[i] = ASR(t, s11, s22, s33, s12, s13, s23, p0, ts, tv)
        
    Si = sobol.analyze(problem, Y, print_to_console=False)
    
    out = np.array([[t]])
    outT = np.array([[t]])
    
    for i in range(0, 9):
        inn = np.array([
            [Si["S1"][i], Si["S1_conf"][i]]
        ])
        out = np.hstack([out, inn])

    for iT in range(0, 9):
        innT = np.array([
            [Si["ST"][iT], Si["ST_conf"][iT]]
        ])
        outT = np.hstack([outT, innT])
        
        
    return out, outT


columns = ["time[h]",
           "s11","s11_err",
           "s22","s22_err",
           "s33","s33_err",
           "s12","s12_err",
           "s13","s13_err",
           "s23","s23_err",
           "p0","p0_err",
           "ts","ts_err",
           "tv","tv_err"
          ]

Sobol_Si = pd.DataFrame(index=[], columns=columns)
Sobol_ST = pd.DataFrame(index=[], columns=columns)

for t in range(1, time, 5):
    SI = S(t)

    Si_p = pd.DataFrame(data = SI[0], columns = columns)
    Sobol_Si = Sobol_Si.append(Si_p)

    ST_p = pd.DataFrame(data = SI[1], columns = columns)
    Sobol_ST = Sobol_ST.append(ST_p)

Sobol_Si.to_csv("output/" + "Si_K_G_svpp" + dirc + ".csv", index=False)
Sobol_ST.to_csv("output/" + "ST_K_G_svpp" + dirc + ".csv", index=False)
