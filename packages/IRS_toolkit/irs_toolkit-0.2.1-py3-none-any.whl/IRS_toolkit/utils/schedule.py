from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional, List
from IRS_toolkit.utils.constants import VALID_FILL_TYPE, VALID_CONVENTIONS
from IRS_toolkit.utils import core
import pandas as pd
import math


class Schedule:
    """A class to generate and manage financial schedules with date ranges.

    This class creates schedules for financial instruments by either taking a list of date ranges
    or generating them based on start date, maturity date and periodicity.

    Args:
        list_date (list[list], optional): List of date ranges, where each range is [start_date, end_date]. Defaults to None.
        start_date (datetime, optional): Start date of the schedule. Required if list_date not provided. Defaults to None.
        maturity_date (datetime, optional): Maturity date of the schedule. Required if list_date not provided. Defaults to None.
        periodicity (int, optional): Number of months between payments. Required if list_date not provided. Defaults to None.
        type_fill (VALID_FILL_TYPE, optional): Fill direction - "Forward" or "Back". Defaults to "Forward".
        date_convention (VALID_CONVENTIONS, optional): Day count convention. Defaults to "ACT/360".
        date_format (str, optional): Format for parsing date strings. Defaults to "%Y-%m-%d".

    Attributes:
        df (pd.DataFrame): DataFrame containing the schedule dates and calculations
        list_date (list): List of date ranges
        date_format (str): Date string format
        start_date (datetime): Schedule start date
        maturity_date (datetime): Schedule maturity date
        periodicity (int): Months between payments
        type_fill (str): Fill direction
        date_convention (str): Day count convention
    """

    def __init__(  # noqa: C901, PLR0912
        self,
        list_date: Optional[List[List[datetime]]] = None,
        start_date: Optional[datetime] = None,
        maturity_date: Optional[datetime] = None,
        periodicity: Optional[int] = None,
        type_fill: VALID_FILL_TYPE = "Forward",
        date_convention: VALID_CONVENTIONS = "ACT/360",
        date_format="%Y-%m-%d",
    ):
        if list_date is not None and len(list_date) > 0 and len(list_date[0]) > 1:
            self.list_date = list_date
            if start_date is None:
                start_date = list_date[0][0]
            if maturity_date is None:
                maturity_date = list_date[0][-1]
            self.df = pd.DataFrame()
            for i in list_date.copy():
                self.add_date_range(i)
            self.df.reset_index(drop=True, inplace=True)

        else:
            self.list_date = []

            def convert(strg):
                if type(strg) is str:
                    if strg == "NaT":
                        return "N/A"
                    return datetime.strptime(strg, date_format)
                else:
                    return strg

            delta = relativedelta(convert(maturity_date), convert(start_date))
            months = (delta.years * 12 + delta.months + delta.days / 30) / periodicity
            period = math.ceil(months)

            if type_fill == "Forward":
                start_range = pd.date_range(
                    start=start_date,
                    periods=period,
                    freq=pd.DateOffset(months=periodicity),
                )

                end_range = start_range + pd.DateOffset(months=periodicity)

                self.df = pd.DataFrame(
                    {"start_date": start_range, "end_date": end_range}
                )

                for i in range(1, len(self.df), 1):
                    if self.df["start_date"][i] != self.df["end_date"][i - 1]:
                        self.df["start_date"][i] = self.df["end_date"][i - 1]

            elif type_fill == "Back":
                end_range = pd.date_range(
                    end=maturity_date,
                    periods=period,
                    freq=pd.DateOffset(months=periodicity),
                )

                start_range = end_range - pd.DateOffset(month=periodicity)

                self.df = pd.DataFrame(
                    {"start_date": start_range, "end_date": end_range}
                )

                for i in range(1, len(self.df), 1):
                    if self.df["start_date"][i] != self.df["end_date"][i - 1]:
                        self.df["start_date"][i] = self.df["end_date"][i - 1]
            else:
                raise ValueError("Error: Not an available option.")

            for _index, row in self.df.iterrows():
                self.list_date.append([row["start_date"], row["end_date"]])

            self.df["start_date"].iloc[0] = pd.Timestamp(start_date)
            self.df["end_date"].iloc[-1] = pd.Timestamp(maturity_date)

        self.df["Period"] = (self.df.end_date - self.df.start_date).apply(
            lambda x: x.days
        )

        self.df["day_count"] = self.df.apply(
            lambda x: core.day_count(x["start_date"], x["end_date"], date_convention),
            axis=1,
        )

        self.date_format = date_format
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.periodicity = periodicity
        self.type_fill = type_fill
        self.date_convention = date_convention

    def add_date_range(self, date_range: list[datetime]):
        """Add a new date range to the schedule.

        This method appends a new date range (start date and end date) to both the list_date
        attribute and the DataFrame representation of the schedule.

        Args:
            date_range (list[datetime]): A list containing two datetime objects - [start_date, end_date]

        Returns:
            None
        """
        self.list_date.append(date_range)
        sub_df = pd.DataFrame.from_dict(
            data={"start_date": [date_range[0]], "end_date": [date_range[1]]}
        )
        self.df = pd.concat([self.df, sub_df])


if __name__ == "__main__":
    start_date = datetime(2024, 1, 1)
    maturity_date = datetime(2024, 12, 2)
    schedule_fix = Schedule(
        start_date=start_date,
        maturity_date=maturity_date,
        periodicity=3,
        type_fill="Forward",
    )
    print(schedule_fix.df)
    print(schedule_fix.list_date)
