from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.shemas.seller import SellerCreate
from app.database.models import Seller

password_context = CryptContext(
    schemes=["sha256_crypt", "md5_crypt", "des_crypt"], deprecated="auto"
)


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            password_hash=password_context.hash(credentials.password),
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller
