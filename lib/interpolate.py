from fractions import Fraction


class Interpolator:
    MODES = ["newton", "divide", ]

    def __init__(self, algorithm=MODES[0]):
        if algorithm not in Interpolator.MODES:
            raise ValueError(f"algorithm argument must be one of {MODES}")

        self.x_data = []
        self.y_data = []
        self.c_data = []
        self.min = 0
        self.max = 0

        if algorithm == Interpolator.MODES[1]:
            self.in_c_data = []
            self.c_data_adder_handler = self.__divide_c_data_adder_handler
        elif algorithm == Interpolator.MODES[0]:
            self.c_data_adder_handler = self.__newton_c_data_adder_handler

    def __compute(self, x):
        res = self.c_data[0] if len(self.c_data) > 0 else 0

        total_sub_x = 1

        for i in range(1, len(self.c_data)):
            total_sub_x *= (x - self.x_data[i - 1])

            res += self.c_data[i] * total_sub_x

        if len(self.x_data) > 0:
            total_sub_x *= (x - self.x_data[-1])

        return res, total_sub_x

    def __divide_c_data_adder_handler(self, x, y):
        if self.size() == 0:
            self.c_data.append(y)
            self.in_c_data.append(y)
        else:
            current_bottom = y
            new_in_c = [current_bottom]

            for old_x, old_in_c in zip(self.x_data[::-1], self.in_c_data):
                current_bottom = (current_bottom - old_in_c) / (x - old_x)
                new_in_c.append(current_bottom)

            # add the last item to the real c data.
            self.c_data.append(current_bottom)

            if 'in_c_data' in dir(self):
                self.in_c_data = new_in_c
            else:
                raise ValueError("divide algorithm handler is used, but the class structure is wrong")

    def __newton_c_data_adder_handler(self, x, y):
        # TODO: x_differences is computed internally in compute(), change that for more efficiency
        old_computed, x_differences = self.__compute(x)
        self.c_data.append((y - old_computed) / x_differences)

    def add(self, x, y):
        x, y = map(Fraction, (x, y))
        try:
            self.c_data_adder_handler(x, y)
        except:
            raise ArithmeticError(f"this value of x ({x}) already exists")
        self.x_data.append(x)
        self.y_data.append(y)

        if x > self.max:
            self.max = x
        if x < self.min:
            self.min = x

    def size(self):
        return len(self.x_data)

    def compute(self, x):
        return self.__compute(x)[0]

    def __str__(self):
        res = []

        c_data_len = len(self.c_data)

        for i in range(c_data_len):
            current_c = self.c_data[i]

            if current_c == 0:
                continue

            sub_res = str(current_c)

            for j in range(i):
                sub_res += f'(x - {self.x_data[j]})'

            res.append(sub_res)

        final = ' + '.join(res)

        if not final and c_data_len > 0:
            final = '0'

        return final.replace(' + -', ' - ').replace(' - -', ' + ')
