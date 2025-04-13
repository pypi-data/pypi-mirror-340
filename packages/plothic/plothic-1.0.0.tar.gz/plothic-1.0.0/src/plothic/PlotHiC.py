#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author: Zijie Jiang
@Contact: jzjlab@163.com
@File: PlotHiC.py
@Time: 2024/9/29 17:08
@Function: Plot Whole genome Hi-C contact matrix heatmap
"""
import os

import hicstraw
import numpy as np

from .ParseHiC import parse_hic
from .PlotMTX import plot_matrix
from .logger import logger


def plot_hic(hic, chr_txt, output='./', resolution=None, data_type="observed",
             normalization="NONE", genome_name="", fig_size=6, dpi=300,
             bar_min=0,
             bar_max=None, cmap="YlOrRd", order=False, log=False, rotation=45, grid=True, out_format="pdf",
             xaxis=False):
    logger.info(f"Start Plot Hi-C data (hic format): {hic}")

    # get hic object
    hic_obj = hicstraw.HiCFile(hic)

    # get resolutions
    resolutions = hic_obj.getResolutions()
    logger.info(f"This Hi-C data has resolutions: {resolutions}")

    # choose resolution
    if resolution is None:
        resolution = resolutions[-4]
        logger.info(f"Resolution not set, use the default max resolution: {resolution}")
    elif resolution not in resolutions:
        logger.error(f"Resolution {resolution} not in {resolutions}")
        resolution = resolutions[-4]
    logger.info(f"Use the resolution: {resolution}")
    if resolution <= 1000:
        logger.warning("The resolution is too small, the memory usage will be large")
    logger.info(f"Use the {data_type} data type and {normalization} normalization method")

    chr_info = {}  # chrom information
    chr_start = 0  # chrom start loci
    last_chr_len = 0  # last chrom len

    # get chromosome information
    with (open(chr_txt, 'r') as f):
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip().split()
            chr_info[line[2]] = {
                "length": int(line[1]) - chr_start,  # chromosome length in hic file
                "name": line[0],
                "hic_loci": int(line[1])  # chromosome loci in hic file
            }
            chr_start = int(line[1])

            # get the last chromosome length
            if int(line[1]) > last_chr_len:
                last_chr_len = int(line[1])

    logger.info(f"Chromosome information: {chr_info}")

    matrix = parse_hic(hic, resolution, matrix_end=last_chr_len, data_type=data_type,
                       normalization=normalization).astype(np.float32)
    matrix_len = len(matrix)

    chr_label_dict = {}  # chr name: loci index in matrix
    for i in chr_info:
        chr_label_dict[chr_info[i]["name"]] = chr_info[i]["hic_loci"] * matrix_len // last_chr_len

    if order:
        logger.info("Order the heatmap by specific order")
        chr_dict_length = len(chr_info)

        pre_index = 0
        # cal the new order
        for i in chr_info:
            chr_info[i]["pre_index"] = pre_index
            chr_info[i]["index"] = (chr_info[i]["hic_loci"] * matrix_len) // last_chr_len
            pre_index = chr_info[i]["index"]

        new_order = []

        pre_label_loci = 0
        for i in range(1, chr_dict_length + 1):
            temp_order = np.arange(chr_info[str(i)]["pre_index"], chr_info[str(i)]["index"])
            new_order.extend(temp_order)
            chr_info[str(i)]["label_loci"] = len(temp_order) + pre_label_loci
            pre_label_loci = chr_info[str(i)]["label_loci"]

        # get the new order matrix
        matrix = matrix[new_order, :][:, new_order]

        chr_label_dict = {}
        for i in chr_info:
            chr_label_dict[chr_info[i]["name"]] = chr_info[i]["label_loci"]
    if os.path.isdir(output):  # output is a directory
        output = os.path.join(output, f"GenomeContact.{out_format}")

    if xaxis:
        logger.info("Show genome size at x-axis")
        x_label_dict = {}
        temp_chr_len = 0
        for i in chr_label_dict:
            x_name = str(round(chr_label_dict[i] * resolution / 1000000, 1)) + " Mb"
            logger.info(f"{i} length: {round(chr_label_dict[i] * resolution / 1000000 - temp_chr_len, 1) } Mb")
            temp_chr_len = round(chr_label_dict[i] * resolution / 1000000, 1)
            x_label_dict[x_name] = chr_label_dict[i]
    else:
        x_label_dict = None
    plot_matrix(matrix, chr_info=chr_label_dict, outfile=output, genome_name=genome_name, fig_size=(fig_size, fig_size),
                dpi=dpi,
                bar_min=bar_min,
                bar_max=bar_max, cmap=cmap, log=log, rotation=rotation, grid=grid, x_info=x_label_dict)

    logger.info(f"Save the plot to {output}")
    logger.info("Finished Plot Hi-C data")


def plot_hic_split(hic, split_txt, output='./', resolution=None, data_type="observed",
                   normalization="NONE", genome_name="", fig_size=6, dpi=300,
                   bar_min=0,
                   bar_max=None, cmap="YlOrRd", log=False, rotation=45, out_format="pdf", xaxis=False):
    logger.info(f"Start Plot Hi-C data (hic format) with split chromosome: {hic}")

    # get hic object
    hic_obj = hicstraw.HiCFile(hic)

    # get resolutions
    resolutions = hic_obj.getResolutions()
    logger.info(f"This Hi-C data has resolutions: {resolutions}")

    # choose resolution
    if resolution is None:
        resolution = resolutions[-4]
        logger.info(f"Resolution not set, use the default max resolution: {resolution}")
    elif resolution not in resolutions:
        logger.error(f"Resolution {resolution} not in {resolutions}")
        resolution = resolutions[-4]
    logger.info(f"Use the resolution: {resolution}")
    logger.info(f"Use the {data_type} data type and {normalization} normalization method")

    chr_info = {}  # chromosome information
    with (open(split_txt, 'r') as f):
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip().split()
            chr_info[line[0]] = {
                "start": int(line[1]),
                "end": int(line[2])
            }

    logger.info(f"Chromosome information: {chr_info}")
    res_max_len = resolution * 1400
    matrix_obj = hic_obj.getMatrixZoomData('assembly', 'assembly', data_type, normalization, "BP", resolution)

    for k in chr_info:
        chr_name = k
        loci_len = chr_info[k]["end"] - chr_info[k]["start"]

        if res_max_len > loci_len:
            contact_matrix = matrix_obj.getRecordsAsMatrix(chr_info[k]["start"], chr_info[k]["end"],
                                                           chr_info[k]["start"], chr_info[k]["end"])
        else:
            extract_times = int(loci_len / res_max_len) + 1  # extract times
            iter_len = np.linspace(chr_info[k]["start"], loci_len, extract_times + 1)  # iteration length
            incr_distance = iter_len[1]  # increment distance
            final_matrix = None

            for i in iter_len[1:]:
                temp_matrix = None
                for j in iter_len[1:]:
                    contact_matrix = matrix_obj.getRecordsAsMatrix(int(i - incr_distance), int(i),
                                                                   int(j - incr_distance),
                                                                   int(j))
                    temp_matrix = contact_matrix if temp_matrix is None else np.hstack((temp_matrix, contact_matrix))

                final_matrix = temp_matrix if final_matrix is None else np.vstack((final_matrix, temp_matrix))

            # Remove all zero rows and columns
            non_zero_rows = final_matrix[~np.all(final_matrix == 0, axis=1)]
            contact_matrix = non_zero_rows[:, ~np.all(non_zero_rows == 0, axis=0)]

        if os.path.isdir(output):  # output is a directory
            chr_output = os.path.join(output, f"{chr_name}.{out_format}")
        else:
            chr_output = os.path.join("./", f"{chr_name}.{out_format}")

        if xaxis:
            logger.info("Show genome size at x-axis")
            x_label_dict = {0: 0}
            x_name = str(round(loci_len / 1000000, 1)) + " Mb"
            logger.info(f"Chromosome length: {x_name}")
            x_label_dict[x_name] = contact_matrix.shape[0]
        else:
            x_label_dict = None

        plot_matrix(contact_matrix, chr_info=x_label_dict, outfile=chr_output, genome_name=genome_name + chr_name,
                    fig_size=(fig_size, fig_size),
                    dpi=dpi,
                    bar_min=bar_min,
                    bar_max=bar_max, cmap=cmap, log=log, rotation=rotation, grid=False)

        logger.info(f"Save the plot to {chr_output}")

    logger.info("Finished Plot Hi-C data with split chromosome")
