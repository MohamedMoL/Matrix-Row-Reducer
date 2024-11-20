from time import perf_counter
from src.matrix import Matrix


def measure_time(matrix: Matrix, test_number: int):
    begin = perf_counter()
    matrix.row_reduce_by_Gauss_Jordan()
    end = perf_counter()
    print(
        f"TEST {test_number}",
        matrix,
        f"Time spended (multiplied by 1000): {(end - begin) * 1000}",
        sep="\n",
    )
