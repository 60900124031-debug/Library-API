from abc import ABC, abstractmethod
from datetime import datetime


class FinePolicy(ABC):
    @abstractmethod
    def calculate(self, due_date: datetime, returned_at: datetime) -> int: ...


class DailyFinePolicy(FinePolicy):
    """Denda tetap per hari penuh keterlambatan."""

    def __init__(self, rate_per_day: int):
        self.rate_per_day = rate_per_day

    def calculate(self, due_date: datetime, returned_at: datetime) -> int:
        late_days = (returned_at - due_date).days
        return max(late_days, 0) * self.rate_per_day