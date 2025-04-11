import datetime
import itertools
from typing import Any, Callable, Iterable, TypeVar

import numpy as np
import numpy.typing as npt
import skyfield.timelib

from thistle.typing import DateTime, TLETuple


def pairwise(iterable: Iterable) -> Iterable[tuple[Any, Any]]:
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


TIME_SCALE = "us"
EPOCH_DTYPE = np.dtype(f"datetime64[{TIME_SCALE}]")
ONE_SECOND_IN_TIME_SCALE = np.timedelta64(1, "s").astype(f"timedelta64[{TIME_SCALE}]")

DATETIME_MIN = datetime.datetime(1957, 1, 1)
DATETIME_MAX = datetime.datetime(2056, 12, 31, 23, 59, 59, 999999)
DATETIME64_MIN = np.datetime64(DATETIME_MIN, TIME_SCALE)
DATETIME64_MAX = np.datetime64(DATETIME_MAX, TIME_SCALE)

JDAY_1957 = 2435839.5


def datetime_to_dt64(dt: datetime.datetime) -> np.datetime64:
    dt = dt.replace(tzinfo=None)
    return np.datetime64(dt, TIME_SCALE)


def dt64_to_datetime(dt: np.datetime64) -> datetime.datetime:
    return datetime.datetime.fromisoformat(str(dt))


def validate_datetime64(value: DateTime) -> np.datetime64:
    return np.datetime64(value, TIME_SCALE)


def trange(
    start: datetime.datetime, stop: datetime.datetime, step: float
) -> np.ndarray[np.datetime64]:
    times = np.arange(
        datetime_to_dt64(start),
        datetime_to_dt64(stop),
        step * ONE_SECOND_IN_TIME_SCALE,
    )
    return times


def datetime_to_tle_epoch(dt: datetime.datetime) -> tuple[int, float]:
    midnight = datetime.datetime.combine(
        dt.date(), datetime.time(0, 0, 0), tzinfo=datetime.timezone.utc
    )
    fday = (dt - midnight).total_seconds()
    yr = int(dt.strftime("%y"))
    days = int(dt.strftime("%j")) + fday / 86_400
    return yr, days


def jday_datetime64(
    array: np.ndarray[np.datetime64],
) -> tuple[np.ndarray[np.float64], np.ndarray[np.float64]]:
    times = (
        (array - np.datetime64("1957-01-01", "us")).astype("i8") / 86_400 / 1_000_000
    )
    jd = np.floor(times)
    fr = times - jd
    jd += JDAY_1957
    return jd, fr


def time_to_dt64(time: skyfield.timelib.Time) -> npt.NDArray[np.datetime64]:
    dt, ls = time.utc_datetime_and_leap_second()
    dt = [
        a.replace(tzinfo=None) + datetime.timedelta(seconds=int(b))
        for a, b in zip(dt, ls)
    ]
    return np.array(dt, dtype=EPOCH_DTYPE)


def tle_epoch(tle: TLETuple) -> float:
    """Get the epoch (float) from a TLE, adjusted for Y2K."""
    epoch = float(tle[0][18:32].replace(" ", "0"))
    epoch += 1900_000 if epoch // 1000 >= 57 else 2000_000
    return epoch


def tle_date(tle: TLETuple) -> str:
    """Get the date (as str) from a TLE."""
    epoch = tle_epoch(tle)
    year, doy = divmod(epoch, 1000)
    doy = doy // 1
    dt = datetime.datetime(int(year), 1, 1) + datetime.timedelta(days=int(doy - 1))
    return dt.strftime("%Y%m%d")


def tle_satnum(tle: TLETuple) -> str:
    """Extract the (Alpha-5) Satnum from a TLE."""
    return tle[0][2:7].replace(" ", "0")


GroupByKey = TypeVar("GroupByKey")


def group_by(
    tles: list[TLETuple], key: Callable[[TLETuple], GroupByKey]
) -> dict[GroupByKey, list[TLETuple]]:
    """Groups input TLEs by values from a callable key."""
    results: dict[GroupByKey, list[TLETuple]] = {}
    for tle in tles:
        group = key(tle)
        if group not in results:
            results[group] = []
        results[group].append(tle)
    return results


T = TypeVar("T")


def unique(tles: list[T]) -> list[T]:
    """Returns input as a list list ensuring unique entries."""
    return list(dict.fromkeys(tles).keys())
