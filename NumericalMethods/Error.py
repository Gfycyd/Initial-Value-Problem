from NumericalMethods.IVPsolver import IVPsolver


class ErrorCalculator:

    @staticmethod
    def local_error(exact, approx) -> list:
        """
        This function calculates locar error.
        :param exact: exact y data
        :param approx: approx y data
        :return: local error data
        """
        return [abs(exact[i] - approx[i]) for i in range(1, len(exact))]

    @staticmethod
    def global_error(approx_method_name, x0, y0, xn) -> list:
        """
        This function calculates global error
        :param approx_method_name: method name
        :param x0: x
        :param y0: y
        :param xn: xn
        :return: global error data
        """
        x = [i for i in range(20, 50, 1)]
        y = [i for i in range(20, 50, 1)]
        for i in range(len(x)):
            exact = IVPsolver(x0, y0, x[i], xn)
            exact.solve('exact')
            approx = IVPsolver(x0, y0, x[i], xn)
            approx.solve(approx_method_name)
            errors = []
            for k in range(len(exact.y)):
                errors.append(ErrorCalculator.local_error(exact.y[k], approx.y[k]))
            global_errors = []
            for j in errors:
                global_errors.append(max(j))



            y[i] = max(global_errors)

        return y
