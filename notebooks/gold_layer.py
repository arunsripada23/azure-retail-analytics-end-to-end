# Gold Layer - Business Analytics Layer

from pyspark.sql.functions import col

spark.conf.set(
    "fs.azure.account.key.stlakehousearun.dfs.core.windows.net",
    "YOUR_STORAGE_ACCOUNT_KEY"
)

# =========================
# READ SILVER TABLES
# =========================

orders = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/orders/"
)

payments = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/payments/"
)

customers = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/customers/"
)

sellers = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/silver/sellers/"
)

order_items = spark.read.format("delta").load(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/order_items/"
)

# =========================
# FACT TABLE
# =========================

fact_orders = orders.alias("o") \
    .join(
        payments.alias("p"),
        col("o.order_id") == col("p.order_id"),
        "left"
    ) \
    .join(
        order_items.alias("oi"),
        col("o.order_id") == col("oi.order_id"),
        "left"
    ) \
    .select(
        col("o.order_id").alias("order_id"),
        col("o.customer_id").alias("customer_id"),
        col("oi.seller_id").alias("seller_id"),
        col("oi.product_id").alias("product_id"),
        col("o.order_status").alias("order_status"),
        col("p.payment_value").alias("payment_value"),
        col("o.delivery_delay_days").alias("delivery_delay_days"),
        col("o.order_purchase_timestamp").alias("order_purchase_timestamp")
    )

# =========================
# DIMENSION TABLES
# =========================

dim_customer = customers.select(
    "customer_id",
    "customer_city",
    "customer_state"
)

dim_seller = sellers.select(
    "seller_id",
    "seller_city",
    "seller_state"
)

# =========================
# WRITE GOLD TABLES
# =========================

fact_orders.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/gold/fact_orders/"
    )

dim_customer.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/gold/dim_customer/"
    )

dim_seller.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/gold/dim_seller/"
    )