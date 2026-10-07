```
+------------------------------------+          +------------------------------------+
|            ParkingLot              | 1      * |             ParkingFloor           |
+------------------------------------+----------+------------------------------------+
| - lot_id: String                   |          | - floor_number: int                |
| - name: String                     |          | - spots: Map<SpotType, Set<Spot>>  |
| - floors: List<ParkingFloor>       |          +------------------------------------+
+------------------------------------+          | + find_available_spot(type): Spot  |
| + assign_spot(vehicle): Ticket     |          +------------------------------------+
| + process_exit(ticket_id): Invoice |                            | 1
+------------------------------------+                            |
                                                                  | *
+------------------------------------+          +------------------------------------+
|             Ticket                 |          |            ParkingSpot             |
+------------------------------------+          +------------------------------------+
| - ticket_id: String                |          | - spot_id: String                  |
| - spot_id: String                  |          | - floor_number: int                |
| - vehicle_license: String          |          | - spot_type: SpotType              |
| - entry_time: LocalDateTime        |          | - is_occupied: boolean             |
| - status: TicketStatus             |          +------------------------------------+
+------------------------------------+          | + occupy(): void                   |
                                                | + vacate(): void                   |
+------------------------------------+          +------------------------------------+
|            FeeStrategy             |                            ^
|            <<interface>>           |                            |
+------------------------------------+                   +-----------------+
| + calculate_fee(ticket): double    |                   |  Handicapped /  |
+------------------------------------+                   | Compact / Large |
                  ^                                      +-----------------+
                  |
     +------------+------------+
     |                         |
+-------------------+ +-------------------+
| FlatRateStrategy  | | HourlyFeeStrategy |
+-------------------+ +-------------------+
```