from models import UserTable, StockTable, PortfolioTable
from main import add_stock_to_portfolio, get_portfolio

def run_example():
    uid = 1
    sid = 3
    quantity = 10

    try:
        # Add stock to user portfolio
        add_stock_to_portfolio(uid, sid, quantity)

        # Get updated portfolio
        portfolio = get_portfolio(uid)
        print("User portfolio after update:", portfolio)

    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    run_example()
