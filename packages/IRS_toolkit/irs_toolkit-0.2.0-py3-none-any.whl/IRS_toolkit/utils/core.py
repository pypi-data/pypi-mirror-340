# Standard library imports
import calendar
from datetime import date, datetime, timedelta
from typing import Union
from dateutil.easter import easter

# Third-party library imports
import pandas as pd
from dateutil.relativedelta import relativedelta
from IRS_toolkit.utils.constants import VALID_CONVENTIONS
# Constants


def day_count(
    start: Union[date, datetime],
    end: Union[date, datetime],
    convention: VALID_CONVENTIONS,
) -> float:
    """
    This function computes the period in years between two given dates
    with a defined convention.

    Args:
        start (datetime): start date
        end (datetime): end date
        convention (str): day count convention.

    Returns:
        float: day count with the given day count convention
    """
    # Validate inputs
    if end < start:
        raise ValueError("End date must be after start date")

    if end == start:
        return 0.0

    # Call the appropriate helper function based on convention
    convention_handlers = {
        "ACT/360": _act_360_day_count,
        "ACT/365": _act_365_day_count,
        "ACT/ACT": _act_act_day_count,
        "30/360": _thirty_360_day_count,
    }

    if convention not in convention_handlers:
        raise ValueError(
            f"Invalid convention: {convention}. Valid conventions are {VALID_CONVENTIONS}."
        )

    return convention_handlers[convention](start, end)


def _act_360_day_count(
    start: Union[date, datetime], end: Union[date, datetime]
) -> float:
    """Calculate day count using ACT/360 convention."""
    return (end - start).days / 360


def _act_365_day_count(
    start: Union[date, datetime], end: Union[date, datetime]
) -> float:
    """Calculate day count using ACT/365 convention."""
    return (end - start).days / 365


def _act_act_day_count(
    start: Union[date, datetime], end: Union[date, datetime]
) -> float:
    """Calculate day count using ACT/ACT convention."""
    start_dt = start
    end_dt = end

    if start_dt.year == end_dt.year:
        days_in_year = 366 if calendar.isleap(start_dt.year) else 365
        days = (end_dt - start_dt).days
        return days / days_in_year
    else:
        # Calculate for different years
        result = 0.0

        # First partial year
        year1_end = datetime(start_dt.year + 1, 1, 1)
        days_year1 = 366 if calendar.isleap(start_dt.year) else 365
        result += (year1_end - start_dt).days / days_year1

        # Full years in between
        result += end_dt.year - start_dt.year - 1

        # Last partial year
        year2_start = datetime(end_dt.year, 1, 1)
        days_year2 = 366 if calendar.isleap(end_dt.year) else 365
        result += (end_dt - year2_start).days / days_year2

        return result


def _thirty_360_day_count(
    start: Union[date, datetime], end: Union[date, datetime]
) -> float:
    """Calculate day count using 30/360 convention."""

    def is_last_day_of_month(date: Union[date, datetime]) -> bool:
        # Get the last day of the month for the given date
        last_day = calendar.monthrange(date.year, date.month)[1]
        # Check if the given date is the last day of the month
        return date.day == last_day

    # Extract year, month, day from the dates
    start_year, start_month, start_day = start.year, start.month, start.day
    end_year, end_month, end_day = end.year, end.month, end.day

    # Adjust days for 30/360 calculation
    if is_last_day_of_month(start):
        start_day = 30
        if is_last_day_of_month(end):
            end_day = 30

    # Calculate the difference in days
    return (
        (end_year - start_year) * 360
        + (end_month - start_month) * 30
        + (end_day - start_day)
    ) / 360


def linear_interpolation(
    list_dates: list[Union[datetime, date]], list_values: list[float], target_dates=None
) -> pd.DataFrame:
    """
    Interpolate values for given dates.

    Args:
        dates: List of datetime objects
        values: List of numerical values
        target_dates: Optional list of target dates for interpolation
                     If None, will use daily frequency between min and max date

    Returns:
        Two lists: interpolated_dates, interpolated_values
    """
    # Create a DataFrame with dates and values
    df = pd.DataFrame({"value": list_values}, index=pd.DatetimeIndex(list_dates))

    # If target_dates not provided, create daily sequence

    if target_dates is None:
        target_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")

    # Interpolate values
    df_interpolated = df.reindex(target_dates).interpolate(method="linear")
    df_interpolated["DATES"] = df_interpolated.index
    df_interpolated.rename(columns={"value": "VALUES"}, inplace=True)
    df_interpolated.reset_index(inplace=True, drop=True)
    df_interpolated.columns = ["VALUES", "DATES"]
    return df_interpolated


