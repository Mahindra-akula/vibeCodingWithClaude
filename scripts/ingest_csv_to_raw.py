import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# GitHub raw URLs
files = {
    "airports":   "https://raw.githubusercontent.com/anshlambagit/Claude_X_Dtabricks/main/airports.csv",
    "bookings":   "https://raw.githubusercontent.com/anshlambagit/Claude_X_Dtabricks/main/bookings.csv",
    "passengers": "https://raw.githubusercontent.com/anshlambagit/Claude_X_Dtabricks/main/passengers.csv",
}

catalog = "claudecatalog"
schema  = "raw"

for table_name, url in files.items():
    print(f"Processing {table_name}...")

    # Read with pandas
    pdf = pd.read_csv(url)
    # Strip whitespace from column names
    pdf.columns = [c.strip() for c in pdf.columns]

    # Convert to Spark DataFrame
    sdf = spark.createDataFrame(pdf)

    # Write as Delta table (overwrite if exists)
    full_name = f"{catalog}.{schema}.{table_name}"
    sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(full_name)

    print(f"  Created {full_name} ({sdf.count()} rows, columns: {sdf.columns})")

print("\nAll tables created successfully!")
