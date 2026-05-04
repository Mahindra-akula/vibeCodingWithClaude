# Prompt Guide — Vibe Coding a Medallion Pipeline with Claude Code + Databricks

A complete log of every prompt used to build this project, with enriched versions you can adapt for your own use.

---

## Prompt 1 — Ingest CSV Files to Raw Layer

**Original prompt:**
> I have 3 CSV files: bookings, passengers, and airports. Ingest them into claudecatalog.raw schema as Delta tables. Create a Databricks Job called "ingest_csv_to_raw".

**Enriched version:**
```
I have 3 CSV files: bookings.csv, passengers.csv, and airports.csv available at 
[your URL or volume path]. 

Please:
1. Create a Python script that reads each CSV using pandas and writes them as Delta 
   tables into claudecatalog.raw schema (bookings, passengers, airports)
2. Upload the script to the Databricks workspace
3. Create a Databricks Job called "ingest_csv_to_raw" using serverless compute with 
   a single Python task that runs the script
```

**What Claude does:**
- Writes `ingest_csv_to_raw.py` with pandas + PySpark ingestion logic
- Uploads to `/Workspace/Users/.../scripts/`
- Creates a Databricks Job with serverless environment

---

## Prompt 2 — Run the Job

**Original prompt:**
> Run the job now

**Enriched version:**
```
Run the job "ingest_csv_to_raw" now and wait for it to complete. 
Let me know if any tasks fail.
```

**What Claude does:**
- Calls `run_now` on the job
- Polls until completion
- Reports final status of each task

---

## Prompt 3 — Build the Silver Layer (Joins)

**Original prompt:**
> I have 3 tables bookings, passengers and airports in my claudecatalog.raw schema. I want to join bookings and passengers tables on passenger_id column. Also, join bookings and airports table on airport_id column. Create a new schema called silver and create the new joined datasets as new tables in the silver schema. Add a new task in the job "ingest_csv_to_raw" for this new requirement.

**Enriched version:**
```
I have 3 Delta tables in claudecatalog.raw: bookings, passengers, and airports.

Please:
1. Create a new schema called "silver" in claudecatalog
2. Write a PySpark script that inner-joins bookings and passengers on passenger_id 
   and saves the result as claudecatalog.silver.bookings_passengers (Delta, overwrite)
3. Write a PySpark script that inner-joins bookings and airports on airport_id 
   and saves the result as claudecatalog.silver.bookings_airports (Delta, overwrite)
4. Upload both scripts to the Databricks workspace
5. Add both as new tasks to the job "ingest_csv_to_raw", each depending on 
   the "ingest_csv_to_raw" task so they run after raw ingestion completes
```

**What Claude does:**
- Creates `claudecatalog.silver` schema via Unity Catalog API
- Writes and uploads two PySpark join scripts
- Updates the job with 2 new parallel tasks (both depending on the raw task)

---

## Prompt 4 — Run the Updated Job

**Original prompt:**
> Run the job now

*(Same as Prompt 2 — Claude always runs the most recent version of the job)*

---

## Prompt 5 — Build the Gold Layer (Aggregations)

**Original prompt:**
> Create a new schema called "gold" in the same claudecatalog. Then, create an aggregate table called booking_by_gender that has bookings by month by gender and another table called bookings_by_airport with an aggregate of bookings by airport by month. Add new tasks to the existing job.

**Enriched version:**
```
Using the silver tables we just created, build the gold layer:

1. Create a new schema called "gold" in claudecatalog
2. Write a PySpark script that reads claudecatalog.silver.bookings_passengers and 
   aggregates to produce claudecatalog.gold.bookings_by_gender with columns:
   - booking_month (yyyy-MM format, derived from booking_date)
   - gender
   - total_bookings (count of booking_id)
   - total_amount (sum of amount)
3. Write a PySpark script that reads claudecatalog.silver.bookings_airports and 
   aggregates to produce claudecatalog.gold.bookings_by_airport with columns:
   - airport_id, airport_name, city, country
   - booking_month (yyyy-MM format)
   - total_bookings (count of booking_id)
   - total_amount (sum of amount)
4. Upload both scripts to the Databricks workspace
5. Add both as new tasks to the existing job:
   - silver_to_gold_bookings_by_gender depends on raw_to_silver_bookings_passengers
   - silver_to_gold_bookings_by_airport depends on raw_to_silver_bookings_airports
```

**What Claude does:**
- Creates `claudecatalog.gold` schema
- Writes and uploads two PySpark aggregation scripts using `date_format` + `groupBy`
- Updates the job with 2 more tasks, correctly chained in the DAG

---

## Prompt 6 — Run the Full Pipeline

**Original prompt:**
> Run the job now

**What Claude does:**
- Triggers all 5 tasks in DAG order
- Reports success/failure per task with total run duration

---

## Prompt 7 — Rename the Job

**Original prompt:**
> Can you update the job name to "claude_vibe_code_medallion_flow"?

**Enriched version:**
```
Update the name of the job with ID [job_id] (currently "ingest_csv_to_raw") 
to "claude_vibe_code_medallion_flow"
```

**What Claude does:**
- Calls `jobs.update` with the new name
- Confirms the change

---

## Prompt 8 — Create Project Documentation and Push to GitHub

**Original prompt:**
> Create a skill file for this project and also a markdown document with step-by-step instructions so that someone new to databricks, claude code, and vibecoding can follow these instructions to build their own. Also, create a prompt guide with all the prompts used in this project. Then commit the entire project to GitHub.

**Enriched version:**
```
Please create the following documentation for this project:
1. SKILL.md — a Claude Code skill file describing what this project does, 
   the tools used, scripts, and reusable prompt patterns
2. GETTING_STARTED.md — a beginner-friendly step-by-step guide covering 
   prerequisites (Databricks account, Claude Code, MCP setup) and every 
   step to rebuild this pipeline from scratch
3. PROMPT_GUIDE.md — a complete log of every prompt used in this project, 
   with enriched versions someone can copy and adapt

Then initialize a git repo, add all project files (scripts, docs, source-files folder),
and push to [GitHub URL].
```

---

## Reusable Prompt Patterns

### Pattern: Create a new layer
```
Create a new schema called "[layer_name]" in [catalog_name].
```

### Pattern: Join two tables
```
Join [table_a] and [table_b] on [join_column]. Save the result as 
[catalog].[schema].[new_table]. Add a task to job "[job_name]" that depends 
on "[upstream_task]".
```

### Pattern: Aggregate to gold
```
Create an aggregate table [catalog].gold.[table_name] from [source_table] with:
- Dimensions: [dim1], [dim2]
- Metrics: count of [id_column] as total_bookings, sum of [amount_column] as total_amount
Add it as a task to the job depending on "[upstream_silver_task]".
```

### Pattern: Check a table
```
Show me a sample of [catalog].[schema].[table] — first 10 rows
```

### Pattern: Debug a failed task
```
The task "[task_name]" failed in the last job run. Can you get the output logs 
and help me understand what went wrong?
```

### Pattern: Add a schedule
```
Add a daily schedule to job "[job_name]" to run at 6am UTC every day.
```
