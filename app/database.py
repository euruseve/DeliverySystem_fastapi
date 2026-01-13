import sqlite3
from contextlib import contextmanager
from typing import Any

from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    # def __enter__(self):
    #     self.connect_to_db()
    #     self.create_table()

    #     return self

    # def __exit__(self, *args):
    #     self.close()

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

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


@contextmanager
def managed_db():
    db = Database()

    db.connect_to_db()
    db.create_table()

    yield db

    db.close()


with managed_db() as db:
    print(db.get(1))
    print(db.get(2))
