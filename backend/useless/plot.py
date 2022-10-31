import matplotlib.pyplot as plt

x = pd.readcsv('density.csv')
y = pd.readcsv('speed.csv')
plt.plot(x, y)
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.show()
