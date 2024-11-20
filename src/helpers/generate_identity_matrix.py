def identity_matrix_by_size(size: int) -> list[list[int]]:
    # An identity matrix is a matrix with only 1s in the principal diagonal
    """[
        [1 0 0]
        [0 1 0]
        [0 0 1]
    ]"""
    identity = [[0] * size for _ in range(size)]  # Create a square matrix with only 0s
    for dim in range(size):
        identity[dim][
            dim
        ] = 1  # Change only the numbers in the principal diagonal to 1s
    return identity
