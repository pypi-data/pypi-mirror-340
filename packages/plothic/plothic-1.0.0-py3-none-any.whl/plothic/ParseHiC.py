#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author: Zijie Jiang
@Contact: jzjlab@163.com
@File: ParseHiC.py
@Time: 2024/11/12 19:33
@Function: Parse Hi-C data
"""

import hicstraw
import numpy as np


def parse_hic(hic, resolution, matrix_end=None, data_type="observed", normalization="NONE"):
    hic_obj = hicstraw.HiCFile(hic)

    chr_info = {chrom.name: chrom.length for chrom in hic_obj.getChromosomes()}
    hic_max_len = chr_info["assembly"]
    matrix_end = hic_max_len if matrix_end is None else matrix_end

    res_max_len = resolution * 1400

    matrix_obj = hic_obj.getMatrixZoomData('assembly', 'assembly', data_type, normalization, "BP", resolution)

    if res_max_len > matrix_end:
        contact_matrix = matrix_obj.getRecordsAsMatrix(0, matrix_end, 0, matrix_end)
    else:
        extract_times = int(matrix_end / res_max_len) + 1  # extract times
        iter_len = np.linspace(0, matrix_end, extract_times + 1)  # iteration length
        incr_distance = iter_len[1]  # increment distance
        final_matrix = None

        for i in iter_len[1:]:
            temp_matrix = None
            for j in iter_len[1:]:
                contact_matrix = matrix_obj.getRecordsAsMatrix(int(i - incr_distance), int(i), int(j - incr_distance),
                                                               int(j))
                temp_matrix = contact_matrix if temp_matrix is None else np.hstack((temp_matrix, contact_matrix))

            final_matrix = temp_matrix if final_matrix is None else np.vstack((final_matrix, temp_matrix))

        # Remove all zero rows and columns
        final_matrix = final_matrix[~np.all(final_matrix == 0, axis=1)]
        contact_matrix = final_matrix[:, ~np.all(final_matrix == 0, axis=0)]

    return contact_matrix
