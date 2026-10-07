import heapq
import threading
from enum import Enum

from fastapi import HTTPException

# --- Enums ---


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class ElevatorState(str, Enum):
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    MAINTENANCE = "MAINTENANCE"


class DoorStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


# --- Domain Models ---


class ElevatorCar:
    def __init__(self, elevator_id: int, total_floors: int = 20):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.current_floor: int = 0
        self.direction: Direction = Direction.IDLE
        self.state: ElevatorState = ElevatorState.STOPPED
        self.door_status: DoorStatus = DoorStatus.CLOSED

        # SCAN queues
        self.up_min_heap: list[int] = []  # Ascending floors for UP
        self.down_max_heap: list[int] = []  # Descending floors for DOWN (-floor)
        self._lock = threading.Lock()

    def add_floor_request(self, floor: int) -> bool:
        """Queues a floor request while guaranteeing safety rules."""
        with self._lock:
            if self.state == ElevatorState.MAINTENANCE:
                return False

            if floor == self.current_floor and self.state == ElevatorState.STOPPED:
                self.open_doors()
                return True

            if self.direction == Direction.UP:
                if floor >= self.current_floor:
                    if floor not in self.up_min_heap:
                        heapq.heappush(self.up_min_heap, floor)
                else:
                    if -floor not in self.down_max_heap:
                        heapq.heappush(self.down_max_heap, -floor)
            elif self.direction == Direction.DOWN:
                if floor <= self.current_floor:
                    if -floor not in self.down_max_heap:
                        heapq.heappush(self.down_max_heap, -floor)
                else:
                    if floor not in self.up_min_heap:
                        heapq.heappush(self.up_min_heap, floor)
            else:  # IDLE
                if floor > self.current_floor:
                    self.direction = Direction.UP
                    heapq.heappush(self.up_min_heap, floor)
                elif floor < self.current_floor:
                    self.direction = Direction.DOWN
                    heapq.heappush(self.down_max_heap, -floor)
                else:
                    self.open_doors()
                self.state = ElevatorState.MOVING
            return True

    def open_doors(self) -> None:
        """Doors can ONLY open if elevator is standing on a floor."""
        if self.state == ElevatorState.STOPPED or self.direction == Direction.IDLE:
            self.door_status = DoorStatus.OPEN

    def close_doors(self) -> None:
        self.door_status = DoorStatus.CLOSED

    def step(self) -> None:
        """Simulates one floor step of movement."""
        with self._lock:
            if self.state == ElevatorState.MAINTENANCE:
                return

            self.close_doors()

            if self.direction == Direction.UP:
                if self.up_min_heap:
                    self.state = ElevatorState.MOVING
                    self.current_floor += 1
                    if self.up_min_heap[0] == self.current_floor:
                        heapq.heappop(self.up_min_heap)
                        self.state = ElevatorState.STOPPED
                        self.open_doors()
                elif self.down_max_heap:
                    self.direction = Direction.DOWN
                else:
                    self.direction = Direction.IDLE
                    self.state = ElevatorState.STOPPED

            elif self.direction == Direction.DOWN:
                if self.down_max_heap:
                    self.state = ElevatorState.MOVING
                    self.current_floor -= 1
                    if -self.down_max_heap[0] == self.current_floor:
                        heapq.heappop(self.down_max_heap)
                        self.state = ElevatorState.STOPPED
                        self.open_doors()
                elif self.up_min_heap:
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.IDLE
                    self.state = ElevatorState.STOPPED


# --- Dispatcher Strategy Pattern ---


class ElevatorDispatcher:
    def select_best_elevator(
        self, elevators: list[ElevatorCar], floor: int, direction: Direction
    ) -> ElevatorCar | None:
        best_elevator = None
        min_distance = float("inf")

        for elevator in elevators:
            if elevator.state == ElevatorState.MAINTENANCE:
                continue

            distance = abs(elevator.current_floor - floor)

            # Preference 1: Elevator moving in same direction and hasn't passed floor yet
            if elevator.direction == direction:
                if (
                    (direction == Direction.UP and elevator.current_floor <= floor)
                    or (direction == Direction.DOWN and elevator.current_floor >= floor)
                ) and distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator

            # Preference 2: IDLE Elevator
            elif elevator.direction == Direction.IDLE and distance < min_distance:
                min_distance = distance
                best_elevator = elevator

        # Fallback: Pick any non-maintenance elevator with the shortest distance
        if not best_elevator:
            active_elevators = [
                e for e in elevators if e.state != ElevatorState.MAINTENANCE
            ]
            if active_elevators:
                best_elevator = min(
                    active_elevators, key=lambda e: abs(e.current_floor - floor)
                )

        return best_elevator


# --- System Controller ---


class ElevatorController:
    def __init__(self, num_elevators: int = 3, total_floors: int = 20):
        self.elevators = [ElevatorCar(i, total_floors) for i in range(num_elevators)]
        self.dispatcher = ElevatorDispatcher()

    def call_elevator(self, floor: int, direction: Direction) -> int:
        best_elevator = self.dispatcher.select_best_elevator(
            self.elevators, floor, direction
        )
        if not best_elevator:
            raise HTTPException(
                status_code=503, detail="No available elevators in service."
            )
        best_elevator.add_floor_request(floor)
        return best_elevator.elevator_id

    def select_internal_floor(self, elevator_id: int, floor: int) -> None:
        if elevator_id < 0 or elevator_id >= len(self.elevators):
            raise HTTPException(status_code=404, detail="Elevator ID not found.")
        self.elevators[elevator_id].add_floor_request(floor)

    def set_maintenance(self, elevator_id: int, in_maintenance: bool) -> None:
        if elevator_id < 0 or elevator_id >= len(self.elevators):
            raise HTTPException(status_code=404, detail="Elevator ID not found.")
        car = self.elevators[elevator_id]
        car.state = (
            ElevatorState.MAINTENANCE if in_maintenance else ElevatorState.STOPPED
        )
