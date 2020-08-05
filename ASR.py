#!/usr/bin/env python
# coding: utf-8

# In[1]:


from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import pandas as pd

#====== change cosine vector ====================#
nn = np.matrix([[1],[0],[0]]) 
#================================================#


dirc = str(nn[0,0]) + str(nn[1,0])+str(nn[2,0])

def ASR(t, s11, s22, s33, s12, s13, s23, p0, G, K, ts, tv):
    #n = np.matrix([[n11,n12,n13,n14,n15,n16, n17, n18, n19],[n21,n22,n23,n24,n25,n26, n27, n28, n29],[n31,n32,n33,n34,n35,n36, n37, n38, n39]])
   
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
    'num_vars': 11,
    'names': [ 's11', 's22', 's33', 's12', 's13', 's23', 'p0', 'G', 'K' 'ts', 'tv'],
    'bounds': [[0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 100],
               [0, 50],
               [0, 50],
               ]
}



param_values = saltelli.sample(problem, 500)


# In[9]:


def S(t):
    Y = np.zeros([param_values.shape[0]])
    
    for i, (s11, s22, s33, s12, s13, s23, p0, G, K, ts, tv) in enumerate(param_values):
        Y[i] = ASR(t, s11, s22, s33, s12, s13, s23, p0, G, K, ts, tv)
        
    Si = sobol.analyze(problem, Y, print_to_console=False)
    
    out = np.array([[t]])
    
    for i in range(0, 11):
        inn = np.array([
            [Si["S1"][i], Si["S1_conf"][i]]
        ])
        out = np.hstack([out, inn])
        
    return out




columns = ["time[h]",
           "s11","s11_err",
           "s22","s22_err",
           "s33","s33_err",
           "s12","s12_err",
           "s13","s13_err",
           "s23","s23_err",
           "p0","p0_err",
           "G","G_err",
           "K","K_err",
           "ts","ts_err",
           "tv","tv_err"
          ]

Sobol = pd.DataFrame(index=[], columns=columns)


for t in range(1, 500, 10):
    Si_p = pd.DataFrame(data = S(t), columns = columns)
    Sobol = Sobol.append(Si_p)
Sobol.to_csv("Sobol"+dirc + ".csv", index=False)
