import uuid
from datetime import UTC, datetime
from enum import Enum


class VehicleType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    COMPACT = "COMPACT"
    SUV = "SUV"
    TRUCK = "TRUCK"


class SpotType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    COMPACT = "COMPACT"
    LARGE = "LARGE"


class TicketStatus(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"


class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type


class ParkingSpot:
    def __init__(self, spot_id: str, floor_number: int, spot_type: SpotType):
        self.spot_id = spot_id
        self.floor_number = floor_number
        self.spot_type = spot_type
        self.is_occupied: bool = False

    def occupy(self) -> None:
        self.is_occupied = True

    def vacate(self) -> None:
        self.is_occupied = False


class Ticket:
    def __init__(self, spot_id: str, license_plate: str):
        self.ticket_id: str = str(uuid.uuid4())
        self.spot_id: str = spot_id
        self.license_plate: str = license_plate
        self.entry_time: datetime = datetime.now(UTC)
        self.status: TicketStatus = TicketStatus.ACTIVE

    def mark_paid(self) -> None:
        self.status = TicketStatus.PAID
