from fastapi import FastAPI, HTTPException
from models import ParkingSpot, SpotType, Vehicle, VehicleType
from parking_lot import ParkingLot
from pydantic import BaseModel
from strategies import HourlyFeeStrategy

app = FastAPI(title="Parking Lot Management API")

# Initialize Singleton Parking Lot instance
lot = ParkingLot(lot_id="LOT-01", fee_strategy=HourlyFeeStrategy(hourly_rate=10.0))

# Pre-populate spots
lot.add_spot(ParkingSpot("SPOT-101", floor_number=1, spot_type=SpotType.COMPACT))
lot.add_spot(ParkingSpot("SPOT-102", floor_number=1, spot_type=SpotType.LARGE))


class ParkVehicleRequest(BaseModel):
    license_plate: str
    vehicle_type: VehicleType


class ExitVehicleRequest(BaseModel):
    ticket_id: str


@app.post("/api/v1/lots/park")
def park_vehicle(req: ParkVehicleRequest):
    try:
        vehicle = Vehicle(
            license_plate=req.license_plate, vehicle_type=req.vehicle_type
        )
        ticket = lot.park_vehicle(vehicle)
        return {
            "message": "Vehicle parked successfully",
            "ticket_id": ticket.ticket_id,
            "spot_id": ticket.spot_id,
            "entry_time": ticket.entry_time,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/lots/exit")
def exit_vehicle(req: ExitVehicleRequest):
    try:
        total_fee = lot.process_exit(req.ticket_id)
        return {
            "message": "Vehicle exited successfully",
            "ticket_id": req.ticket_id,
            "total_fee_due": total_fee,
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    # Local CLI execution verification
    v = Vehicle("MH-12-AB-1234", VehicleType.SUV)
    t = lot.park_vehicle(v)
    print(f"[CLI Demo] Vehicle Parked | Ticket ID: {t.ticket_id}")
    fee = lot.process_exit(t.ticket_id)
    print(f"[CLI Demo] Vehicle Exited | Total Fee: ${fee}")
