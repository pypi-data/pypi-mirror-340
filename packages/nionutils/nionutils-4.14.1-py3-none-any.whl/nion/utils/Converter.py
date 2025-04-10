"""
    Converter classes. Useful for bindings.
"""

# standard libraries
import datetime
import locale
import pathlib
import re
import typing
import uuid

# third party libraries
# none

# local libraries
# none

FT = typing.TypeVar('FT')
TT = typing.TypeVar('TT')


class ConverterLike(typing.Protocol[FT, TT]):
    def convert(self, value: typing.Optional[FT]) -> typing.Optional[TT]: ...

    def convert_back(self, formatted_value: typing.Optional[TT]) -> typing.Optional[FT]: ...


class IntegerToStringConverter(ConverterLike[int, str]):
    """ Convert between int value and formatted string. """

    def __init__(self, format: typing.Optional[str] = None, pass_none: bool = False, fuzzy: bool = True) -> None:
        """ format specifies int to string conversion """
        self.__format = format if format else "{:d}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value: typing.Optional[int]) -> typing.Optional[str]:
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(int(value) if value is not None else 0)

    def convert_back(self, formatted_value: typing.Optional[str]) -> typing.Optional[int]:
        """ Convert string to value using standard int conversion """
        formatted_value = re.sub(r"[+-](?!\d)|(?<=\.)\w*|[^-+0-9]", "", formatted_value) if self.__fuzzy and formatted_value else None
        if formatted_value:
            return int(formatted_value)
        else:
            return None if self.__pass_none else 0


class FloatToStringConverter(ConverterLike[float, str]):
    """ Convert between float value and formatted string. """

    def __init__(self, format: typing.Optional[str] = None, pass_none: bool = False, fuzzy: bool = True) -> None:
        self.__format = format if format else "{:g}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value: typing.Optional[float]) -> typing.Optional[str]:
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(value)

    def convert_back(self, formatted_value: typing.Optional[str]) -> typing.Optional[float]:
        """ Convert string to value using standard float conversion """
        if self.__pass_none and (formatted_value is None or len(formatted_value) == 0):
            return None
        decimal_point = str(locale.localeconv().get("decimal_point", "."))
        if self.__fuzzy:
            _parser = re.compile(r"""        # A numeric string consists of:
                (?P<sign>[-+])?              # an optional sign, followed by either...
                (
                    (?=\d|[\.,]\d)              # ...a number (with at least one digit)
                    (?P<int>\d*)             # having a (possibly empty) integer part
                    ([\.,](?P<frac>\d*))?       # followed by an optional fractional part
                    (E(?P<exp>[-+]?\d+))?    # followed by an optional exponent, or...
                )
            """, re.VERBOSE | re.IGNORECASE).match
            m = _parser(formatted_value.strip()) if formatted_value is not None else None
            if m is not None:
                if decimal_point != '.':
                    return locale.atof(m.group(0).replace(".", decimal_point))
                return locale.atof(m.group(0))
            return 0.0
        else:
            if decimal_point != '.':
                return locale.atof(formatted_value.replace(".", decimal_point) if formatted_value else str())
            return locale.atof(formatted_value) if formatted_value else 0.0


class FloatToScaledIntegerConverter(ConverterLike[float, int]):
    """ Convert between float value and int (float * 100). """

    def __init__(self, n: int, value_min: float = 0.0, value_max: float = 1.0) -> None:
        self.n = n
        self.value_min = value_min
        self.value_max = value_max

    def convert(self, value: typing.Optional[float]) -> typing.Optional[int]:
        """ Convert float between 0, 1 to percentage int """
        if value is not None:
            if self.value_max - self.value_min > 0.0:
                return int(self.n * (value - self.value_min) / (self.value_max - self.value_min))
            else:
                return 0
        else:
            return None

    def convert_back(self, value_int: typing.Optional[int]) -> typing.Optional[float]:
        """ Convert int percentage value to float """
        if value_int is not None:
            if self.n > 0 and self.value_max - self.value_min > 0.0:
                return (value_int * (self.value_max - self.value_min) / self.n + self.value_min)
            else:
                return 0.0
        else:
            return None


class FloatToPercentStringConverter(ConverterLike[float, str]):
    """ Convert between float value and percentage string. """

    def convert(self, value: typing.Optional[float]) -> typing.Optional[str]:
        """ Convert float between 0, 1 to percentage string """
        return str(int(value * 100)) + "%" if value is not None else None

    def convert_back(self, formatted_value: typing.Optional[str]) -> typing.Optional[float]:
        """ Convert percentage string to float between 0, 1 """
        return float(formatted_value.strip('%'))/100.0 if formatted_value is not None else None


