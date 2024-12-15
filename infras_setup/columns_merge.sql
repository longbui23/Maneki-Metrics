-- Declare and initialize the array of new columns
DECLARE new_columns_2024 ARRAY<STRING>;
DECLARE new_columns_2023 ARRAY<STRING>;

-- Retrieve new columns for 2024
SET new_columns_2024 = (
  SELECT ARRAY(
    SELECT column_name
    FROM `sp500.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'balance_sheet_2024'
      AND column_name NOT IN (
          SELECT column_name
          FROM `sp500.INFORMATION_SCHEMA.COLUMNS`
          WHERE table_name = 'balance_sheet'
      )
  )
);

-- Retrieve new columns for 2023
SET new_columns_2023 = (
  SELECT ARRAY(
    SELECT column_name
    FROM `sp500.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'balance_sheet'
      AND column_name NOT IN (
          SELECT column_name
          FROM `sp500.INFORMATION_SCHEMA.COLUMNS`
          WHERE table_name = 'balance_sheet_2024'
      )
  )
);

-- Use CREATE TEMP TABLE to help with iteration
CREATE TEMP TABLE column_iterations_2024 AS
SELECT col AS column_name
FROM UNNEST(new_columns_2024) AS col;

CREATE TEMP TABLE column_iterations_2023 AS
SELECT col AS column_name
FROM UNNEST(new_columns_2023) AS col;

-- Iterate through new columns for 2024 and add them to the balance_sheet table
FOR record IN (SELECT column_name FROM column_iterations_2024) 
DO
  -- Use EXECUTE IMMEDIATE with proper string formatting
  EXECUTE IMMEDIATE FORMAT(
    "ALTER TABLE `sp500.balance_sheet` ADD COLUMN `%s` STRING", 
    record.column_name
  );
END FOR;

FOR record IN (SELECT column_name FROM column_iterations_2023) 
DO
  -- Use EXECUTE IMMEDIATE with proper string formatting
  EXECUTE IMMEDIATE FORMAT(
    "ALTER TABLE `sp500.balance_sheet_2024` ADD COLUMN `%s` STRING", 
    record.column_name
  );
END FOR;

-- Drop the temporary table
DROP TABLE column_iterations_2024;
DROP TABLE column_iterations_2023;