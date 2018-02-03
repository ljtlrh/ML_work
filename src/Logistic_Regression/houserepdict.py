#!/usr/bin/env python
#-*- coding:UTF-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

year = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
price = [2.000, 2.500, 2.900, 3.147, 4.515, 4.903, 5.365, 5.704, 6.853, 7.971, 8.561, 10.000, 11.280, 12.900]


def predict():
	s1=0
	s2=0
	k2=-5
	k3=0
	k4=0
	a=0.001
	k1=0
	while True:
		s2=0
		k3=0
		k4=0
		i=0
		while i<14:
			s2+=(k1+k2*year[i]-price[i])*(k1+k2*year[i]-price[i])/2;
			k3+= k1+k2*year[i]-price[i];
			k4+=(k1+k2*year[i]-price[i])*year[i];
			i+=1
		k1=k1-k3*a/14;
		k2=k2-k4*a/14;
		if math.fabs(s2-s1)<0.0000001:
			print(k2 , k1)
			print((k1+k2*14))
			break
		s1 = s2;
predict()