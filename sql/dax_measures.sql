-- ============================================
-- POWER BI DAX MEASURES
-- ============================================

-- Revenue
Revenue =
SUM(fact_orders[payment_value])

-- Total Orders
Total Orders =
DISTINCTCOUNT(fact_orders[order_id])

-- Total Customers
Total Customers =
DISTINCTCOUNT(fact_orders[customer_id])

-- Total Sellers
Total Sellers =
DISTINCTCOUNT(fact_orders[seller_id])

-- Avg Revenue Per Order
Avg Revenue Per Order =
DIVIDE(
    [Revenue],
    [Total Orders]
)

-- Cancelled Orders
Cancelled Orders =
CALCULATE(
    [Total Orders],
    fact_orders[order_status] = "canceled"
)

-- Cancelled %
Cancelled % =
DIVIDE(
    [Cancelled Orders],
    [Total Orders]
)

-- Delivered Orders
Delivered Orders =
CALCULATE(
    [Total Orders],
    fact_orders[order_status] = "delivered"
)

-- Delivered %
Delivered % =
DIVIDE(
    [Delivered Orders],
    [Total Orders]
)

-- Avg Delay
Avg Delay =
AVERAGE(fact_orders[delivery_delay_days])

-- Max Delay
Max Delay =
MAX(fact_orders[delivery_delay_days])

-- Min Delay
Min Delay =
MIN(fact_orders[delivery_delay_days])

-- On Time Deliveries
On Time Deliveries =
CALCULATE(
    [Total Orders],
    fact_orders[delivery_delay_days] <= 0
)

-- Late Deliveries
Late Deliveries =
CALCULATE(
    [Total Orders],
    fact_orders[delivery_delay_days] > 0
)

-- Delivery Success %
Delivery Success % =
DIVIDE(
    [On Time Deliveries],
    [Delivered Orders]
)

-- Revenue Growth %
Revenue Growth % =
DIVIDE(
    [Revenue] - [Previous Month Revenue],
    [Previous Month Revenue]
)

-- Previous Month Revenue
Previous Month Revenue =
CALCULATE(
    [Revenue],
    DATEADD(
        Dim_Date[Date],
        -1,
        MONTH
    )
)

-- YTD Revenue
YTD Revenue =
TOTALYTD(
    [Revenue],
    Dim_Date[Date]
)

-- MTD Revenue
MTD Revenue =
TOTALMTD(
    [Revenue],
    Dim_Date[Date]
)

-- QTD Revenue
QTD Revenue =
TOTALQTD(
    [Revenue],
    Dim_Date[Date]
)

-- YoY Growth %
YoY Growth % =
DIVIDE(
    [Revenue] -
    CALCULATE(
        [Revenue],
        SAMEPERIODLASTYEAR(Dim_Date[Date])
    ),
    CALCULATE(
        [Revenue],
        SAMEPERIODLASTYEAR(Dim_Date[Date])
    )
)