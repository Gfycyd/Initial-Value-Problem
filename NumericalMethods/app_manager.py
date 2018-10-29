from matplotlib import pyplot as plt
from NumericalMethods.IVPsolver import IVPsolver
from NumericalMethods.Error import ErrorCalculator as e


class GraphsBuilder:
    def __init__(self, x0, y0, N, xn):
        self.x0, self.y0, self.N, self.xn = x0, y0, N, xn

    def get_graph(self) :
        """
        Plot IVP solution for all methods and exact
        """
        plt.close(1)
        plt.figure(1)
        plt.ylabel('y')
        plt.xlabel('x')
        exact = IVPsolver(self.x0, self.y0, self.N, self.xn)
        eiler = IVPsolver(self.x0, self.y0, self.N, self.xn)
        improved_eiler = IVPsolver(self.x0, self.y0, self.N, self.xn)
        runge_kutta = IVPsolver(self.x0, self.y0, self.N, self.xn)
        eiler.solve('eiler')
        exact.solve('exact')
        improved_eiler.solve('impr_eiler')
        runge_kutta.solve('runge_kutta')
        plt.plot(exact.x[0], exact.y[0], label=u'Exact', color='g')
        plt.plot(eiler.x[0], eiler.y[0], label=u'Eiler', color='r')
        plt.plot(improved_eiler.x[0], improved_eiler.y[0], label=u'Improved-Eiler', color='b')
        plt.plot(runge_kutta.x[0], runge_kutta.y[0], label=u'Runge-Kutta', color='y')
        if len(exact.x) > 1:
            for i in range(1, len(exact.x)):
                plt.plot(exact.x[i], exact.y[i], color='g')
                plt.plot(eiler.x[i], eiler.y[i], color='r')
                plt.plot(improved_eiler.x[i], improved_eiler.y[i], color='b')
                plt.plot(runge_kutta.x[i], runge_kutta.y[i], color='y')

        plt.title('IVP problem:')
        plt.legend()
        return plt.figure(1)

    def local_error_graph(self) -> plt.figure:
        """
        Plot local error graph
        :return:
        """
        plt.close(2)
        plt.figure(2)
        plt.ylabel('Local error')
        plt.xlabel('x')
        exact = IVPsolver(self.x0, self.y0, self.N, self.xn)
        eiler = IVPsolver(self.x0, self.y0, self.N, self.xn)
        improved_eiler = IVPsolver(self.x0, self.y0, self.N, self.xn)
        runge_kutta = IVPsolver(self.x0, self.y0, self.N, self.xn)
        eiler.solve('eiler')
        exact.solve('exact')
        improved_eiler.solve('impr_eiler')
        runge_kutta.solve('runge_kutta')
        domain = []
        for i in range(len(exact.x)):
            domain.append(exact.x[i][1:])

        plt.plot(domain[0], e.local_error(exact.y[0], eiler.y[0]), label=u'Eiler', color='r')
        plt.plot(domain[0], e.local_error(exact.y[0], improved_eiler.y[0]), label=u'Improved-Eiler', color='g')
        plt.plot(domain[0], e.local_error(exact.y[0], runge_kutta.y[0]), label=u'Runge-Kutta', color='y')
        for i in range(len(exact.x)):
            plt.plot(domain[i], e.local_error(exact.y[i], eiler.y[i]), color='r')
            plt.plot(domain[i], e.local_error(exact.y[i], improved_eiler.y[i]), color='g')
            plt.plot(domain[i], e.local_error(exact.y[i], runge_kutta.y[i]), color='y')

        plt.title('Local Error Graph')
        plt.legend()
        return plt.figure(2)

    def global_error_graph(self) -> plt.figure:
        """
        Plot global error graph.
        """
        plt.close(3)
        plt.figure(3)
        plt.ylabel('Global error')
        plt.xlabel('N')
        x = [i for i in range(20, 50, 1)]
        eiler = e.global_error('eiler', self.x0, self.y0, self.xn)
        impr_eiler = e.global_error('impr_eiler', self.x0, self.y0, self.xn)
        runge_kutta = e.global_error('runge_kutta', self.x0, self.y0, self.xn)
        plt.plot(x, eiler, label='Eiler', color='r')
        plt.plot(x, impr_eiler, label='Improved Eiler', color='g')
        plt.plot(x, runge_kutta, label='Runge-Kutta', color='y')
        plt.title('Global Error Graph')
        plt.legend()
        return plt.figure(3)
