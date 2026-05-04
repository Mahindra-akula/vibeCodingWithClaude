from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Read raw tables
bookings = spark.table("claudecatalog.raw.bookings")
airports = spark.table("claudecatalog.raw.airports")

# Join bookings with airports on airport_id
bookings_airports = bookings.join(airports, on="airport_id", how="inner")

# Write to silver schema as a Delta table
(
    bookings_airports.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("claudecatalog.silver.bookings_airports")
)

print("Successfully created claudecatalog.silver.bookings_airports")
print(f"Row count: {spark.table('claudecatalog.silver.bookings_airports').count()}")
