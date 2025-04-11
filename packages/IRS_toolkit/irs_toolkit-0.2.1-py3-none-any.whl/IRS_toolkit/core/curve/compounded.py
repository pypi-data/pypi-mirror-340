import pandas as pd
from datetime import datetime
from typing import Optional
from IRS_toolkit.utils import core


class Compounded:
    """
    A class to handle compounded ESTR (Euro Short-Term Rate) data.

    This class processes lists of dates and ESTR rates, performs linear interpolation,
    and stores the results in a pandas DataFrame.

    Args:
        list_date (list[datetime]): List of dates for the ESTR rates
        list_estr (list[float]): List of ESTR rate values
        as_of_date (Optional[datetime], optional): Reference date for the rates. Defaults to None.
        data_base (int, optional): Base to divide ESTR rates by. Defaults to 1.

    Attributes:
        data_base (int): Base used to scale ESTR rates
        list_date (list[datetime]): Original list of dates
        list_estr (list[float]): Scaled ESTR rates
        as_of_date (datetime): Reference date
        df (pd.DataFrame): DataFrame containing interpolated ESTR data with columns:
            - DATES: Dates for the rates
            - ESTR: Interpolated ESTR values
            - AS_OF_DATE: Reference date
    """

    def __init__(
        self,
        list_date: list[datetime],
        list_estr: list[float],
        as_of_date: Optional[datetime] = None,
        data_base=1,
    ):
        self.data_base = data_base
        new_list_estr = [x / data_base for x in list_estr]
        self.list_date = list_date
        self.list_estr = new_list_estr
        self.as_of_date = as_of_date

        dict_estr = {"DATES": self.list_date, "ESTR": self.list_estr}
        df = pd.DataFrame(dict_estr)
        df["DATES"] = pd.to_datetime(df["DATES"])

        ESTR = core.linear_interpolation(df["DATES"].to_list(), df["ESTR"].to_list())
        ESTR.rename(columns={"VALUES": "ESTR"}, inplace=True)
        ESTR["AS_OF_DATE"] = self.as_of_date
        ESTR["DATES"] = pd.to_datetime(ESTR["DATES"])
        ESTR["AS_OF_DATE"] = pd.to_datetime(ESTR["AS_OF_DATE"])

        self.df = ESTR
