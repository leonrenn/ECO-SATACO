"""Plotting functions for the main program provide a very
handy way to plot different matrices.
"""

import pathlib
from typing import List

import matplotlib.pyplot as plt
import numpy as np


def corr_matrix_plotting(correlation_matrix: np.array,
                         column_names: List[str],
                         cut: bool = False,
                         show: bool = False) -> None:
    """Generates a figure of the correlation matrix showing
    which stocks regions correlate.
    Args:
        correlation_matrix (np.array): Pearson Correlation Coeff.
        column_names (List[str]): Names of the stocks.
        show (bool, optional): Shows figure while
        running the analysis run. Defaults to False.
    """
    # from binary format into float format such that
    # diagonal elements can be painted grey (self correlating SRs),
    # white for SR correlations below threshold and black for above
    correlation_matrix = np.array(correlation_matrix, dtype=np.float32)
    # indices of lower triangle and set them to 1
    indices_lower = np.tril_indices_from(correlation_matrix)
    correlation_matrix[indices_lower] = 1
    if cut is True:
        # set diagonal to 0.5 for better visualization
        np.fill_diagonal(correlation_matrix, 0.5)
    # transpose matrix as in TACO paper
    correlation_matrix = correlation_matrix.T

    font = {'size': 6}

    # using rc function
    plt.rc('font', **font)
    fig, ax = plt.subplots(figsize=(14, 14))

    pcol = ax.pcolor(correlation_matrix, cmap=plt.cm.Greys)

    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(len(column_names)) + 0.5,
                  minor=False)
    ax.set_yticks(np.arange(len(column_names)) + 0.5,
                  minor=False)
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.xaxis.set_ticks_position('both')
    ax.set_xticklabels(column_names,
                       minor=False,
                       rotation=45)
    ax.set_yticklabels(column_names,
                       minor=False)
    fig.colorbar(pcol, ax=ax)

    if cut is False:
        fig.savefig(str(pathlib.Path(__file__).parent.resolve()) +
                    "/../../results/correlations.png")
    else:
        fig.savefig(str(pathlib.Path(__file__).parent.resolve()) +
                    "/../../results/correlations_threshold.png")

    if show is True:
        plt.show()
    return
