SELECT 
    u.UID, 
    u.Name, 
    u.Email, 
    s.SID AS Stock_Price,
    p.Qty AS Number_Of_Stocks,
    (s.Price * p.Qty) AS Stock_Value
FROM 
    UserTable u
JOIN 
    PortfolioTable p ON u.UID = p.UID
JOIN 
    StockTable s ON p.SID = s.SID
WHERE 
    u.UID = :uid;  -- Replace :uid with the specific user's UID
-- SELECT *
-- FROM StockTable;

-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema = 'public';



