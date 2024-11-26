CREATE TABLE IF NOT EXISTS sp500 (
        ticker_id INT IDENTITY(1,1),
        symbol VARCHAR(10),
        Security VARCHAR(50),
        GICS_Sector VARCHAR(100),
        GICS_Sub_Industry VARCHAR(100),
        Location VARCHAR(100),
        CIK INT,
        Founded INT,
        PRIMARY KEY (ticker_id)
)

CREATE TABLE IF NOT EXISTS stock_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    open DECIMAL(10, 2) NOT NULL,
    high DECIMAL(10, 2) NOT NULL,
    low DECIMAL(10, 2) NOT NULL,
    close DECIMAL(10, 2) NOT NULL,
    volume BIGINT NOT NULL,
    dividends DECIMAL(10, 4) DEFAULT 0,
    stock_splits DECIMAL(5, 3) DEFAULT 1,
    ticker VARCHAR(10) NOT NULL,
    SMA_20 DECIMAL(10, 2),
    EMA_20 DECIMAL(10, 2),
    RSI DECIMAL(6, 2),
    MACD DECIMAL(10, 4),
    Signal DECIMAL(10, 4),
    middle_band DECIMAL(10, 2),
    std_dev DECIMAL(10, 4),
    upper_band DECIMAL(10, 2),
    lower_band DECIMAL(10, 2),
);

-- Cash Flow Statement Table
CREATE TABLE cash_flow_statement (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    operating_cash_flow DECIMAL(20, 2),
    investing_cash_flow DECIMAL(20, 2),
    financing_cash_flow DECIMAL(20, 2),
    net_change_in_cash DECIMAL(20, 2),
    free_cash_flow DECIMAL(20, 2),
    capital_expenditures DECIMAL(20, 2),
);

-- Balance Sheet Table
CREATE TABLE balance_sheet (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    total_assets DECIMAL(20, 2),
    total_liabilities DECIMAL(20, 2),
    total_equity DECIMAL(20, 2),
    cash_and_equivalents DECIMAL(20, 2),
    short_term_investments DECIMAL(20, 2),
    net_receivables DECIMAL(20, 2),
    inventory DECIMAL(20, 2),
    long_term_investments DECIMAL(20, 2),
    property_plant_equipment DECIMAL(20, 2),
    total_current_assets DECIMAL(20, 2),
    total_current_liabilities DECIMAL(20, 2),
    long_term_debt DECIMAL(20, 2),
);