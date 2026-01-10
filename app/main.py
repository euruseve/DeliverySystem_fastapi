from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database import Database
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()

db = Database()


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment


@app.post("/shipment")
def submip_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)

    return {"id": new_id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    updated = db.update(id, shipment)
    return updated


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"detail": f"shipment with id: {id} is deleted"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
