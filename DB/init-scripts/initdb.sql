-- PostgreSQL Initialization File for Schema

-- User Table
CREATE TABLE UserTable (
    UID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL UNIQUE,
    DOB DATE NOT NULL,
    PhoneNo VARCHAR(15) NOT NULL UNIQUE
);

-- Stock Table
CREATE TABLE StockTable (
    SID SERIAL PRIMARY KEY,
    Name VARCHAR(5) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Portfolio Table
CREATE TABLE PortfolioTable (
    UID INT NOT NULL,
    SID INT NOT NULL,
    Qty INT NOT NULL,
    PRIMARY KEY (UID, SID),
    FOREIGN KEY (UID) REFERENCES UserTable(UID) ON DELETE CASCADE,
    FOREIGN KEY (SID) REFERENCES StockTable(SID) ON DELETE CASCADE
);

-- Transaction Table
CREATE TABLE TransactionTable (
    TID SERIAL PRIMARY KEY,
    UID INT NOT NULL,
    SID INT NOT NULL,
    Typ VARCHAR(5) NOT NULL,
    Qty INT NOT NULL,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO UserTable (Name, Email, DOB, PhoneNo) VALUES
('Alice Smith', 'alice.smith@example.com', '1990-01-15', '555-1234'),
('Bob Johnson', 'bob.johnson@example.com', '1985-03-22', '555-5678'),
('Charlie Brown', 'charlie.brown@example.com', '1992-06-11', '555-8765'),
('David White', 'david.white@example.com', '1987-09-30', '555-4321'),
('Eve Black', 'eve.black@example.com', '1993-02-20', '555-1357'),
('Frank Green', 'frank.green@example.com', '1990-08-25', '555-2468'),
('Grace Blue', 'grace.blue@example.com', '1988-12-04', '555-3697'),
('Hannah Red', 'hannah.red@example.com', '1991-07-19', '555-1478'),
('Ian Purple', 'ian.purple@example.com', '1989-11-12', '555-2589'),
('Jack Yellow', 'jack.yellow@example.com', '1994-04-01', '555-3695');

INSERT INTO StockTable (Name, Price) VALUES
('ABC', 100.50),
('DEF', 250.75),
('GHI', 300.30),
('JKL', 150.20),
('MNO', 500.10);

INSERT INTO PortfolioTable (UID, SID, Qty) VALUES
(1, 1, 50),
(1, 2, 30),
(2, 1, 10),
(2, 3, 25),
(3, 2, 100),
(3, 4, 15),
(4, 5, 10),
(5, 3, 60),
(6, 4, 20),
(7, 1, 40),
(8, 2, 15),
(9, 3, 30),
(10, 5, 25);

INSERT INTO TransactionTable (UID, SID, Typ, Qty) VALUES
(1, 1, 'BUY', 10),
(1, 2, 'BUY', 20),
(2, 3, 'SELL', 15),
(2, 1, 'SELL', 5),
(3, 4, 'BUY', 10),
(3, 2, 'SELL', 50),
(4, 5, 'SELL', 5),
(4, 3, 'BUY', 10),
(5, 4, 'SELL', 30),
(5, 1, 'BUY', 20),
(6, 2, 'SELL', 40),
(6, 5, 'BUY', 10),
(7, 1, 'SELL', 10),
(7, 4, 'BUY', 15),
(8, 3, 'SELL', 10),
(8, 2, 'BUY', 5),
(9, 1, 'SELL', 30),
(9, 5, 'SELL', 20),
(10, 2, 'BUY', 10),
(10, 3, 'SELL', 5);


