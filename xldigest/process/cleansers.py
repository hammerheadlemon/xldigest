from datetime import date, datetime
from operator import itemgetter
from typing import AnyStr, Callable, Any, Optional, Union, List, Dict
import re

from dateutil.parser import parse

ENDASH_REGEX = r"–"
ENDASH_FIX = r"-"
COMMA_REGEX = r",\s?"
COMMA_FIX = r" "
APOS_REGEX = r"^'"
APOS_FIX = r""
DATE_REGEX = r"^(\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4})"
DATE_REGEX_TIME = r"^(\d{2,4})(/|-)(\d{1,2})(/|-)(\d{1,2})\s(0:00:00)"
INT_REGEX = r"^[-+]?\d+$"
FLOAT_REGEX = r"^[-+]?([0-9]*)\.[0-9]+$"
NL_REGEX = r"\n"
NL_FIX = r" | "
SPACE_PIPE_CHAR_REGEX = r"\ \|\S"
SPACE_PIPE_CHAR_FIX = r" | "
PERCENT_REGEX = r"^(\d{1,3})%$"
POUND_REGEX = r"^(-)?£(\d+(\.\d{1,2})?)(\d+)?$"  # handles negative numbers


class Cleanser:
    """
    Takes a string, and cleans it.

    Doctests:
    >>> t = "Text, with commas"
    >>> c = Cleanser(t)
    >>> c.clean()
    'Text with commas'
    >>> a = "\'Text with leading apos."
    >>> c = Cleanser(a)
    >>> c.clean()
    'Text with leading apos.'

    """

    def __init__(self, string: str) -> None:
        self.string = string

        # a list of dicts that describe everything needed to fix errors in
        # string passed to class constructor. Method self.clean() runs through
        # them,  fixing each in turn.
        self._checks: List[Dict[str, Any]] = [
            dict(
                c_type="emdash",
                rule=ENDASH_REGEX,
                fix=ENDASH_FIX,
                func=self._endash,
                count=0),
            dict(
                c_type='commas',
                rule=COMMA_REGEX,
                fix=COMMA_FIX,
                func=self._commas,
                count=0),
            dict(
                c_type='leading_apostrophe',
                rule=APOS_REGEX,
                fix=APOS_FIX,
                func=self._apostrophe,
                count=0),
            dict(
                c_type='newline',
                rule=NL_REGEX,
                fix=NL_FIX,
                func=self._newline,
                count=0),
            dict(
                c_type='double_space',
                rule="  ",
                fix=" ",
                func=self._doublespace,
                count=0),
            dict(
                c_type='pipe_char',
                rule=SPACE_PIPE_CHAR_REGEX,
                fix=SPACE_PIPE_CHAR_FIX,
                func=self._space_pipe_char,
                count=0),
            dict(
                c_type='date',
                rule=DATE_REGEX,
                fix=None,
                func=self._date,
                count=0),
            dict(
                c_type='date_time',
                rule=DATE_REGEX_TIME,
                fix=None,
                func=self._date_time,
                count=0),
            dict(
                c_type='int',
                rule=INT_REGEX,
                fix=None,
                func=self._int,
                count=0),
            dict(
                c_type='float',
                rule=FLOAT_REGEX,
                fix=None,
                func=self._float,
                count=0),
            dict(
                c_type='percent',
                rule=PERCENT_REGEX,
                fix=None,
                func=self._percent,
                count=0),
            dict(
                c_type='pound',
                rule=POUND_REGEX,
                fix=None,
                func=self._pound,
                count=0)
        ]
        self.checks_l = len(self._checks)
        self._analyse()

    def _sort_checks(self) -> None:
        """
        Sorts the list of dicts in self._checks by their count, highest
        first, so that when the fix methods run down them, they always have
        a count with a value higher than 0 to run with, otherwise later
        fixes might not get hit.
        """
        self._checks = sorted(
            self._checks, key=itemgetter('count'), reverse=True)

    def _endash(self, regex: str, fix: str) -> str:
        """
        Turns – into -.
        """
        return re.sub(regex, fix, self.string)

    def _pound(self, regex: str, fix: str) -> float:
        """
        Turns £12.24 into 12.24 (a float).
        """
        m = re.match(regex, self.string)
        sum_p = m.group(2)
        if m.group(1) == "-":
            return float(sum_p) * -1
        else:
            return float(sum_p)

    def _percent(self, regex: str, fix: str) -> float:
        """
        Turns 100% into 1.0.
        """
        m = re.match(regex, self.string)
        p = int(m.group(1))
        return p / 100

    def _float(self, regex: str, fix: str) -> float:
        """
        Turns numbers that look like floats into floats.
        """
        return float(self.string)

    def _int(self, regex: str, fix: str) -> int:
        """
        Turns numbers that look like integers into integers.
        """
        return int(self.string)

    def _date(self, regex: str, fix: str) -> Union[datetime, str]:
        """
        Handles dates in "03/05/2016" format.
        """
        m = re.match(regex, self.string)
        if int(m.groups()[-1]) in range(1965, 1967):
            print(("Dates inputted as dd/mm/65 will migrate as dd/mm/2065. "
                   "Dates inputted as dd/mm/66 will migrate as dd/mm/1966."))
        try:
            return parse(m.string, dayfirst=True)
        except ValueError:
            print("This date is causing problems: {}".format(self.string))
            return self.string

    def _date_time(self, regex: str, fix: str) -> Union[date, str]:
        """
        Handles dates in "2017-05-01 0:00:00" format. We get this from the
        csv file when we send it back out to templates/forms. Returns a Python
        date object.
        """
        m = re.match(regex, self.string)
        year = int(m.group(1))
        month = int(m.group(3))
        day = int(m.group(5))
        try:
            return date(year, month, day)
        except ValueError:
            print("Incorrect date format {}!".format(self.string))
            return self.string

    def _commas(self, regex: str, fix: str) -> str:
        """
        Handles commas in self.string according to rule in self._checks
        """
        # we want to sort the list first so self._checks has any item
        # with a count > 0 up front, otherwise if a count of 0 appears
        # before it in the list, the > 0 count never gets fixed
        return re.sub(regex, fix, self.string)

    def _apostrophe(self, regex: str, fix: str) -> str:
        """Handles apostrophes as first char of the string."""
        return self.string.lstrip('\'')

    def _newline(self, regex: str, fix: str) -> str:
        """Handles newlines anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _doublespace(self, regex: str, fix: str) -> str:
        """Handles double-spaces anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _space_pipe_char(self, regex: str, fix: str) -> str:
        """Handles space pipe char anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _access_checks(self, c_type: str) -> int:
        """Helper method returns the index of rule in self._checks
        when given a c_type"""
        return self._checks.index(next(
            item for item in self._checks if item['c_type'] == c_type))

    def _analyse(self) -> None:
        """
        Uses the self._checks table as a basis for counting the number of
        each cleaning target required, and calling the appropriate method
        to clean.
        """
        i = 0
        while i < self.checks_l:
            try:
                matches = re.finditer(self._checks[i]['rule'], self.string)
                if matches:
                    self._checks[i]['count'] += len(list(matches))
                i += 1
            except TypeError:
                i += 1

    def clean(self) -> str:
        """Runs each applicable cleaning action and returns the cleaned
        string."""
        self._sort_checks()
        for check in self._checks:
            if check['count'] > 0:
                self.string = check['func'](
                    check['rule'], check['fix'])
                check['count'] = 0
            else:
                return self.string
        return self.string
