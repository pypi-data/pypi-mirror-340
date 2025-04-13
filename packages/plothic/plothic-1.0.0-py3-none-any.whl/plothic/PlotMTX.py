#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author: Zijie Jiang
@Contact: jzjlab@163.com
@File: PlotMTX.py
@Time: 2024/11/12 15:47
@Function: Plot Whole genome Hi-C contact matrix heatmap
"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import log2

from .logger import logger


def plot_matrix(matrix, chr_info=None, genome_name="Genome", outfile='GenomeContact.pdf', fig_size=(6, 6), dpi=300,
                bar_min=0,
                bar_max=None,
                cmap="YlOrRd",
                axes_len=4,
                axes_wd=1,
                axes_pad=6, grid=True,
                grid_style='dashed', grid_color='black', grid_width=1, grip_alpha=0.8, bar_size="3%", bar_pad=0.1,
                font_size=10,
                log=False, rotation=45, x_info=None):
    fig, ax = plt.subplots(1, 1, figsize=fig_size, dpi=dpi)

    if chr_info is None:
        labels = []
        pos = []
    else:
        labels = list(chr_info.keys())  # chrom names
        pos = list(chr_info.values())  # chrom loci

    ax.set_xticks(pos)
    ax.set_yticks(pos)

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    if x_info is not None:
        x_labels = list(x_info.keys())  # chrom names
        x_pos = list(x_info.values())  # chrom loci

        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels)

    # set genome title
    if genome_name == "":
        logger.warning("Genome name is not set")
    else:
        logger.info(f"Genome name: {genome_name}")
    ax.set_title(genome_name, fontsize=20, pad=8, fontstyle='italic')

    if grid:
        logger.info("Show grid in the heatmap")
        ax.grid(color=grid_color, linestyle=grid_style, linewidth=grid_width, alpha=grip_alpha)

    plt.setp(ax.get_xticklabels(), rotation=rotation, ha="right", rotation_mode="anchor", fontsize=font_size)
    plt.setp(ax.get_yticklabels(), rotation=rotation, ha="right", rotation_mode="anchor", fontsize=font_size)

    ax.tick_params(direction='out', length=axes_len, width=axes_wd, pad=axes_pad)

    color_bar = make_axes_locatable(ax)
    cax = color_bar.append_axes("right", size=bar_size, pad=bar_pad)

    matrix_len = len(matrix)  # matrix length
    lim_extents = matrix_len + 0.5
    ax.set_ylim(0.5, lim_extents)
    ax.set_xlim(0.5, lim_extents)

    matrix = matrix + 1e-9  # avoid log2(0) error
    maxcolor = (np.percentile(matrix, 90))
    if bar_max is None:
        bar_max = maxcolor
        logger.info(f"Max color is not set, use the default max color: {bar_max}")
    logger.info(f"Color bar range: {bar_min} - {bar_max}")
    logger.info(f"Use the color map: {cmap}")
    with np.errstate(divide='ignore'):
        img = ax.imshow(log2(matrix) if log else matrix, cmap=plt.get_cmap(cmap), vmin=bar_min, vmax=bar_max,
                        origin="lower",
                        interpolation="nearest",
                        extent=(0.5, lim_extents, 0.5, lim_extents), aspect='auto')

    cb = fig.colorbar(img, ax=ax, cax=cax, orientation="vertical")
    cb.ax.tick_params(labelsize=font_size)

    plt.savefig(outfile)
