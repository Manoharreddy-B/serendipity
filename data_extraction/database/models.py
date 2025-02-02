from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

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
    name = Column(String(5), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

class PortfolioTable(Base):
    __tablename__ = "portfoliotable"

    uid = Column(Integer, ForeignKey("usertable.uid", ondelete="CASCADE"), primary_key=True)
    sid = Column(Integer, ForeignKey("stocktable.sid", ondelete="CASCADE"), primary_key=True)
    qty = Column(Integer, nullable=False)

class TransactionTable(Base):
    __tablename__ = "transactiontable"

    tid = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey("usertable.uid"))
    sid = Column(Integer, ForeignKey("stocktable.sid"))
    typ = Column(String(5), nullable=False) 
    qty = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'tid' : self.tid,
            'uid' : self.uid,
            'sid' : self.sid,
            'qty' : self.qty,
            'timestamp' : self.timestamp
        }