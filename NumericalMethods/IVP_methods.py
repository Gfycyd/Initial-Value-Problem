import numpy as np
import math


def cubic_root(x): return math.copysign(math.pow(abs(x), 1.0 / 3.0), x)


class Grid:
    x: np.array
    y: np.array
    const: float
    neighborhood: float

    @staticmethod
    def derivative(x, y) -> float:
        """
        Calculate derivative of our function in some point
        :param x: x coordinate of point
        :param y: y coordinate of point
        :return: float value of derivative in this point
        """
        return (x ** 3) * (y ** 4) - y / x

    @staticmethod
    def is_in_break_point(x, break_point, neighborhood) -> bool:
        """
        Check X on discontinuity
        :param x: X value
        :param break_point: point of discontinuity
        :param neighborhood: neighborhood size
        :return: True/False
        """
        return break_point[1] > x > break_point[0] or neighborhood > x > -neighborhood

    def apply(self, x0=None, y0=None, N=None, xn=None, method=None):
        """
        Apply corresponding method for IVP with this input data
        :param x0: x of initial point
        :param y0: y of initial point
        :param N: amount of splits
        :param xn: x of end point
        :param method: method name
        :return:
        """
        pass


class ExactFunction(Grid):
    def __init__(self, x0, y0, N, xn):
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        h = (xn - x0) / N
        self.const = 1 / (np.power(x0 * y0, 3)) + 3 * x0
        self.neighborhood = h / 2
        self.break_point = self.const / 3 - self.neighborhood, self.const / 3 + self.neighborhood
        self.x[0] = x0
        for i in range(1, len(self.x)):
            self.x[i] = self.x[i - 1] + h

        self.y[0] = y0

        for i in range(1, len(self.x)):
            self.y[i] = self.get_exact(self.x[i])

    def get_exact(self, x) -> float:
        """
        Return exact value of function in this point
        :param x: x coordinate
        :return: float
        """
        return 1 / (cubic_root(self.const * (x ** 3) - 3 * (x ** 4)))


class EilerMethod(Grid):
    def __init__(self, x0, y0, N, xn):
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        self.x[0], self.y[0] = x0, y0
        self.const = 1 / (np.power(x0 * y0, 3)) + 3 * x0
        self.h = (xn - x0) / N
        self.neighborhood = self.h / 2
        self.break_point = self.const / 3 - self.neighborhood, self.const / 3 + self.neighborhood
        for i in range(1, len(self.x)):
            self.x[i] = self.x[i - 1] + self.h

    def get_exact(self, x):
        if self.is_in_break_point(x, self.break_point, self.neighborhood):
            return 10000
        else:
            return 1 / (cubic_root(self.const * (x ** 3) - 3 * (x ** 4)))

    def apply(self, x0=None, y0=None, N=None, xn=None, method=None):
        for i in range(1, len(self.x)):
            self.y[i] = self.y[i - 1] + self.h * self.derivative(self.x[i - 1], self.y[i - 1])


class ImprovedEilerMethod(EilerMethod):
    def apply(self, x0=None, y0=None, N=None, xn=None, method=None):
        for i in range(1, len(self.x)):
            f1 = self.derivative(self.x[i - 1], self.y[i - 1])
            f2 = self.derivative(self.x[i], self.y[i - 1] + self.h * f1)
            self.y[i] = self.y[i - 1] + (self.h / 2) * (f1 + f2)


class RungeKuttaMethod(EilerMethod):
    def apply(self, x0=None, y0=None, N=None, xn=None, method=None):
        for i in range(1, len(self.x)):
            k1 = self.derivative(self.x[i - 1], self.y[i - 1])
            k2 = self.derivative(self.x[i - 1] + self.h / 2, self.y[i - 1] + self.h * k1 / 2)
            k3 = self.derivative(self.x[i - 1] + self.h / 2, self.y[i - 1] + self.h * k2 / 2)
            k4 = self.derivative(self.x[i], self.y[i - 1] + self.h * k3)
            self.y[i] = self.y[i - 1] + (self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
