from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format, to_date, count, sum as _sum

spark = SparkSession.builder.getOrCreate()

# Read silver table
bookings_passengers = spark.table("claudecatalog.silver.bookings_passengers")

# Aggregate bookings by month and gender
bookings_by_gender = (
    bookings_passengers
    .withColumn("booking_month", date_format(to_date("booking_date"), "yyyy-MM"))
    .groupBy("booking_month", "gender")
    .agg(
        count("booking_id").alias("total_bookings"),
        _sum("amount").alias("total_amount")
    )
    .orderBy("booking_month", "gender")
)

# Write to gold schema as a Delta table
(
    bookings_by_gender.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("claudecatalog.gold.bookings_by_gender")
)

print("Successfully created claudecatalog.gold.bookings_by_gender")
print(f"Row count: {spark.table('claudecatalog.gold.bookings_by_gender').count()}")
