from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format, to_date, count, sum as _sum

spark = SparkSession.builder.getOrCreate()

# Read silver table
bookings_airports = spark.table("claudecatalog.silver.bookings_airports")

# Aggregate bookings by airport and month
bookings_by_airport = (
    bookings_airports
    .withColumn("booking_month", date_format(to_date("booking_date"), "yyyy-MM"))
    .groupBy("airport_id", "airport_name", "city", "country", "booking_month")
    .agg(
        count("booking_id").alias("total_bookings"),
        _sum("amount").alias("total_amount")
    )
    .orderBy("airport_name", "booking_month")
)

# Write to gold schema as a Delta table
(
    bookings_by_airport.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("claudecatalog.gold.bookings_by_airport")
)

print("Successfully created claudecatalog.gold.bookings_by_airport")
print(f"Row count: {spark.table('claudecatalog.gold.bookings_by_airport').count()}")
