import pathlib
from itertools import combinations_with_replacement
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import yfinance as yf

from exceptions.exceptions import InvalidDownload


def download_tickers_data(tickers: str,
                          start: str,
                          end: str,
                          threads: bool = True) -> pd.DataFrame:
    """Download data from yahoo finance for a certain
    time span.

    Args:
        tickers (str): Tickers of the threads.
        start (str): Start as a date format.
        end (str): End as date format
        threads (bool, optional): Using threads. Defaults to True.

    Returns:
        pd.DataFrame: Downloaded data as dataframe.
    """
    try:
        dtype_dict: Dict = {"Date": pd.StringDtype,
                            "Volume": pd.Int32Dtype,
                            "Adj Close": pd.Float32Dtype,
                            "Close": pd.Float32Dtype,
                            "High": pd.Float32Dtype,
                            "Low": pd.Float32Dtype,
                            "Open": pd.Float32Dtype}
        df_download: pd.DataFrame = pd.DataFrame(
            data=yf.download(tickers=tickers,
                             start=start,
                             end=end,
                             threads=threads,
                             progress=False))
        df_download = df_download.convert_dtypes(dtype_dict)
    except Exception:
        print("Region is invalid")
        raise InvalidDownload
    return df_download.dropna()


def evaluate_performance(tickers: str,
                         df: pd.DataFrame) -> pd.DataFrame:
    """Generate dataframe that evaluates the temporal performance of the 
    stock with comparing open to close values.

    Args:
        tickers (str): Tickers of the stocks
        df (pd.DataFrame): Dataframe from tickers with
        open and close values

    Returns:
        pd.DataFrame: Dataframe with boolean performance values.
    """
    df_performance: pd.DataFrame = pd.DataFrame()
    for ticker in tickers.split(" "):
        up_trend = df["Close"][ticker] > df["Open"][ticker]
        down_trend = (df["Close"][ticker] < df["Open"][ticker]) * (-1)
        df_performance[ticker] = up_trend + down_trend
    return df_performance.convert_dtypes(pd.Int8Dtype)


def read_tickers(file_path: str = "tickers.txt") -> str:
    """Read tickers from dedicated tickers file
    where short forms are stored

    Args:
        file_path (str, optional): File path and name to tickers.
        Defaults to "tickers.txt".

    Returns:
        str: Tickers in a single string.
    """
    # define path to file
    tickers_path: str = str(pathlib.Path(
        __file__).parent.resolve()) + f"/{file_path}"
    # read lines of file
    with open(tickers_path, "r") as file:
        tickers: str = " ".join(file.readlines())
    # remove characters from string
    tickers = tickers.replace("\n", "")
    tickers = tickers.replace("\t", "")
    return tickers


def tickers_combinations(tickers: str) -> Iterable:
    """Generating combinations for
    comparison of stocks.

    Args:
        tickers (str): Tickers of the stocks.

    Returns:
        Iterable: Cobinations as iterable.
    """
    tickers_list: List = tickers.split(" ")
    combs = combinations_with_replacement(tickers_list, r=2)
    return combs


def gen_tickeridx_ticks(tickers: str) -> Tuple[Dict]:
    """Generate dictionary with index of ticker and 
    ticker string itself. Additionally also the inverse.

    Args:
        tickers (str): Tickers of the stocks.

    Returns:
        Tuple[Dict]: Dictionaries and inverse.
    """
    ticker_idx: Dict = {}
    idx_ticker: Dict = {}
    for idx, ticker in enumerate(tickers.split(" ")):
        ticker_idx[ticker] = idx
        idx_ticker[idx] = ticker
    return ticker_idx, idx_ticker


def compare_combinations(combinations: Iterable,
                         df: pd.DataFrame,
                         ticker_dict: Dict,
                         length: int) -> np.array:
    """Compare stock performances and generate
    combined matrix

    Args:
        combinations (Iterable): Combinations of stocks. 
        (Always pair of two.)
        df (pd.DataFrame): Dataframe with the performance
        of the stocks.
        ticker_dict (Dict): Dictionary to get indices.
        length (int): For generating correct shape.

    Returns:
        np.array: _description_
    """
    combined_matrix: np.array = np.zeros(
        shape=(length, length), dtype=np.int64)
    for comb in combinations:
        i, j = ticker_dict[comb[0]], ticker_dict[comb[1]]
        comb_0: np.array = np.array(df[comb[0]], dtype=np.int8)
        comb_1: np.array = np.array(df[comb[1]], dtype=np.int8)
        combined = (comb_0 == comb_1)
        res = np.sum(combined)
        combined_matrix[i, j] = res
        if i != j:
            combined_matrix[j, i] = res
    return combined_matrix


def calc_corr_matrix(combined_matrix: np.array) -> np.array:
    """Calulated Pearson correlation matrix.

    Args:
        combined_matrix (np.array): Combined matrix of integers
        of stock performance in comparison with each other.

    Returns:
        np.array: Correlation matrix.
    """
    return np.corrcoef(combined_matrix,
                       dtype=np.float64)
