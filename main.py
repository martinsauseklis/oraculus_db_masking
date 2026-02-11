from dotenv import load_dotenv
from sqlalchemy import create_engine, text, select, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from cryptography.fernet import Fernet
import os

key = Fernet.generate_key()
cipher_suite = Fernet(key)

"""Needs to be setup in a way that allows specific table names to be entered??"""
load_dotenv()

DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")


class Base(DeclarativeBase):
    pass


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id: Mapped[int] = mapped_column(primary_key=True)
    tracking_number: Mapped[str] = mapped_column(String(20))
    reference_number: Mapped[str] = mapped_column(String(30))
    sender_name: Mapped[str] = mapped_column(String(30))
    sender_country: Mapped[str] = mapped_column(String(2))
    sender_city: Mapped[str] = mapped_column(String(100))
    sender_postcode: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f"Shipment(shipment_id={self.shipment_id!r}, tracking_number={self.tracking_number!r}, reference_number={self.reference_number!r}, sender_name={self.sender_name!r})"


engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)
session = Session(engine)


def main():
    stmt = select(Shipment).where(Shipment.shipment_id.in_([9]))
    result = session.scalars(stmt)
    for r in result:
        print(r.__dict__)
        encrypted = encrypt_data(r.__dict__, ["sender_name"])
        print(encrypted)


def encrypt_data(obj: dict, encryptable_keys: list[str]):
    result = {}
    for key in obj.keys():
        if key in encryptable_keys:
            # result[key] = cipher_suite.encrypt(bytes(obj[key], "utf-8"))
            result[key] = f"<{key}>"
        else:
            result[key] = obj[key]

    return result


if __name__ == "__main__":
    main()
