import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from flow import *
import math

x = flow6710()[0]
y = flow6710()[2]
z = flow6710()[1]
a = flow6710()[3]

theta= polyfit(x, y, 2)
xy = []
for i in range(len(x)):
    xy.append(theta[2] + theta[1] * math.pow(x[i], 1) + theta[0] * math.pow(x[i], 2))

zy=[]
theta1= polyfit(z, y, 2)
for i in range(len(x)):
    zy.append(theta1[2] + theta1[1] * math.pow(z[i], 1) + theta1[0] * math.pow(z[i], 2))


plt.scatter(x, y, marker="o", label="left side")
plt.scatter(z, y, marker="v", label = "right side")
plt.legend(loc="upper right")
##plt.plot(x, xy)
##plt.plot(z, zy)

plt.xlabel('density')
plt.ylabel('speed')
plt.show()
