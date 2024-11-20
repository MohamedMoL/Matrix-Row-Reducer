from src.matrix import Matrix
from src.helpers.measure_time import measure_time
from src.helpers.generate_identity_matrix import identity_matrix_by_size


if __name__ == "__main__":
    # ------------------ TESTS ------------------ #
    # Test 1
    ex = [[0, 4, 5], [0, 0, 0], [0, 2, 1], [3, 0, 3], [0, 0, 0]]
    matrix_a = Matrix(ex)
    matrix_a.row_reduce_by_Gauss_Jordan()
    # matrix_a.show_all_states()

    # Test 2
    ex = [[2, 4, 5, 4], [4, 3, 0, 3], [2, 1, 1, 5], [2, 3, 2, 0]]
    matrix_a = Matrix(ex)
    # matrix_a.row_reduce_by_Gauss_Jordan()
    # matrix_a.show_all_states()
    """identity = identity_matrix_by_size(4)
    identity = Matrix(identity)
    identity.recover_states(matrix_a.get_func_ids_and_params())"""

    # Test 3
    ex = [
        [2, 4, 5, 4],
        [0, 0, 0, 0],
        [4, 3, 0, 3],
        [2, 1, 1, 5],
        [0, 0, 0, 0],
        [2, 3, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    matrix_a = Matrix(ex)
    # measure_time(matrix_a, 3)
    # matrix_a.show_all_states()

    # Test 4
    ex = [[0, 2, 3, 1], [3, 2, 4, 1], [2, 3.141536, 1, 1]]
    matrix_a = Matrix(ex)
    matrix_a.row_reduce_by_Gauss_Jordan()
    matrix_a.show_all_states()
