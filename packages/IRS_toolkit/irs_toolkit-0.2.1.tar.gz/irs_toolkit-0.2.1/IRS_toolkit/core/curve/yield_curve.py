# Standard library imports
import warnings
from datetime import datetime, timedelta, timezone


# Third-party imports
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from typing import Optional

# Local/application imports
from IRS_toolkit.utils import core, financial
from IRS_toolkit.utils.constants import (
    VALID_COUPON_FREQUENCY,
    VALID_CONVENTIONS,
    pay_frequency,
)

# Configure warnings
warnings.filterwarnings("ignore")


class YieldCurve:
    """
    A class for handling yield curves used in pricing and preparing
    zero-coupon curves for cash flow computation and discounting.

    Args:
        list_tenor (list[str]): List of tenors (e.g. ["1M", "3M", "6M", "1Y"])
        list_rate (list[float]): List of corresponding rates
        date_curve (datetime, optional): Reference date for the curve
        date_convention (str, optional): Day count convention. Defaults to "ACT/360"
        date_format (str, optional): Date format string. Defaults to "%Y-%m-%d"
        data_base (int, optional): Base for rate calculations. Defaults to 1
        compounding_type (str, optional): Type of compounding - "discrete" or "continuous". Defaults to "discrete".
        business_days (pd.DataFrame, optional): Business days calendar. If None, uses default from core.py

    Attributes:
        date_curve (datetime): Reference date for the curve
        df (pd.DataFrame): DataFrame containing dates, zero-coupon rates and discount factors
        compounding_type (str): Type of rate compounding
        list_tenor (list): List of tenors
        list_rate (list): List of rates
        date_convention (str): Day count convention
        date_format (str): Date format string
        base_data (int): Base for rate calculations
        business_days (pd.DataFrame): Business days calendar

    Methods:
        bootstrap(): Compute the zero-coupon curve using bootstrapping
        forward_rates(): Compute forward rates between two dates
        monthly_avg_daily(): Compute monthly averages of daily forward rates
    """

    def __init__(
        self,
        list_tenor: list[str],
        list_rate: list[float],
        date_curve: Optional[datetime] = None,
        date_convention: VALID_CONVENTIONS = "ACT/360",
        date_format="%Y-%m-%d",
        data_base=1,
        compounding_type="discrete",
        business_days: pd.DataFrame = None,
    ):
        """
        Initialize a YieldCurve instance.

        Args:
            list_tenor (list[str]): List of tenors (e.g. ["1M", "3M", "6M", "1Y"])
            list_rate (list[float]): List of corresponding rates
            date_curve (datetime, optional): Reference date for the curve
            date_convention (str, optional): Day count convention. Defaults to "ACT/360"
            date_format (str, optional): Date format string. Defaults to "%Y-%m-%d"
            data_base (int, optional): Base for rate calculations. Defaults to 1
            compounding_type (str, optional): Type of compounding - "discrete" or "continuous". Defaults to "discrete".
            business_days (pd.DataFrame, optional): Business days calendar. If None, uses default from core.py
        """
        if compounding_type not in ["discrete", "continuous"]:
            raise ValueError(
                "compounding_type must be either 'discrete' or 'continuous'"
            )

        self.compounding_type = compounding_type
        self.base_data = data_base
        new_list_rate = [x / data_base for x in list_rate]

        # Store input parameters
        self.list_tenor = list_tenor
        self.list_rate = new_list_rate
        self.date_curve = date_curve
        self.date_convention = date_convention
        self.date_format = date_format

        # Check if curve_date is a weekend day
        if (
            self.date_curve and self.date_curve.weekday() >= 5
        ):  # 5 is Saturday, 6 is Sunday
            raise ValueError(
                f"Curve date {self.date_curve.strftime('%Y-%m-%d')} is a weekend day. Please use a week day."
            )

        # Initialize business days calendar
        start_year = (
            self.date_curve.year
            if self.date_curve
            else datetime.now(tz=timezone.utc).year
        )
        self.business_days = (
            business_days
            if business_days is not None
            else core.setup_business_days_calendar(start_year=start_year)
        )

        # Create initial dataframe with input tenors and rates
        df = pd.DataFrame(
            {
                "TENOR": ["0D", *self.list_tenor],  # Add 0D tenor at start
                "STRIPPEDRATES": [np.nan, *self.list_rate],  # Add NaN rate for 0D
                "AS_OF_DATE": [date_curve] * (len(self.list_tenor) + 1),
                "DATE": [date_curve] * (len(self.list_tenor) + 1),
                "PERIOD": [0] * (len(self.list_tenor) + 1),
                "DAY_COUNT": [0] * (len(self.list_tenor) + 1),
            }
        )

        # Add dates if date_curve is provided
        if date_curve is not None:
            for i in range(len(df)):
                tenor = df.loc[i, "TENOR"]
                is_short_tenor = tenor in ["0D", "1D", "2D"]

                # Set AS_OF_DATE - curve date for short tenors, 2D date for others
                df.loc[i, "AS_OF_DATE"] = (
                    self.date_curve
                    if is_short_tenor
                    else df.loc[df["TENOR"] == "2D", "DATE"].iloc[0]
                )

                # Calculate DATE
                if tenor == "2D":
                    one_day_date = core.adjust_to_business_day(
                        pd.to_datetime(
                            df.loc[i, "AS_OF_DATE"] + core.tenor_to_period("1D")
                        ),
                        self.business_days,
                    )
                    df.loc[i, "DATE"] = core.adjust_to_business_day(
                        one_day_date + relativedelta(days=1), self.business_days
                    )
                else:
                    df.loc[i, "DATE"] = core.adjust_to_business_day(
                        pd.to_datetime(
                            df.loc[i, "AS_OF_DATE"] + core.tenor_to_period(tenor)
                        ),
                        self.business_days,
                    )

                # Calculate PERIOD and DAY_COUNT
                reference_date = (
                    df.loc[df["TENOR"] == "1D", "DATE"].iloc[0]
                    if tenor == "2D"
                    else (
                        self.date_curve if is_short_tenor else df.loc[i, "AS_OF_DATE"]
                    )
                )
                df.loc[i, "PERIOD"] = (df.loc[i, "DATE"] - reference_date).days
                df.loc[i, "DAY_COUNT"] = core.day_count(
                    reference_date, df.loc[i, "DATE"], convention=self.date_convention
                )

        df.sort_index(inplace=True)
        self.df = df
        self._setup_interpolated_curve()

    def _calculate_zc_rates(self, rate, period):
        """
        Helper method to calculate zero-coupon rates based on compounding type.

        Args:
            rate (float): Interest rate
            period (float): Time period

        Returns:
            float: Zero-coupon rate
        """
        if period == 0:
            return 0.0
        if self.compounding_type == "discrete":
            return (1 + rate * period) ** (1 / period) - 1
        else:  # continuous
            return np.log(1 + rate * period) / period

    def _calculate_discount_factor(self, zc_rate, period):
        """
        Helper method to calculate discount factors based on compounding type.

        Args:
            zc_rate (float): Zero-coupon rate
            period (float): Time period

        Returns:
            float: Discount factor
        """
        if period == 0:
            return 1.0

        if self.compounding_type == "discrete":
            return 1 / (1 + zc_rate) ** period
        else:  # continuous
            return np.exp(-zc_rate * period)

    def _setup_interpolated_curve(self):
        """
        Setup the interpolated curve with daily rates.
        """
        # Create a copy of the original dataframe
        interpolated_df = self.df.copy()

        # Calculate relative deltas and dates
        interpolated_df["RELATIVEDELTA"] = interpolated_df["TENOR"].apply(
            lambda x: relativedelta(days=1) if x == "2D" else core.tenor_to_period(x)
        )

        # Calculate relative dates
        one_day_date = interpolated_df.loc[
            interpolated_df["TENOR"] == "1D", "DATE"
        ].iloc[0]
        interpolated_df["RELATIVE_DATE"] = interpolated_df.apply(
            lambda x: core.adjust_to_business_day(
                one_day_date + x["RELATIVEDELTA"]
                if x["TENOR"] == "2D"
                else x["AS_OF_DATE"] + x["RELATIVEDELTA"],
                self.business_days,
            ),
            axis=1,
        )

        # Calculate periods
        interpolated_df["PERIOD"] = (
            interpolated_df["RELATIVE_DATE"] - self.date_curve
        ).dt.days

        # Create daily periods and interpolate rates
        max_period = max(interpolated_df["PERIOD"])
        daily_periods = pd.DataFrame({"PERIOD": np.arange(1, max_period + 1)})
        interpolated_df = daily_periods.merge(interpolated_df, "left", on="PERIOD")
        interpolated_df["STRIPPEDRATES"] = interpolated_df["STRIPPEDRATES"].astype(
            float
        )

        # Add dates and day counts
        interpolated_df["DATE"] = interpolated_df["PERIOD"].apply(
            lambda x: self.date_curve + timedelta(days=x)
        )

        interpolated_df["DAY_COUNT"] = interpolated_df.apply(
            lambda x: core.day_count(
                self.date_curve, x["DATE"], convention=self.date_convention
            ),
            axis=1,
        )

        # Interpolate rates
        interpolated_df.set_index("DAY_COUNT", inplace=True, drop=False)
        interpolated_df["STRIPPEDRATES"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )

        # Add 0D row at start
        zero_day = pd.DataFrame(
            [
                {
                    "PERIOD": 0,
                    "TENOR": "0D",
                    "STRIPPEDRATES": np.nan,
                    "DATE": self.date_curve,
                    "DAY_COUNT": 0.0,
                }
            ]
        )

        interpolated_df = pd.concat([zero_day, interpolated_df])
        interpolated_df.sort_index(inplace=True)

        # Keep only needed columns and rename tenors
        df_interpolated = interpolated_df[
            ["TENOR", "STRIPPEDRATES", "PERIOD", "DATE", "DAY_COUNT"]
        ]
        df_interpolated.loc[df_interpolated["TENOR"] == "1D", "TENOR"] = "ON"
        df_interpolated.loc[df_interpolated["TENOR"] == "2D", "TENOR"] = "TN"

        self.df_interpolated = df_interpolated

    def bootstrap(self, coupon_frequency: VALID_COUPON_FREQUENCY, zc_curve=None):
        """
        Transform the yield curve to a zero-coupon (ZC) curve using bootstrapping.

        Args:
            coupon_frequency (str): Frequency of coupon payments (e.g. "1M", "3M", "6M", "1Y")
            zc_curve (pd.DataFrame, optional): Input zero-coupon curve. If None, uses self.df

        Updates the instance's df attribute with bootstrapped rates and discount factors
        """
        # Use provided curve or copy of self.df
        if zc_curve is None:
            zc_curve = self.df.copy()

        # Calculate coupon periods and frequency
        coupon_periods = int(12 / pay_frequency[coupon_frequency]) * 60
        coupon_frequency_date = pay_frequency[coupon_frequency]

        # Get tomorrow next date and use it as base for coupon dates
        tn_date = zc_curve.loc[zc_curve["TENOR"] == "2D", "DATE"].iloc[0]

        # Generate coupon dates
        zc_date = [
            tn_date + relativedelta(months=i * coupon_frequency_date)
            for i in range(coupon_periods + 1)
        ]

        # Adjust dates to business days
        zc_date = [
            core.adjust_to_business_day(date, self.business_days) for date in zc_date
        ]

        # Process curve before first coupon date
        zc_curve_before = zc_curve[zc_curve["DATE"] < zc_date[1]].copy()
        zc_curve_before["Coupon_period"] = zc_curve_before["DAY_COUNT"]

        # Calculate ZC rates and discount factors for the first part
        zc_curve_before["ZC"] = zc_curve_before.apply(
            lambda x: self._calculate_zc_rates(x["STRIPPEDRATES"], x["Coupon_period"]),
            axis=1,
        )
        zc_curve_before["DF"] = zc_curve_before.apply(
            lambda x: self._calculate_discount_factor(x["ZC"], x["Coupon_period"]),
            axis=1,
        )

        # Process remaining curve
        zc_curve_temp = zc_curve[zc_curve["DATE"].isin(zc_date[1:])].copy()
        zc_curve_temp.reset_index(drop=True, inplace=True)

        # Calculate coupon periods for the remaining curve
        zc_curve_temp["Date_lagg"] = zc_curve_temp["DATE"].shift()
        zc_curve_temp["Date_lagg"].fillna(
            zc_curve_temp["AS_OF_DATE"].iloc[0], inplace=True
        )
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: core.day_count(x["Date_lagg"], x["DATE"], self.date_convention),
            axis=1,
        )

        # Calculate discount factors iteratively
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["STRIPPEDRATES"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["STRIPPEDRATES"][i] * zc_curve_temp["Coupon_period"][i]
            )

        # Calculate ZC rates from discount factors
        if self.compounding_type == "discrete":
            zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
                1 / zc_curve_temp["DAY_COUNT"]
            ) - 1
        else:  # continuous
            zc_curve_temp["ZC"] = (
                -np.log(zc_curve_temp["DF"]) / zc_curve_temp["DAY_COUNT"]
            )

        # Combine and process final curve
        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)

        # Update main dataframe
        self.df = zc_curve.merge(zc_curve.dropna(), "left")

        # Create daily dates
        dates = pd.DataFrame(
            {
                "DATE": pd.date_range(
                    start=self.date_curve, end=zc_curve["DATE"].iloc[-1], freq="D"
                )
            }
        )

        # Merge and interpolate
        self.df = dates.merge(zc_curve, "left")

        # Fix 2D discount factor
        self.df.loc[self.df["TENOR"] == "2D", "DF"] = (
            self.df.loc[self.df["TENOR"] == "1D", "DF"].iloc[0]
            * self.df.loc[self.df["TENOR"] == "2D", "DF"].iloc[0]
        )

        # Set AS_OF_DATE based on date
        self.df["AS_OF_DATE"] = np.where(
            self.df["DATE"] <= tn_date, self.date_curve, tn_date
        )

        # Interpolate discount factors
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )

        # Calculate additional fields
        self.df["PERIOD"] = (self.df["DATE"] - self.date_curve).dt.days

        # Calculate day counts in ACT/ACT convention
        self.df["DAY_COUNT_ACT_ACT"] = self.df.apply(
            lambda x: core.day_count(self.date_curve, x["DATE"], "ACT/ACT"), axis=1
        )

        self.df["DF"] = self.df["DF"].astype(float)

        # Get DF value at two days
        as_of_df = self.df.loc[self.df["TENOR"] == "2D", "DF"].iloc[0]

        # Multiply DF by the DF at two days for dates after two days (TN)
        mask = self.df["DATE"] > tn_date
        self.df.loc[mask, "DF"] = self.df.loc[mask, "DF"] * as_of_df

        # Calculate final ZC rates
        if self.compounding_type == "discrete":
            self.df["ZC"] = (1 / self.df["DF"]) ** (
                1 / self.df["DAY_COUNT_ACT_ACT"]
            ) - 1
        else:  # continuous
            self.df["ZC"] = -np.log(self.df["DF"]) / self.df["DAY_COUNT_ACT_ACT"]

        # Interpolate stripped rates
        self.df["STRIPPEDRATES"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )

        # Set initial values
        self.df.at[0, "DF"] = 1
        self.df.at[0, "Coupon_period"] = 0
        self.df.at[0, "ZC"] = 0

        # Calculate day counts using the chosen convention
        self.df["DAY_COUNT"] = self.df.apply(
            lambda x: core.day_count(self.date_curve, x["DATE"], self.date_convention),
            axis=1,
        )

        # Cut the DataFrame to the last row with a valid TENOR value
        last_valid_tenor = self.df[self.df["TENOR"].notna()].index[-1]
        self.df = self.df.iloc[: last_valid_tenor + 1]

    def forward_rates(self, begin: datetime, end: datetime, relative_delta=None):
        """
        Compute forward rates between two dates.

        Args:
            begin (datetime): Start date
            end (datetime): End date
            relative_delta (relativedelta, optional): Optional time delta to adjust end date

        Returns:
            float: Forward rate between the two dates, or None if dates are invalid
        """
        # Set default relative delta if not provided
        if relative_delta is None:
            relative_delta = relativedelta(days=0)

        # Convert string dates to datetime if necessary
        begin_date = (
            datetime.strptime(begin, self.date_format)
            if isinstance(begin, str)
            else begin
        )
        end_date = (
            datetime.strptime(end, self.date_format) if isinstance(end, str) else end
        )
        end_date = end_date + relative_delta

        # Validate date ranges
        if end_date < self.date_curve or begin_date >= end_date:
            return None

        # Format dates for lookup
        begin_str = begin_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        # Get zero-coupon rates and discount factors
        zc_begin = self.df.loc[self.df["DATE"] == begin_str, "ZC"]
        zc_end = self.df.loc[self.df["DATE"] == end_str, "ZC"]
        df_begin = self.df.loc[self.df["DATE"] == begin_str, "DF"]
        df_end = self.df.loc[self.df["DATE"] == end_str, "DF"]

        # Return None if dates not found in curve
        if zc_begin.empty or zc_end.empty:
            return None

        # Calculate time periods
        time_begin = core.day_count(self.date_curve, begin_date, "ACT/360")
        time_end = core.day_count(self.date_curve, end_date, "ACT/360")
        delta_t = core.day_count(begin_date, end_date, "ACT/360")

        # Calculate forward rate based on compounding type
        if self.compounding_type == "discrete":
            num = (1 + zc_end.iloc[0]) ** time_end
            den = (1 + zc_begin.iloc[0]) ** time_begin
            return (num / den) ** (1.0 / delta_t) - 1
        else:  # continuous
            return (time_end * zc_end.iloc[0] - time_begin * zc_begin.iloc[0]) / delta_t

    def monthly_avg_daily(
        self,
        start_date: datetime,
        end_date: datetime,
        frequency: str = "D",
        relative_delta=None,
    ):
        """
        Compute monthly averages of daily forward rates between specified dates.

        Args:
            start_date (datetime): Start date for forward rate calculations
            end_date (datetime): End date for forward rate calculations
            frequency (str, optional): Frequency for rate calculations. Defaults to "D" (daily).
                Can be "D" (daily), "W" (weekly), "M" (monthly), or "Between Tenor"
            relative_delta (relativedelta, optional): Optional time delta to adjust end dates

        Returns:
            tuple: (monthly_averages, daily_rates)
                - monthly_averages: DataFrame with monthly averages of forward rates
                - daily_rates: DataFrame with daily forward rates
        """
        if relative_delta is None:
            relative_delta = relativedelta(days=0)

        # Define time delta dictionary for "Between Tenor" frequency
        timedelta_dict = {
            "1D": relativedelta(days=1),
            "2D": relativedelta(days=2),
            "1W": relativedelta(weeks=1),
            "2W": relativedelta(weeks=2),
            "3W": relativedelta(weeks=3),
            "1M": relativedelta(months=1),
            "2M": relativedelta(months=2),
            "3M": relativedelta(months=3),
            "4M": relativedelta(months=4),
            "5M": relativedelta(months=5),
            "6M": relativedelta(months=6),
            "7M": relativedelta(months=7),
            "8M": relativedelta(months=8),
            "9M": relativedelta(months=9),
            "10M": relativedelta(months=10),
            "11M": relativedelta(months=11),
            "1Y": relativedelta(years=1),
            "15M": relativedelta(months=15),
            "18M": relativedelta(months=18),
            "21M": relativedelta(months=21),
            "2Y": relativedelta(years=2),
            "3Y": relativedelta(years=3),
            "4Y": relativedelta(years=4),
            "5Y": relativedelta(years=5),
            "6Y": relativedelta(years=6),
            "7Y": relativedelta(years=7),
            "8Y": relativedelta(years=8),
            "9Y": relativedelta(years=9),
            "10Y": relativedelta(years=10),
            "11Y": relativedelta(years=11),
            "12Y": relativedelta(years=12),
            "15Y": relativedelta(years=15),
            "20Y": relativedelta(years=20),
            "25Y": relativedelta(years=25),
            "30Y": relativedelta(years=30),
            "40Y": relativedelta(years=40),
            "50Y": relativedelta(years=50),
            "60Y": relativedelta(years=60),
        }

        # Convert string dates to datetime if necessary
        start_date = (
            datetime.strptime(start_date, self.date_format)
            if isinstance(start_date, str)
            else start_date
        )
        end_date = (
            datetime.strptime(end_date, self.date_format)
            if isinstance(end_date, str)
            else end_date
        )

        # Generate date list based on frequency
        if frequency == "Between Tenor":
            date_list = []
            base_date = start_date
            for tenor, delta in timedelta_dict.items():
                next_date = core.adjust_to_business_day(
                    base_date + delta, self.business_days
                )
                if next_date <= end_date:
                    date_list.append(next_date)
        else:
            # Generate dates using pandas date_range
            date_list = pd.date_range(start=start_date, end=end_date, freq=frequency)
            # Adjust dates to business days
            date_list = [
                core.adjust_to_business_day(date, self.business_days)
                for date in date_list
            ]

        # Create DataFrame for forward rates
        forward_df = pd.DataFrame(
            {"start_date": date_list[:-1], "end_date": date_list[1:]}
        )

        # Calculate forward rates
        forward_df["foreward_ZC"] = forward_df.apply(
            lambda x: self.forward_rates(
                x["start_date"], x["end_date"], relative_delta
            ),
            axis=1,
        )

        # Calculate day counts
        forward_df["day_count"] = forward_df.apply(
            lambda x: core.day_count(
                x["start_date"], x["end_date"], self.date_convention
            ),
            axis=1,
        )

        # Convert to simple rates if using discrete compounding

        forward_df["forward_simple"] = forward_df.apply(
            lambda x: financial.zc_to_simplerate(x["foreward_ZC"], x["day_count"]),
            axis=1,
        )

        # Set index for grouping
        forward_df = forward_df.set_index("start_date")
        forward_df.index = pd.to_datetime(forward_df.index)

        # Calculate monthly averages
        monthly_avg = forward_df.groupby(pd.Grouper(freq="M")).mean()

        return monthly_avg, forward_df

    def bootstrap_12m_semi_yearly_coupon(
        self, coupon_frequency: VALID_COUPON_FREQUENCY
    ):
        """
        Transform the yield curve to a zero-coupon (ZC) curve.

        This function processes the initial curve data to compute zero-coupon rates and discount factors.
        It handles different date calculations based on whether the current day is the first of the month.
        """
        zc_curve = self.df.copy()

        coupon_periods = {
            "quarterly": 29 * 4,
            "yearly": 29,
            "monthly": 29 * 12,
            "semi_annual": 29 * 2,
        }[coupon_frequency]
        coupon_frequency_date = {
            "quarterly": pd.DateOffset(months=3),  # "3MS",
            "yearly": pd.DateOffset(years=1),
            "monthly": pd.DateOffset(months=1),
            "semi_annual": pd.DateOffset(months=6),
        }[coupon_frequency]

        # if self.date.day == 1:
        zc_date1 = pd.date_range(
            self.date.strftime(self.date_format),
            periods=2,
            freq=pd.DateOffset(months=6),
        )

        zc_date2 = pd.date_range(
            (self.date + pd.DateOffset(years=1)).strftime(self.date_format),
            periods=coupon_periods,
            freq=coupon_frequency_date,
        )

        zc_date = zc_date1.append(zc_date2)

        zc_curve_before = zc_curve[zc_curve["Date"] < zc_date[1]]
        zc_curve_before["Period"] = (zc_curve_before["Date"] - self.date).apply(
            lambda x: x.days
        )

        zc_curve_before["Coupon_period"] = zc_curve_before["day_count"]

        zc_curve_before["ZC"] = (
            1 + zc_curve_before["StrippedRates"] * zc_curve_before["Coupon_period"]
        ) ** (1 / zc_curve_before["Coupon_period"]) - 1
        zc_curve_before["DF"] = (
            1 / (1 + zc_curve_before["ZC"]) ** (zc_curve_before["Coupon_period"])
        )

        zc_curve_temp = zc_curve[zc_curve["Date"].isin(zc_date)]
        zc_curve_temp.reset_index(drop=True, inplace=True)
        zc_curve_temp["Date_lagg"] = zc_curve_temp["Date"].shift()
        zc_curve_temp["Date_lagg"].fillna(self.date, inplace=True)
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: core.day_count(x["Date_lagg"], x["Date"], self.date_convention),
            axis=1,
        )
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["StrippedRates"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["StrippedRates"][i] * zc_curve_temp["Coupon_period"][i]
            )
        zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
            1 / zc_curve_temp["day_count"]
        ) - 1
        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)
        self.df = self.df.merge(zc_curve.dropna(), "left")
        dates = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=self.date + relativedelta(days=1),
                    end=self.date + relativedelta(years=30),
                    freq="D",
                ),
            }
        )

        self.df = dates.merge(self.df, "left")
        self.df["DF"] = self.df["DF"].astype(float)
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: core.day_count(self.date, x["Date"], self.date_convention), axis=1
        )
        self.df["ZC"] = (1 / self.df["DF"]) ** (1 / self.df["day_count"]) - 1
        self.df["StrippedRates"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
