import pathlib
from itertools import combinations_with_replacement
from typing import Dict, Iterable, List

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
                             threads=threads))
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
        df_performance[f"Performance {ticker}"] = (
            df["Close"][ticker] > df["Open"][ticker])
    return df_performance.convert_dtypes(pd.BooleanDtype)


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


def compare_combinations(combinations: Iterable,
                         df: pd.DataFrame):
    # comparison_matrix =
    # TODO: Convert dtypes for addition and multiplication
    for comb in combinations:
        res = df[comb[0]] * df[comb[1]] * (df[comb[0]] + df[comb[1]])
    pass
