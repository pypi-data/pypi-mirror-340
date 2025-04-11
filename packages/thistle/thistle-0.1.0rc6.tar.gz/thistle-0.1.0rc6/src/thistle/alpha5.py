from typing import Union

_A_TO_I = {
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "J": 18,
    "K": 19,
    "L": 20,
    "M": 21,
    "N": 22,
    "P": 23,
    "Q": 24,
    "R": 25,
    "S": 26,
    "T": 27,
    "U": 28,
    "V": 29,
    "W": 30,
    "X": 31,
    "Y": 32,
    "Z": 33,
}
_I_TO_A = {val: key for key, val in _A_TO_I.items()}


def to_alpha5(satnum: int) -> str:
    """Encode an integer to an Alpha-5 string."""
    if satnum < 0 or satnum > 339_999:
        msg = "Alpha-5 satnum must be >= 0 and < 334,000 (encoded as Z9999)"
        raise ValueError(msg)

    if satnum < 100_000:
        return f"{satnum:05}"

    a, b = divmod(satnum, 10_000)
    return f"{_I_TO_A[a]}{b:04}"


def from_alpha5(satnum: str) -> int:
    """Decode an Alpha-5 string to an integer."""
    satnum = str(satnum)
    if satnum[0].isnumeric():
        return int(satnum)
    return _A_TO_I[satnum[0]] * 10_000 + int(satnum[1:])


def ensure_alpha5(satnum: Union[int, str]) -> str:
    if isinstance(satnum, int):
        return to_alpha5(satnum)
    elif isinstance(satnum, str):
        return satnum
    raise TypeError
