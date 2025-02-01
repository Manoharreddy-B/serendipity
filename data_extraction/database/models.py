from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "usertable"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    phoneno = Column(String(15), nullable=False, unique=True)

class StockTable(Base):
    __tablename__ = "stocktable"

    sid = Column(Integer, primary_key=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)

class PortfolioTable(Base):
    __tablename__ = "portfoliotable"

    uid = Column(Integer, ForeignKey("usertable.uid", ondelete="CASCADE"), primary_key=True)
    sid = Column(Integer, ForeignKey("stocktable.sid", ondelete="CASCADE"), primary_key=True)
    qty = Column(Integer, nullable=False)
