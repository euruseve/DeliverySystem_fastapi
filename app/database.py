import sqlite3
from typing import Any

from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def close(self):
        self.conn.close()

    def create_table(self):
        self.cur.execute(
            """
            create table if not exists shipment (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT)
            """
        )

    def create(self, shipmemt: ShipmentCreate) -> int:
        new_id = (
            self.cur.execute("select max(id) from shipment").fetchone()[0] or 0
        ) + 1

        self.cur.execute(
            """
            insert into shipment
            values (:id, :content, :weight, :status)
            """,
            {
                "id": new_id,
                **shipmemt.model_dump(),
                "status": "placed",
            },
        )

        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute(
            """
            select * from shipment
            where id = ?
            """,
            (id,),
        )

        row = self.cur.fetchone()

        return dict(zip(("id", "content", "weight", "status"), row)) if row else None

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cur.execute(
            """
            update shipment set status = :status
            where id = :id
            """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()

        result = self.get(id)
        if result is None:
            raise ValueError(f"Shipment with id {id} not found")

        return result

    def delete(self, id: int):
        self.cur.execute(
            """
            delete from shipment
            where id = ?
            """,
            (id,),
        )

        self.conn.commit()
