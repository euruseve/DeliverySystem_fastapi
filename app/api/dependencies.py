from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oath2_scheme
from app.database.models import Seller
from app.database.session import get_session
from app.servises.seller import SellerService
from app.servises.shipment import ShipmentService
from app.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]


def get_seller_service(session: SessionDep):
    return SellerService(session)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]


def get_access_token(
    token: Annotated[str, Depends(oath2_scheme)], session: SessionDep
) -> dict:
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    return data


async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep
):
    return await session.get(Seller, token_data["user"]["id"])


SellerDep = Annotated[Seller, Depends(get_current_seller)]
