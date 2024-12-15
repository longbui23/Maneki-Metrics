CREATE OR REPLACE TABLE `axial-sight-443417-a6.sp500.cash_flow_combined` AS
SELECT
  2020 AS year,
  *
FROM
  `axial-sight-443417-a6.sp500.cash_flow_2020`

UNION ALL

SELECT
  2021 AS year,
  *
FROM
  `axial-sight-443417-a6.sp500.cash_flow_2021`

UNION ALL

SELECT
  2022 AS year,
  *
FROM
  `axial-sight-443417-a6.sp500.cash_flow_2022`

UNION ALL

SELECT
  2023 AS year,
  *
FROM
  `axial-sight-443417-a6.sp500.cash_flow_2023`;
