from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Read raw tables
bookings = spark.table("claudecatalog.raw.bookings")
passengers = spark.table("claudecatalog.raw.passengers")

# Join bookings with passengers on passenger_id
bookings_passengers = bookings.join(passengers, on="passenger_id", how="inner")

# Write to silver schema as a Delta table
(
    bookings_passengers.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("claudecatalog.silver.bookings_passengers")
)

print("Successfully created claudecatalog.silver.bookings_passengers")
print(f"Row count: {spark.table('claudecatalog.silver.bookings_passengers').count()}")
