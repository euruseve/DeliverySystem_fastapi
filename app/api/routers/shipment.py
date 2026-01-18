from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ShipmentServiceDep
from app.api.shemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: int, service: ShipmentServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment


@router.post("/")
async def submip_shipment(
    shipment: ShipmentCreate, service: ShipmentServiceDep
) -> Shipment:
    return await service.add(shipment)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: int, updated_shipment: ShipmentUpdate, service: ShipmentServiceDep
):
    updated = updated_shipment.model_dump(exclude_none=True)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided."
        )

    shipment = await service.update(id, updated)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"shipment with id: {id} is deleted"}
