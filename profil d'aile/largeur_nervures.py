# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:34:34 2026

@author: julie
"""

import numpy as np

emax=15
emin=12.5
l=20
n=4


a=(emax-emin)/l
x=np.array([i*l/n for i in range(n+1)])


def f(x):
    return emax-a*x

print(f(x))
