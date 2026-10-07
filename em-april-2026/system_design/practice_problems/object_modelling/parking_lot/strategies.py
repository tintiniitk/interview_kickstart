import math
from abc import ABC, abstractmethod
from datetime import datetime

from models import Ticket


class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket, exit_time: datetime) -> float:
        pass


class HourlyFeeStrategy(FeeStrategy):
    def __init__(self, hourly_rate: float = 10.0):
        self.hourly_rate = hourly_rate

    def calculate_fee(self, ticket: Ticket, exit_time: datetime) -> float:
        duration = exit_time - ticket.entry_time
        hours = math.ceil(max(duration.total_seconds() / 3600, 1.0))
        return hours * self.hourly_rate
