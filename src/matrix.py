from math import lcm, gcd


class Matrix:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.states = {
            1: {
                "message": "Original matrix",
                "state": matrix.copy(),
                "ID": "",
                "params": [],
            }
        }
        self.amount_of_states = 1
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])
        self.func_ids = {
            "Elim": self.eliminate_null_rows,
            "Mult": self.multiply_row,
            "Div": self.divide_row,
            "Substract": self.substract_rows,
            "Sum": self.sum_rows,
            "Exchange": self.exchange_rows,
            "No_fr": self.transform_floats_to_integers,
        }

    def __str__(self) -> str:
        begin_delimiter = "--------------------\n"
        message = self.print_matrix(self.amount_of_states)
        end_delimiter = "\n--------------------"

        return begin_delimiter + message + end_delimiter

    def get_func_ids_and_params(self):
        ids_params = {}
        for key in self.states.keys():
            ids_params[key] = (self.states[key]["ID"], self.states[key]["params"])
        return ids_params

    def recover_states(self, ids_params):
        for id, param in ids_params.values():
            if id != "":
                self.func_ids[id](*param)

    def print_matrix(self, state: int):
        # ------------ Get the greatest length of a number in every column ------------ #
        matrix: list[list[int]] = self.states[state]["state"]
        columns_widths = {
            column_ind: [] for column_ind in range(self.columns)
        }  # Keep all column lengths
        for row in matrix:
            for column_ind, num in enumerate(row):
                columns_widths[column_ind].append(len(str(num)))

        max_widths = [max(col_width) for col_width in columns_widths.values()]

        # ------------ Create the final print ceil by ceil ------------ #
        final_matrix = []
        for row in matrix:
            # Format each ceil and join them
            formatted_row = " | ".join(
                f"{ceil:^{max_widths[col_ind]}}" for col_ind, ceil in enumerate(row)
            )
            final_matrix.append(f"[ {formatted_row} ]")
        return "\n".join(
            final_matrix
        )  # Return all the rows formatted after adding line breaks

    def show_all_states(self) -> None:
        for state in self.states.keys():
            print(state, "->", self.states[state]["message"])
            print(self.print_matrix(state), "\n")

    def add_matrix_state(self, message: str, id: str, params: list) -> None:
        self.amount_of_states += 1
        self.states.update(
            {
                self.amount_of_states: {
                    "message": message,
                    "state": self.matrix.copy(),
                    "ID": id,
                    "params": params,
                }
            }
        )

    def eliminate_null_rows(self) -> None:
        # Null row == [0, 0, 0, ...]
        # They do not count for anything
        indexes_of_null_rows = []
        null_row = [0] * self.columns

        for index, row in enumerate(self.matrix):
            if row == null_row:
                indexes_of_null_rows.append(index)

        if len(indexes_of_null_rows) != 0:
            # Delete each null row, starting from the end of the matrix
            # Because of avoid reodering of the rows in the right side of the null one
            for index in indexes_of_null_rows[::-1]:
                del self.matrix[index]

            # Keep the new state of the matrix with the specific change made
            personalized_message = "Eliminate null rows"
            self.add_matrix_state(personalized_message, "Elim", [])

            self.rows = len(
                self.matrix
            )  # As some rows may be eliminated, we have to update the length of the matrix

    def is_it_row_reduced_by_gauss(self) -> bool:
        """
        A row_reduced matrix have the following form:
        [x, y, z, t]
        [0, y, z, t]
        [0, 0, z, t]
        [0, 0, 0, t]
        """
        for column in range(self.columns):
            for row in range(column + 1, self.rows):
                if self.matrix[row][column] != 0:
                    return False
        return True

    def is_it_row_reduced_by_gauss_jordan(self) -> bool:
        """
        A row_reduced matrix have the following form:
        [1, 0, 0, 0, x]
        [0, 1, 0, 0, y]
        [0, 0, 1, 0, z]
        [0, 0, 0, 1, t]
        """
        min_size = min(self.columns, self.rows)
        for dim_r in range(min_size):
            for dim_c in range(min_size):
                if dim_r == dim_c:
                    if self.matrix[dim_r][dim_c] != 1:
                        return False
                else:
                    if self.matrix[dim_r][dim_c] != 0:
                        return False
        return True

    def get_principal_diagonal(self) -> list[int]:
        diagonal = []
        size = min(self.rows, self.columns)
        for dimension in range(size):
            diagonal.append(self.matrix[dimension][dimension])
        return diagonal

    def select_rows_to_exchange(self) -> None:
        diagonal = self.get_principal_diagonal()
        for diag_index, num in enumerate(diagonal):
            if num == 0:
                for row_ind, row in enumerate(self.matrix[diag_index + 1 :]):
                    if row[diag_index] != 0:
                        self.exchange_rows(diag_index, diag_index + row_ind + 1)
                        return

    def multiply_row(self, row_index: int, scalar: int) -> None:
        new_nums = []
        for num in self.matrix[row_index]:

            new_num = num * scalar  # Multiplications always returns a float number

            if new_num == int(new_num):  # Check if the number is like x.0
                new_nums.append(int(new_num))  # Num as int is more readable
            else:
                new_nums.append(new_num)

        self.matrix[row_index] = new_nums

        # Keep the new state of the matrix with the specific change made
        personalized_message = f"Multiply row {row_index + 1} by {scalar}"
        self.add_matrix_state(personalized_message, "Mult", [row_index, scalar])

    def divide_row(self, row_index: int, scalar: int) -> None:
        new_nums = []
        for num in self.matrix[row_index]:

            new_num = num / scalar  # Divisions always returns a float number

            if new_num == int(new_num):  # Check if the number is like x.0
                new_nums.append(int(new_num))  # Num as int is more readable
            else:
                new_nums.append(new_num)

        self.matrix[row_index] = new_nums

        # Keep the new state of the matrix with the specific change made
        personalized_message = f"Divide row {row_index + 1} by {scalar}"
        self.add_matrix_state(personalized_message, "Div", [row_index, scalar])

    def row_times(self, row: list[int], scalar: int) -> list[int]:
        return [num * scalar for num in row]

    def exchange_rows(self, index_a: int, index_b: int) -> None:
        self.matrix[index_a], self.matrix[index_b] = (
            self.matrix[index_b],
            self.matrix[index_a],
        )

        # Keep the new state of the matrix with the specific change made
        personalized_message = f"Exchange rows {index_a + 1} and {index_b + 1}"
        self.add_matrix_state(personalized_message, "Exchange", [index_a, index_b])

    def sum_rows(self, ind1: int, ind2: int, scalar1: int, scalar2: int) -> None:

        changing_row = self.matrix[ind1]
        pivot = self.matrix[ind2]

        changing_row_mult = self.row_times(changing_row, scalar1)
        pivot_mult = self.row_times(pivot, scalar2)

        self.matrix[ind1] = [
            num1 + num2 for num1, num2 in zip(changing_row_mult, pivot_mult)
        ]

        # Keep the new state of the matrix with the specific change made
        message1 = (
            f"row {ind1 + 1}" if scalar1 == 1 else f"{scalar1} times row {ind1 + 1}"
        )
        message2 = (
            f"row {ind2 + 1}" if scalar2 == 1 else f"{scalar2} times row {ind2 + 1}"
        )
        personalized_message = f"Sum {message1} with {message2}"
        self.add_matrix_state(
            personalized_message, "Sum", [ind1, ind2, scalar1, scalar2]
        )

    def substract_rows(self, ind1: int, ind2: int, scalar1: int, scalar2: int) -> None:

        changing_row = self.matrix[ind1]
        pivot = self.matrix[ind2]

        changing_row_mult = self.row_times(changing_row, scalar1)
        pivot_mult = self.row_times(pivot, scalar2)

        self.matrix[ind1] = [
            num1 - num2 for num1, num2 in zip(changing_row_mult, pivot_mult)
        ]

        # Keep the new state of the matrix with the specific change made
        message1 = (
            f"row {ind1 + 1}" if scalar1 == 1 else f"{scalar1} times row {ind1 + 1}"
        )
        message2 = (
            f"row {ind2 + 1}" if scalar2 == 1 else f"{scalar2} times row {ind2 + 1}"
        )
        personalized_message = f"Substract {message1} with {message2}"
        self.add_matrix_state(
            personalized_message,
            "Substract",
            [ind1, ind2, scalar1, scalar2],
        )

    def simplify_rows(self) -> None:
        gcds = {}
        for index, row in enumerate(self.matrix):
            max_divisor = gcd(*row)
            if max_divisor != 1:
                gcds.update({index: max_divisor})
        for index, divisor in gcds.items():
            self.divide_row(index, divisor)

    def float_to_int(self, row_ind: int) -> None:
        for column in range(self.columns):
            real_num = self.matrix[row_ind][column]
            if type(real_num) == float:
                int_num = int(real_num)
                if real_num == int_num:
                    self.matrix[row_ind][column] = int_num

    def transform_floats_to_integers(self) -> None:
        rows_to_transform = {}
        for index, row in enumerate(self.matrix):
            ex = [True for num in row if num == int(num)]
            if len(ex) == self.columns:
                continue
            rounded_nums = [round(num, 5) for num in row]
            rows_to_transform.update({index: self.row_times(rounded_nums, 100_000)})
        for index in range(self.rows):
            if not rows_to_transform.get(index):
                self.float_to_int(index)
                continue
            self.matrix[index] = [int(num) for num in rows_to_transform[index]]

            # Keep the new state of the matrix with the specific change made
            personalized_message = (
                f"Round nums, and multiply row {index + 1} by 100.000 (default)"
            )
            self.add_matrix_state(personalized_message, "No_fr", [])
        self.simplify_rows()

    def search_floats_in_square(self) -> bool:
        dim = min(self.columns, self.rows)
        for row in range(dim):
            for column in range(dim):
                if type(self.matrix[row][column]) == float:
                    return True
        return False

    def get_column_to_row_reduce(
        self, row_reduce_below: bool = True
    ) -> tuple[int, list[int]]:
        res = []
        dim = min(self.columns, self.rows)  # Only numbers in the square matrix
        if row_reduce_below:  # Reduce below principal diagonal (Gauss Method)
            for col_ind in range(dim):

                # In Gauss Method we ignore all numbers above principal diagonal
                nums_in_column = [row[col_ind] for row in self.matrix[col_ind + 1 :]]

                for row_index, num in enumerate(nums_in_column, start=col_ind + 1):
                    if num != 0:
                        res.append(row_index)
                if len(res) != 0:  # If one column needs to be reduced, finish the func
                    return (col_ind, res)
        else:  # Reduce above principal diagonal (Gauss-Jordan Method)
            for col_ind in range(dim):

                # In Gauss-Jordan we ignore all numbers below principal diagonal
                upper_limit = dim - col_ind - 1
                nums_in_column = [row[upper_limit] for row in self.matrix[:upper_limit]]

                for row_index, num in enumerate(nums_in_column):
                    if num != 0:
                        res.append(row_index)
                if len(res) != 0:  # If one column needs to be reduced, finish the func
                    return (upper_limit, res)
        return (-1, res)

    def operate_to_make_a_0(self, column: int, rows: list[int]):
        sum_num = self.matrix[column][column]  # Pivot number to make 0s
        for row in rows:  # Rows we have to reduce
            changing_num = self.matrix[row][column]  # This number has to be 0
            least_common_multiple = lcm(int(changing_num), int(sum_num))

            # In summation and substraction of matrixes' rows, they can be multiplied by scalars
            # Scalars will be always positive, and in case is like x.0, parse it to integer
            scalar1 = abs(least_common_multiple / changing_num)
            if scalar1 == int(scalar1):
                scalar1 = int(scalar1)
            scalar2 = abs(least_common_multiple / sum_num)
            if scalar2 == int(scalar2):
                scalar2 = int(scalar2)

            if (changing_num > 0 and sum_num > 0) or (changing_num < 0 and sum_num < 0):
                self.substract_rows(row, column, scalar1, scalar2)  # Both + or -
            else:
                self.sum_rows(row, column, scalar1, scalar2)  # One is + and the other -

    def row_reduce_by_Gauss(self) -> None:

        self.eliminate_null_rows()
        is_row_reduced = self.is_it_row_reduced_by_gauss()
        if is_row_reduced:
            return

        while not is_row_reduced:

            if self.search_floats_in_square():  # Work with floats is uncomfortable
                self.transform_floats_to_integers()

            diagonal = self.get_principal_diagonal()
            if 0 in diagonal:  # All numbers in diagonal have to be different from 0
                self.select_rows_to_exchange()

            column, rows = self.get_column_to_row_reduce()
            self.operate_to_make_a_0(column, rows)

            self.eliminate_null_rows()
            is_row_reduced = self.is_it_row_reduced_by_gauss()

        self.transform_floats_to_integers()

    def row_reduce_by_Gauss_Jordan(self) -> None:

        is_row_reduced = self.is_it_row_reduced_by_gauss_jordan()
        if is_row_reduced:
            return

        self.row_reduce_by_Gauss()  # Firsts steps of Gauss-Jordan is equal to Gauss Method
        dim = min(self.columns, self.rows) - 1
        # Verify if the last number in the principal diagonal is 1 to make easier calculations
        if self.matrix[dim][dim] != 1:
            self.divide_row(dim, self.matrix[dim][dim])

        while not is_row_reduced:
            column, rows = self.get_column_to_row_reduce(False)
            if column == -1:  # Matrix is already reduced
                diag = self.get_principal_diagonal()
                for ind, num in enumerate(diag):
                    if num != 1:  # Transform to 1s the principal diagonal
                        self.divide_row(ind, num)
                break
            self.operate_to_make_a_0(column, rows)

            is_row_reduced = self.is_it_row_reduced_by_gauss_jordan()
