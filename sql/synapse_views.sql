-- ============================================
-- Brazilian E-Commerce Analytics
-- Synapse Serverless SQL Views
-- ============================================

-- ============================================
-- DIM SELLER VIEW
-- ============================================

CREATE OR ALTER VIEW vw_dim_seller AS
SELECT *
FROM OPENROWSET(
    BULK 'https://stlakehousearun.dfs.core.windows.net/retail-lakehouse/gold/dim_seller/',
    FORMAT = 'DELTA'
) AS rows;

-- ============================================
-- DIM CUSTOMER VIEW
-- ============================================

CREATE OR ALTER VIEW vw_dim_customer AS
SELECT *
FROM OPENROWSET(
    BULK 'https://stlakehousearun.dfs.core.windows.net/retail-lakehouse/gold/dim_customer/',
    FORMAT = 'DELTA'
) AS rows;

-- ============================================
-- FACT ORDERS VIEW
-- ============================================

CREATE OR ALTER VIEW vw_fact_orders AS
SELECT *
FROM OPENROWSET(
    BULK 'https://stlakehousearun.dfs.core.windows.net/retail-lakehouse/gold/fact_orders/',
    FORMAT = 'DELTA'
) AS rows;