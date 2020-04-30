from fractions import Fraction
from typing import Tuple


class Interpolator:
    """Class that creates and handles an interpolation instance

    THe behaviour can change based on the algorithm chosen, which can be found in *MODES*.
    """
    MODES = ["newton", "divide", ]

    def __init__(self, algorithm=MODES[0]):
        """Initialize the interpolator with the algorithm chosen by the user

        :param algorithm: chosen algorithm for this interpolator from the list *Interpolator.MODES*
        :type algorithm: str
        """
        if algorithm not in Interpolator.MODES:
            raise ValueError(f"algorithm argument must be one of {Interpolator.MODES}")

        self.x_data = []
        self.y_data = []
        self.c_data = []

        if algorithm == Interpolator.MODES[1]:
            # this is used for only "divide" method and this is the inner part of the tree
            # or you can think of it as the hidden part that is used to build the c values
            # so it's important and should be present
            self.in_c_data = []
            self.c_data_adder_handler = self.__divide_c_data_adder_handler
        elif algorithm == Interpolator.MODES[0]:
            self.c_data_adder_handler = self.__newton_c_data_adder_handler
        else:
            raise ValueError(f"algorithm must be one of {Interpolator.MODES}")

    def __compute(self, x):
        """private function version of *compute*

        :param x: the value of x to be computed on the interpolation function
        :type x: Fraction
        :return: [computed_value, x_differences]
        :rtype: Tuple[Fraction, Fraction]
        """

        # start by the first value of c_data if it exist
        res = self.c_data[0] if len(self.c_data) > 0 else 0

        # this will store the value of (x - x0)(x - x1)(x - x2)...
        # this is where the optimization is, because using the normal method with 2 loops
        # the value of (x - x0) is computed many times and all the other values which use x
        # this variable will store them for use later.
        total_sub_x = 1

        for i in range(1, len(self.c_data)):
            total_sub_x *= (x - self.x_data[i - 1])

            res += self.c_data[i] * total_sub_x

        # add the last value of x_data because in the original compute, it is not added
        # but we add it here because we need the x_differences with all the points from x_data
        if len(self.x_data) > 0:
            total_sub_x *= (x - self.x_data[-1])

        return res, total_sub_x

    def __divide_c_data_adder_handler(self, x, y):
        """function that handles adding the new value of **c** for the divide algorithm

        :param x: point x
        :type x: Fraction
        :param y: point y
        :type y: Fraction
        :rtype: None
        """
        # if this is the first point, then just add it straight
        if self.size() == 0:
            self.c_data.append(y)
            self.in_c_data.append(y)
        else:
            current_bottom = y
            new_in_c = [current_bottom]

            # the x_data is reversed and used with the c_data
            for old_x, old_in_c in zip(self.x_data[::-1], self.in_c_data):
                # compute the next stage of the new c_data
                current_bottom = (current_bottom - old_in_c) / (x - old_x)
                new_in_c.append(current_bottom)

            # add the last item to the real c data.
            self.c_data.append(current_bottom)

            # if this is the newton's method, 'in_c_data' should not be defined
            if 'in_c_data' in dir(self):
                self.in_c_data = new_in_c
            else:
                raise ValueError("divide algorithm handler is used, but the class structure is wrong")

    def __newton_c_data_adder_handler(self, x, y):
        """function that handles adding the new value of **c** for the newton's algorithm

        this is the function that use x_difference from __compute, so most of the core code to compute the c
        value is there.

        :param x: point x
        :type x: Fraction
        :param y: point y
        :type y: Fraction
        :rtype: None
        """
        # TODO: x_differences is computed internally in compute(), change that for more efficiency
        old_computed, x_differences = self.__compute(x)
        self.c_data.append((y - old_computed) / x_differences)

    def add(self, x, y):
        """Add pair (x, y) to the interpolation memory

        :param x: point x
        :type x: Fraction
        :param y: point y
        :type y: Fraction
        :rtype: None
        """
        # convert the input to Fraction whatever it is.
        x, y = map(Fraction, (x, y))
        try:
            # call the data handler, this should change based on the algorithm
            self.c_data_adder_handler(x, y)
        except ZeroDivisionError:
            # if there is division by zero, then this means there is duplicate in x values.
            raise ArithmeticError(f"this value of x ({x}) already exists")
        # after c value is added, add x and y, adding them after c is important, because calculating c value uses
        # the past x, y values
        self.x_data.append(x)
        self.y_data.append(y)

    def size(self):
        """ Get the size of the interpolation dataset

        :return: size of the dataset stored in the interpolation memory
        :rtype: int
        """
        return len(self.x_data)

    def compute(self, x):
        """Pass value x to the interpolation function and get the result

        :param x: input
        :type x: Fraction
        :return: result of the compute
        :rtype: Fraction
        """
        return self.__compute(x)[0]

    def __str__(self):
        """Build the interpolation representation as a string and return it

        :return: string representation of the interpolation
        :rtype: str
        """
        res = []

        # the size of the interpolation
        c_data_len = len(self.c_data)

        for i in range(c_data_len):
            current_c = self.c_data[i]

            # if the current value is zero, then there is no need to print it as it will cancel out with the zero
            if current_c == 0:
                continue

            sub_res = str(current_c)

            for j in range(i):
                sub_res += f'(x - {self.x_data[j]})'

            res.append(sub_res)

        final = ' + '.join(res)

        # if there is a data, but all of them cancel out, then just return zero
        if not final and c_data_len > 0:
            final = '0'

        # convert +- into - and -- into +, as sometimes the concatenation does this if the numbers are negative.
        return final.replace(' + -', ' - ').replace(' - -', ' + ')
