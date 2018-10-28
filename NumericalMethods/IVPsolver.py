from NumericalMethods import IVP_methods
import numpy as np
import math


def cubic_root(x): return math.copysign(math.pow(abs(x), 1.0 / 3.0), x)


class IVPsolver(IVP_methods.Grid):
    def __init__(self, x0, y0, N, xn):
        self.x0, self.y0, self.N, self.xn = x0, y0, N, xn
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        self.x[0], self.y[0] = x0, y0
        self.const = 1 / (np.power(x0 * y0, 3)) + 3 * x0
        self.h = (xn - x0) / N
        self.neighborhood = self.h / 2
        self.break_point = self.const / 3 - self.neighborhood, self.const / 3 + self.neighborhood
        if self.is_in_break_point(self.x0, self.break_point, self.neighborhood):
            self.x0 += self.h
            self.x[0] = self.x0
            self.y0 = self.get_exact(self.x0)
            self.y[0] = self.y0
            self.xn += self.h
        for i in range(1, len(self.x)):
            self.x[i] = self.x[i - 1] + self.h

    def __get_break_points(self):
        """

        :return: indexes of break points
        """
        return [i for i in range(len(self.x)) if self.is_in_break_point(self.x[i], self.break_point, self.neighborhood)]

    def get_exact(self, x):
        return 1 / (cubic_root(self.const * (x ** 3) - 3 * (x ** 4)))

    def solve(self, method):
        """
        Define break points and solve IVP on several subarrays
        :param method: Method name
        :return: y data
        """
        break_points = self.__get_break_points()
        break_points.sort()
        if self.is_in_break_point(self.x0, self.break_point, self.neighborhood):
            raise ZeroDivisionError
        if len(break_points) == 0:
            self.y = [self.apply(self.x0, self.y0, self.N, self.xn, method)]
            self.x = [self.x]
        elif len(break_points) == 1:
            new_x0 = self.x[break_points[0] + 2]
            new_n1 = int(np.ceil((self.x[break_points[0] - 1] - self.x0) / self.h))
            new_n2 = self.N - new_n1 - 3
            if new_n1 != 0:
                self.y = self.apply(self.x0, self.y0, new_n1, self.x[break_points[0] - 1], method), \
                         self.apply(new_x0, self.get_exact(new_x0), new_n2, self.xn + self.h, method)

                self.x = [self.x[i] for i in range(0, len(self.y[0]))], \
                         [self.x[i] for i in range(break_points[0] + 2, break_points[0] + 2 + len(self.y[1]))]

            else:
                self.y = [self.apply(new_x0, self.get_exact(new_x0), new_n2, self.xn + self.h, method)]
                self.x = [[self.x[i] for i in range(break_points[0] + 2, break_points[0] + 2 + len(self.y[0]))]]
        else:
            new_x0_0 = self.x[break_points[0] + 1]
            new_x0_1 = self.x[break_points[1] + 1]
            new_n1 = int(np.ceil((self.x[break_points[0] - 1] - self.x0) / self.h))
            new_n2 = int(np.ceil((self.x[break_points[1] - 1] - new_x0_0) / self.h))
            new_n3 = self.N - new_n2 - new_n1
            self.y = self.apply(self.x0, self.y0, new_n1, self.x[break_points[0] - 1], method), \
                     self.apply(new_x0_0, self.get_exact(new_x0_0), new_n2, self.x[break_points[1] - 1], method), \
                     self.apply(new_x0_1, self.get_exact(new_x0_1), new_n3, self.xn, method)

    def apply(self, x0=None, y0=None, N=None, xn=None, method=None):
        solver: IVP_methods.Grid
        if method == 'exact':
            solver = IVP_methods.ExactFunction(x0, y0, N, xn)
        if method == 'eiler':
            solver = IVP_methods.EilerMethod(x0, y0, N, xn)
        if method == 'impr_eiler':
            solver = IVP_methods.ImprovedEilerMethod(x0, y0, N, xn)
        if method == 'runge_kutta':
            solver = IVP_methods.RungeKuttaMethod(x0, y0, N, xn)

        solver.apply()

        return solver.y
