from classes import Direction, ElevatorController
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Elevator System Control API")
controller = ElevatorController(num_elevators=3, total_floors=20)


class ExternalCallRequest(BaseModel):
    floor: int
    direction: Direction


class InternalSelectRequest(BaseModel):
    elevator_id: int
    floor: int


class MaintenanceRequest(BaseModel):
    elevator_id: int
    in_maintenance: bool


@app.post("/api/v1/elevators/call")
def external_call(req: ExternalCallRequest):
    assigned_id = controller.call_elevator(req.floor, req.direction)
    return {"message": "Elevator dispatched", "assigned_elevator_id": assigned_id}


@app.post("/api/v1/elevators/select")
def internal_select(req: InternalSelectRequest):
    controller.select_internal_floor(req.elevator_id, req.floor)
    return {"message": f"Floor {req.floor} queued for Elevator {req.elevator_id}"}


@app.post("/api/v1/elevators/step")
def step_simulation():
    """Simulates one time-tick across all elevators."""
    for elevator in controller.elevators:
        elevator.step()
    return {"status": "Simulation stepped 1 tick forward"}


@app.get("/api/v1/elevators/status")
def get_status():
    return [
        {
            "id": e.elevator_id,
            "current_floor": e.current_floor,
            "direction": e.direction,
            "state": e.state,
            "door_status": e.door_status,
            "up_queue": e.up_min_heap,
            "down_queue": [-f for f in e.down_max_heap],
        }
        for e in controller.elevators
    ]


@app.post("/api/v1/admin/maintenance")
def set_maintenance(req: MaintenanceRequest):
    controller.set_maintenance(req.elevator_id, req.in_maintenance)
    return {
        "message": f"Elevator {req.elevator_id} maintenance mode set to {req.in_maintenance}"
    }


if __name__ == "__main__":
    # Initialize 3 elevators
    sys_controller = ElevatorController(num_elevators=3, total_floors=20)

    print("--- 1. External Call: Floor 5 going UP ---")
    assigned = sys_controller.call_elevator(floor=5, direction=Direction.UP)
    print(f"Assigned Elevator: {assigned}")

    print("--- 2. Internal Request: Passenger inside presses Floor 10 ---")
    sys_controller.select_internal_floor(elevator_id=assigned, floor=10)

    print("--- 3. Stepping Simulation until arrival ---")
    car = sys_controller.elevators[assigned]
    for _ in range(12):
        car.step()
        print(
            f"Floor: {car.current_floor} | Dir: {car.direction.value} | State: {car.state.value} | Doors: {car.door_status.value}"
        )
