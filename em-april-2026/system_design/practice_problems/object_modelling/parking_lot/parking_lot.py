import threading
from collections import deque
from datetime import UTC, datetime

from models import ParkingSpot, SpotType, Ticket, Vehicle, VehicleType
from strategies import FeeStrategy


class ParkingLot:
    def __init__(self, lot_id: str, fee_strategy: FeeStrategy):
        self.lot_id = lot_id
        self.fee_strategy = fee_strategy

        # O(1) spot allocation data structures
        self.available_spots: dict[SpotType, deque[ParkingSpot]] = {
            st: deque() for st in SpotType
        }
        self.active_spot_map: dict[str, ParkingSpot] = {}
        self.active_tickets: dict[str, Ticket] = {}
        self._lock = threading.Lock()

    def add_spot(self, spot: ParkingSpot) -> None:
        with self._lock:
            self.available_spots[spot.spot_type].append(spot)
            self.active_spot_map[spot.spot_id] = spot

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        required_type = self._map_vehicle_to_spot_type(vehicle.type)

        with self._lock:
            spot_queue = self.available_spots.get(required_type)
            if not spot_queue:
                raise ValueError(
                    f"No available spots for vehicle type: {vehicle.type.value}"
                )

            spot = spot_queue.popleft()
            spot.occupy()

            ticket = Ticket(spot_id=spot.spot_id, license_plate=vehicle.license_plate)
            self.active_tickets[ticket.ticket_id] = ticket
            return ticket

    def process_exit(self, ticket_id: str) -> float:
        with self._lock:
            ticket = self.active_tickets.pop(ticket_id, None)
            if not ticket:
                raise KeyError("Invalid or non-existent Ticket ID.")

            spot = self.active_spot_map[ticket.spot_id]
            spot.vacate()
            self.available_spots[spot.spot_type].append(spot)

            ticket.mark_paid()
            return self.fee_strategy.calculate_fee(ticket, datetime.now(UTC))

    @staticmethod
    def _map_vehicle_to_spot_type(vehicle_type: VehicleType) -> SpotType:
        mapping = {
            VehicleType.MOTORCYCLE: SpotType.MOTORCYCLE,
            VehicleType.COMPACT: SpotType.COMPACT,
            VehicleType.SUV: SpotType.LARGE,
            VehicleType.TRUCK: SpotType.LARGE,
        }
        return mapping[vehicle_type]
