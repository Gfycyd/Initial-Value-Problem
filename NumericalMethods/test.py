import matplotlib.pyplot as plt
import numpy as np

a = 1
x = np.arange(-2*np.pi, 2*np.pi, 0.2)
y = np.sin(x) * np.cos(x)
f = np.sin(x) + np.cos(x)
xz = a*(2*np.cos(x) - np.cos(2*x))
yz = a*(2*np.sin(x) - np.sin(2*x))

# ?????? 1 ? ??????? label
plt.plot(x, f, label = u'????? cos ? sin')
plt.scatter(x, y, label = u'???????????? cos ? sin', color='r')
plt.plot(xz, yz, label = u'?????????')

plt.grid(True)
plt.xlabel(u'????????')
plt.ylabel(u'???????')
plt.title(u'????????? ????????')

plt.legend()   # ??????? ??? ????? ??????? fig


plt.show()