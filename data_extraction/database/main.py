from . import models
from .session_utils import DBSessionManager
from .utils import convert_transaction_to_list
from typing import List


def add_stock_to_portfolio(uid: int, sid: int, quantity: int):
    # quantity > 0 means we want to add stocks
    with DBSessionManager() as db:
        # 1. Check if user exists
        user = db.query(models.UserTable).filter(models.UserTable.uid == uid).first()
        if not user:
            raise ValueError(f"User {uid} does not exist.")

        # 2. Check if stock exists
        stock = db.query(models.StockTable).filter(models.StockTable.sid == sid).first()
        if not stock:
            raise ValueError(f"Stock {sid} does not exist.")

        # 3. Check if a portfolio row already exists
        portfolio_entry = (
            db.query(models.PortfolioTable)
            .filter(models.PortfolioTable.uid == uid, models.PortfolioTable.sid == sid)
            .first()
        )

        # 4. Insert or update
        if portfolio_entry:
            portfolio_entry.qty += quantity
        else:
            new_portfolio = models.PortfolioTable(uid=uid, sid=sid, qty=quantity)
            db.add(new_portfolio)

        # 5. The `DBSessionManager` context will commit automatically
        #    if no exceptions are raised before exiting.

def get_portfolio(uid: int):
    """Example read operation: get the user's entire portfolio."""
    with DBSessionManager() as db:
        user_portfolio = (
            db.query(models.PortfolioTable)
            .filter(models.PortfolioTable.uid == uid)
            .all()
        )
        return user_portfolio

def get_transaction(uid: List[int]):
    """"""
    with DBSessionManager() as db:
        transactions = (
            db.query(
            models.UserTable.uid,
            models.UserTable.name.label('uname'),
            models.UserTable.email,
            models.TransactionTable.sid,
            models.StockTable.name.label('sname'),
            models.TransactionTable.qty,
            models.TransactionTable.typ,
            models.TransactionTable.qty*models.StockTable.price.label('value')
            ).join(
                models.StockTable, models.TransactionTable.sid == models.StockTable.sid
            ).join(
                models.UserTable, models.TransactionTable.uid == models.UserTable.uid
            ).filter(
                models.TransactionTable.uid.in_(uid)
            ).order_by(
                models.UserTable.uid
            )
            .all()
        )
        
        result = convert_transaction_to_list(transactions)
        return result


