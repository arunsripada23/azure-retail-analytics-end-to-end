# Brazilian E-Commerce Analytics
# Bronze Layer - Raw Data Ingestion

spark.conf.set(
    "fs.azure.account.key.stlakehousearun.dfs.core.windows.net",
    "YOUR_STORAGE_ACCOUNT_KEY"
)

# =========================
# READ RAW FILES
# =========================

customers = spark.read.option("header","true").csv(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/raw/olist_customers_dataset.csv"
)

orders = spark.read.option("header","true").csv(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/raw/olist_orders_dataset.csv"
)

payments = spark.read.option("header","true").csv(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/raw/olist_order_payments_dataset.csv"
)

order_items = spark.read.option("header","true").csv(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/raw/olist_order_items_dataset.csv"
)

sellers = spark.read.option("header","true").csv(
    "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/raw/olist_sellers_dataset.csv"
)

# =========================
# DISPLAY DATA
# =========================

display(customers)
display(orders)
display(payments)
display(order_items)
display(sellers)

# =========================
# WRITE BRONZE DELTA TABLES
# =========================

customers.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/customers/"
    )

orders.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/orders/"
    )

payments.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/payments/"
    )

order_items.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/order_items/"
    )

sellers.write.format("delta") \
    .mode("overwrite") \
    .save(
        "abfss://retail-lakehouse@stlakehousearun.dfs.core.windows.net/bronze/sellers/"
    )