from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pylan.schedule import keep_or_convert, timedelta_from_schedule, timedelta_from_str


class Projection(ABC):
    """@public
    Projection is an abstract base class with the following implementations:
    - Add(schedule, value)
    - Subtract(schedule, value)
    - Multiply(schedule, value)
    - Divide(schedule, value)
    - Replace(schedule, value)

    Note, all implementations have the following optional parameters:
    - start_date: str or datetime with the minimum date for the projection to start
    - end_date: str or datetime, max date for the projection
    - offset: str, offsets each occurence of the projection based on the start date

    >>> mortgage = Subtract("0 0 2 * *", 1500)  # cron support
    >>> inflation = Divide(["2025-1-1", "2026-1-1", "2027-1-1"], 1.08)
    """

    def __init__(
        self,
        schedule: Any,
        value: float | int,
        start_date: str | datetime = None,
        end_date: str | datetime = None,
        offset: str = None,
        include_start: bool = False,
    ) -> None:
        self.schedule = schedule
        self.value = value
        self.include_start = include_start
        self.iterations = 0
        self.dt_schedule = []
        self.projections = []

        self.start_date = start_date
        self.offset = offset
        self.end_date = end_date

        self.__backup_value = value

    @abstractmethod
    def apply(self) -> None:
        """@public
        Applies the projection to the item provided as a parameter. Implemented in the
        specific classes.
        """
        pass

    def add_projection(self, projection: Any) -> None:
        """@public
        Applies the projection to the value of this projection. E.g. You add a salary each month,
        over time this salary can grow using another projection.
        """
        self.projections.append(projection)

    def update_value(self, current: datetime) -> None:
        """@private
        Grows the value the amount of times that it was scheduled in the past.
        """
        for projection in self.projections:
            try:
                while projection.dt_schedule[projection.iterations] < current:
                    projection.apply(self)
                    projection.iterations += 1
            except IndexError:
                pass

    def scheduled(self, current: datetime) -> bool:
        """@public
        Returns true if projection is scheduled on the provided date.
        """
        if self.projections:
            self.update_value(current)
        if not self.dt_schedule:
            return False
        if self.iterations >= len(self.dt_schedule):
            return False
        if current >= self.dt_schedule[self.iterations]:
            self.iterations += 1
            return True
        return False

    def setup(self, start: datetime, end: datetime, iterative: bool = False) -> None:
        """@private
        Iterates between start and end date and returns sets the list of datetimes that
        the projection is scheduled. Note, the model is iterative for until() computes. In
        these cases the values and iterations should not be reset.
        """
        if not iterative:
            self.value = self.__backup_value
            self.iterations = 0
        start, end = self.__apply_date_settings(start, end)
        self.dt_schedule = timedelta_from_schedule(
            self.schedule, start, end, self.include_start
        )
        [projection.setup(start, end, iterative) for projection in self.projections]

    def __apply_date_settings(
        self, start: datetime, end: datetime
    ) -> tuple[datetime, datetime]:
        """@private
        Checks if the optional start/end date variables are set and returns updated value.
        """
        if self.start_date and keep_or_convert(self.start_date) > start:
            start = keep_or_convert(self.start_date)
        if self.end_date and keep_or_convert(self.end_date) < end:
            end = keep_or_convert(self.end_date)
        if self.offset:
            start += timedelta_from_str(self.offset)
        return start, end
