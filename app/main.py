from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

# from .database import Database
from .database.models import Shipment, ShipmentStatus
from .database.session import SessionDep, create_db_tables
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment


@app.post("/shipment")
def submip_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, updated_shipment: ShipmentUpdate, session: SessionDep):
    updated = updated_shipment.model_dump(exclude_none=True)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided."
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(updated)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    session.delete(session.get(Shipment, id))
    session.commit()
    return {"detail": f"shipment with id: {id} is deleted"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