def tenor_to_period(tenor: str) -> Union[timedelta, relativedelta]:
    """
    Convert a given tenor to a period.

    Args:
        tenor (str): A string representing the tenor (e.g., '1D', '2W', '3M', '1Y').

    Returns:
        Union[timedelta, relativedelta]: The corresponding period as a timedelta or relativedelta object.

    Raises:
        ValueError: If the tenor unit is invalid.

    Example:
        >>> tenor_to_period('1D')
        datetime.timedelta(days=1)
        >>> tenor_to_period('2W')
        datetime.timedelta(days=14)
        >>> tenor_to_period('3M')
        relativedelta(months=+3)
    """
    # Extract numeric value and unit from the tenor
    tenor_value = int(tenor[:-1])
    tenor_unit = tenor[-1].lower()

    # Define a dictionary mapping tenor units to their corresponding period objects
    dict_tenor = {
        "d": timedelta(days=tenor_value),
        "w": timedelta(weeks=tenor_value),
        "m": relativedelta(months=tenor_value),
        "y": relativedelta(years=tenor_value),
    }

    # Return the corresponding period if the unit is valid, otherwise raise an error
    if tenor_unit in dict_tenor:
        return dict_tenor[tenor_unit]
    else:
        raise ValueError(
            f"Invalid tenor unit: {tenor_unit}. Valid units are 'd', 'w', 'm', 'y'."
        )


def period_to_tenor(period: int) -> str:
    """
    Convert a given period in days to its corresponding tenor.

    Args:
        period (int): Number of days.

    Returns:
        str: Corresponding tenor, or None if no match is found.

    Note:
        This function assumes 30 days per month and 360 days per year.
    """
    # Ensure period is an integer
    period = int(period)

    # Define tenor dictionary with optimized calculations
    tenor_dict = {
        1: "1D",
        7: "1W",
        14: "2W",
        21: "3W",
        **{30 * i: f"{i}M" for i in range(1, 12)},  # 1M to 11M
        360: "1Y",
        360 + 90: "15M",
        360 + 180: "18M",
        360 + 270: "21M",
        **{360 * i: f"{i}Y" for i in range(2, 13)},  # 2Y to 12Y
        360 * 15: "15Y",
        360 * 20: "20Y",
        360 * 25: "25Y",
        360 * 30: "30Y",
    }
    if period in tenor_dict:
        result = tenor_dict.get(period)
    else:
        raise ValueError(
            f"Invalid period: {period}. Valid periods are {list(tenor_dict.keys())}."
        )

    # Return the tenor if found, otherwise None
    return result


def previous_coupon_date(
    list_start_dates: list[datetime],
    list_end_dates: list[datetime],
    valuation_date: datetime,
) -> datetime:
    """
    get the pervious coupon date with a given valuation date

    Args:
        df (Dataframe): Payments  details
        valuation_date (datetime): valuation date

    Returns:
        datetime: previous coupon date
    """
    list_start_dates = list(list_start_dates)
    list_end_dates = list(list_end_dates)
    if valuation_date < list_start_dates[0]:
        raise ValueError("Valuation date is before the first coupon date")
    elif valuation_date > list_end_dates[-1]:
        return valuation_date
    else:
        previous_coupon = valuation_date

    for date_index in range(len(list_start_dates)):
        if (
            valuation_date >= list_start_dates[date_index]
            and valuation_date < list_end_dates[date_index]
        ):
            previous_coupon = list_start_dates[date_index]
    return previous_coupon


def setup_business_days_calendar(start_year=2022, end_year=2100):
    """
    Create business days calendar with holidays.
    """
    # Generate Easter holidays (Good Friday and Easter Monday)
    easter_holidays = []
    for year in range(start_year, end_year + 1):
        easter_sunday = easter(year)
        easter_holidays.extend(
            [
                easter_sunday - timedelta(days=2),  # Good Friday
                easter_sunday + timedelta(days=1),  # Easter Monday
            ]
        )

    # Generate fixed holidays for all years
    fixed_holidays = []
    for year in range(start_year, end_year + 1):
        fixed_holidays.extend(
            [
                datetime(year, 1, 1),  # New Year's Day
                datetime(year, 5, 1),  # Labor Day
                datetime(year, 12, 25),  # Christmas
                datetime(year, 12, 26),  # Boxing Day
            ]
        )

    # Combine all holidays
    all_holidays = easter_holidays + fixed_holidays

    return pd.DataFrame(
        {
            "date": pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31"),
            "business_day": True,
        }
    ).assign(
        business_day=lambda df: ~(
            df["date"].dt.dayofweek.isin([5, 6])  # Weekends
            | df["date"].isin(all_holidays)  # Holidays
        )
    )


def adjust_to_business_day(date, business_days):
    """
    Adjust a date to the next business day if it falls on a non-business day.
    """
    if isinstance(date, (str, pd.Timestamp)):
        date = pd.to_datetime(date).to_pydatetime()

    is_business_day = business_days.loc[
        business_days["date"] == date, "business_day"
    ].iloc[0]
    if is_business_day:
        return date

    next_business_day = business_days.loc[
        (business_days["date"] > date) & (business_days["business_day"]), "date"
    ].iloc[0]

    return next_business_day
