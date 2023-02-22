
from typing import Dict, Iterable

import numpy as np
import pandas as pd

from utils.functions import (calc_corr_matrix, compare_combinations,
                             download_tickers_data, evaluate_performance,
                             gen_tickeridx_ticks, read_tickers,
                             tickers_combinations)
from utils.plotting import corr_matrix_plotting


# main program with all functions
# run after the other
def main() -> int:
    # 1) READ TICKERS FROM LOCAL CSV FILE
    ticks: str = read_tickers()
    num_tickers: int = len(ticks.split(" "))
    # 2) DOWNLOAD DATA FROM YAHOO
    df_finance_data = download_tickers_data(
        tickers=ticks,
        start="2023-01-01",
        end="2023-02-11",
        threads=True)
    # 3) WRITE PERFORMANCE IN ADDTIONAL DF
    df_performance: pd.DataFrame = evaluate_performance(
        tickers=ticks,
        df=df_finance_data)
    # 4) GENERATE COMBINATIONS
    combs: Iterable = tickers_combinations(tickers=ticks)
    # 5) GENERATE NECESSARY DICTIONARIES
    ticker_dict, inv_ticker_dict = gen_tickeridx_ticks(
        tickers=ticks)
    # 6) DEFINE COMBINATION MATRIX
    combined_matrix: np.array = compare_combinations(
        combinations=combs,
        df=df_performance,
        ticker_dict=ticker_dict,
        length=num_tickers)
    corr_matrix: np.array = calc_corr_matrix(combined_matrix=combined_matrix)
    corr_matrix_plotting(correlation_matrix=corr_matrix,
                         column_names=ticks.split(" "),
                         cut=False)
    # define cut
    cut_variable: float = 0.4
    corr_matrix = corr_matrix < cut_variable
    corr_matrix_plotting(correlation_matrix=corr_matrix,
                         column_names=ticks.split(" "),
                         cut=True)
    return 0


if __name__ == "__main__":
    main()
