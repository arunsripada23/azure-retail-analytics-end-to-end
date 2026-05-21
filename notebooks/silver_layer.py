# Silver Layer - Data Cleaning & Transformation

from pyspark.sql.functions import col, datediff

spark.conf.set(
    "fs.azure.account.key.stlakehousearun.dfs.core.windows.net",
    "YOUR_STORAGE_ACCOUNT_KEY"
)

# =========================
# READ BRONZE TABLES
# =========================

customers = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/customers/"
)

orders = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/orders/"
)

payments = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/payments/"
)

order_items = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/order_items/"
)

sellers = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/sellers/"
)

# =========================
# CLEAN ORDERS
# =========================

silver_orders = orders \
    .withColumn(
        "order_purchase_timestamp",
        col("order_purchase_timestamp").cast("timestamp")
    ) \
    .withColumn(
        "order_delivered_customer_date",
        col("order_delivered_customer_date").cast("timestamp")
    ) \
    .withColumn(
        "order_estimated_delivery_date",
        col("order_estimated_delivery_date").cast("timestamp")
    ) \
    .withColumn(
        "delivery_delay_days",
        datediff(
            col("order_delivered_customer_date"),
            col("order_estimated_delivery_date")
        )
    )

# =========================
# CLEAN PAYMENTS
# =========================

silver_payments = payments.withColumn(
    "payment_value",
    col("payment_value").cast("double")
)

# =========================
# CLEAN CUSTOMERS
# =========================

silver_customers = customers.select(
    "customer_id",
    "customer_city",
    "customer_state"
)

# =========================
# CLEAN SELLERS
# =========================

silver_sellers = sellers.select(
    "seller_id",
    "seller_city",
    "seller_state"
)

# =========================
# WRITE SILVER TABLES
# =========================

silver_orders.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/orders/"
    )

silver_payments.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/payments/"
    )

silver_customers.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/customers/"
    )

silver_sellers.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/sellers/"
    )