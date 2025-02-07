from .models import UserTable, StockTable, PortfolioTable, TransactionTable
from .session_utils import DBSessionManager


def add_stock_to_portfolio(uid: int, sid: int, quantity: int):
    # quantity > 0 means we want to add stocks
    with DBSessionManager() as db:
        # 1. Check if user exists
        user = db.query(UserTable).filter(UserTable.uid == uid).first()
        if not user:
            raise ValueError(f"User {uid} does not exist.")

        # 2. Check if stock exists
        stock = db.query(StockTable).filter(StockTable.sid == sid).first()
        if not stock:
            raise ValueError(f"Stock {sid} does not exist.")

        # 3. Check if a portfolio row already exists
        portfolio_entry = (
            db.query(PortfolioTable)
            .filter(PortfolioTable.uid == uid, PortfolioTable.sid == sid)
            .first()
        )

        # 4. Insert or update
        if portfolio_entry:
            portfolio_entry.qty += quantity
        else:
            new_portfolio = PortfolioTable(uid=uid, sid=sid, qty=quantity)
            db.add(new_portfolio)

        # 5. The `DBSessionManager` context will commit automatically
        #    if no exceptions are raised before exiting.

def get_portfolio(uid: int):
    """Example read operation: get the user's entire portfolio."""
    with DBSessionManager() as db:
        user_portfolio = (
            db.query(PortfolioTable)
            .filter(PortfolioTable.uid == uid)
            .all()
        )
        return user_portfolio

def get_transaction(uid: int):
    """"""
    with DBSessionManager() as db:
        transactions = (
            db.query(
            UserTable.uid,
            (UserTable.name).label('uname'),
            UserTable.email,
            TransactionTable.sid,
            (StockTable.name).label('sname'),
            TransactionTable.qty,
            TransactionTable.typ,
            (TransactionTable.qty*StockTable.price).label('value')
            ).join(
                StockTable, TransactionTable.sid == StockTable.sid
            ).join(
                UserTable, TransactionTable.uid == UserTable.uid
            ).filter(
                TransactionTable.uid == uid)
            .all()
        )
        print(transactions)
        js = {
            'uid' : transactions[0].uid,
            'name' : transactions[0].uname,
            'email' : transactions[0].email,
            'stocks' : []
        }
        for uid, uname, email, sid, sname, qty, typ, value in transactions:
            transaction = (
                sname,
                qty,
                typ,
                value,
            )
            print(type(transaction))
            js['stocks'].append(transaction)
        return js

def get_user(uid: int):
    with DBSessionManager() as db:
        user = db.query(UserTable).filter(UserTable.uid == uid).first()
        print(user)
        js = {
            'uid' : user.uid,
            'name' : user.name,
            'email' : user.email
        }
        return js


