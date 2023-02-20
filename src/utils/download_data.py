from typing import Dict

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
    return df_download
