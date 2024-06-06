import numpy as np


def uncompress_matrix(cm):
    CMAT0_MASK = 0x3ff00000
    CMAT1_MASK = 0x000ffc00
    CMAT2_MASK = 0x000003ff
    result_matrix = np.zeros((3, 3), dtype=np.int32)
    v = ((cm[0] & CMAT0_MASK) << 2) >> 22
    result_matrix[0, 0] = v << 6
    v = ((cm[0] & CMAT1_MASK) << 12) >> 22
    result_matrix[0, 1] = v << 6
    v = ((cm[0] & CMAT2_MASK) << 22) >> 22
    result_matrix[0, 2] = v << 6
    v = ((cm[1] & CMAT0_MASK) << 2) >> 22
    result_matrix[1, 0] = v << 6
    v = ((cm[1] & CMAT1_MASK) << 12) >> 22
    result_matrix[1, 1] = v << 6
    v = ((cm[1] & CMAT2_MASK) << 22) >> 22
    result_matrix[1, 2] = v << 6
    v = ((cm[2] & CMAT0_MASK) << 2) >> 22
    result_matrix[2, 0] = v << 6
    v = ((cm[2] & CMAT1_MASK) << 12) >> 22
    result_matrix[2, 1] = v << 6
    v = ((cm[2] & CMAT2_MASK) << 22) >> 22
    result_matrix[2, 2] = v << 6
    # print(result_matrix)
    result_matrix = (result_matrix * 1/32704)

    # result_matrix = np.char.split(result_matrix, " ")
    result_matrix = result_matrix.tolist()

    return result_matrix


def darci_first_frame():
    rot_matrices = [[0.94716243, 0.2739726,  -0.16634051]
 [-0.27592955,  0.962818,    0.01956947]
 [ 0.16438356,  0.02544031,  0.98630137]]


if __name__ == '__main__':
    cm = np.array([521044052, 86494284, 973016563], dtype=np.int32)

    uncompress_matrix(cm)