class PhysicalValueToStringConverter(ConverterLike[float, str]):
    """ Convert between physical value represented by a float and a formatted string. """

    def __init__(self, units: str, multiplier: float=1.0, format:typing.Optional[str]=None, pass_none:bool=False, fuzzy:bool=True) -> None:
        self.__units = units
        self.__multiplier = multiplier
        self.__format = format + " {:s}" if format else "{:g} {:s}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value: typing.Optional[float]) -> typing.Optional[str]:
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(value * self.__multiplier, self.__units) if value is not None else None

    def convert_back(self, formatted_value: typing.Optional[str]) -> typing.Optional[float]:
        """ Convert string to value using standard float conversion """
        value = FloatToStringConverter().convert_back(formatted_value)
        return value / self.__multiplier if value is not None else None


class BoolToStringConverter(ConverterLike[bool, str]):
    def convert(self, value: typing.Optional[bool]) -> typing.Optional[str]:
        return "true" if value else "false"

    def convert_back(self, value: typing.Optional[str]) -> bool:
        return value.lower().strip() == "true" if value else False


class CheckedToCheckStateConverter(ConverterLike[bool, str]):
    """ Convert between bool and checked/unchecked strings. """

    def convert(self, value: typing.Optional[bool]) -> typing.Optional[str]:
        """ Convert bool to checked or unchecked string """
        return "checked" if bool(value) else "unchecked"

    def convert_back(self, value: typing.Optional[str]) -> bool:
        """ Convert checked or unchecked string to bool """
        return value == "checked"


class UuidToStringConverter(ConverterLike[uuid.UUID, str]):
    def convert(self, value: typing.Optional[uuid.UUID]) -> typing.Optional[str]:
        return str(value) if value else None

    def convert_back(self, value: typing.Optional[str]) -> typing.Optional[uuid.UUID]:
        if value and re.fullmatch("[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}", value.strip(),
                                  re.IGNORECASE) is not None:
            return uuid.UUID(value.strip())
        return None


class PathToStringConverter(ConverterLike[pathlib.Path, str]):
    def convert(self, value: typing.Optional[pathlib.Path]) -> typing.Optional[str]:
        return str(value) if value else None

    def convert_back(self, value: typing.Optional[str]) -> typing.Optional[pathlib.Path]:
        return pathlib.Path(value) if value else None


class DatetimeToStringConverter(ConverterLike[datetime.datetime, str]):
    """Convert between UTC datetime and str.

    datetime value is always utc and is naive to timezone.

    is_local can be used to _display_ the datetime in local time zone.

    format can be used to specify the format but must be parseable if used to convert both forward and back.
    """
    def __init__(self, is_local: bool = False, timezone: typing.Optional[datetime.tzinfo] = None, format: typing.Optional[str] = None) -> None:
        self.__is_local = is_local
        self.__timezone = timezone
        self.__format = format

    def convert(self, value: typing.Optional[datetime.datetime]) -> typing.Optional[str]:
        if value:
            if self.__is_local:
                value = value.replace(tzinfo=datetime.timezone.utc).astimezone().replace(tzinfo=None)
            elif self.__timezone:
                value = value.replace(tzinfo=datetime.timezone.utc).astimezone(self.__timezone).replace(tzinfo=None)
        if value and self.__format:
            return value.strftime(self.__format)
        return value.isoformat() if value is not None else None

    def convert_back(self, value: typing.Optional[str]) -> typing.Optional[datetime.datetime]:
        try:
            if self.__format:
                format_ = self.__format
            elif value and len(value) == 26:
                format_ = "%Y-%m-%dT%H:%M:%S.%f"
            elif value and len(value) == 19:
                format_ = "%Y-%m-%dT%H:%M:%S"
            else:
                format_ = str()

            dt = datetime.datetime.strptime(value, format_) if value else None

            if dt and self.__is_local:
                return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
            elif dt and self.__timezone:
                return dt.replace(tzinfo=self.__timezone).astimezone(datetime.timezone.utc).replace(tzinfo=None)
            else:
                return dt.replace(tzinfo=None) if dt else None
        except ValueError as e:
            print(e)
            pass  # fall through
        return None


class ValuesToIndexConverter(ConverterLike[FT, int], typing.Generic[FT]):
    """Convert between set of values of type FT and int index value."""

    def __init__(self, values: typing.Sequence[FT]) -> None:
        self.__values = list(values)

    def convert(self, value: typing.Optional[FT]) -> typing.Optional[int]:
        return self.__values.index(value) if value in self.__values else None

    def convert_back(self, index: typing.Optional[int]) -> typing.Optional[FT]:
        return self.__values[index] if index is not None and 0 <= index < len(self.__values) else None
