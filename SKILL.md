# Vibe Coding Medallion Flow — Claude Code Skill

## Overview

This skill guides Claude Code to build a **full Medallion Architecture pipeline on Databricks** (Bronze/Raw → Silver → Gold) using natural language prompts. It covers Unity Catalog schema management, PySpark transformations, and Databricks Jobs orchestration — all driven conversationally via Claude Code + the Databricks MCP server.

## What This Skill Enables

- Create Unity Catalog schemas (`raw`, `silver`, `gold`) in any catalog
- Ingest CSV files from URLs or volumes into raw Delta tables
- Build silver-layer joined tables using PySpark
- Build gold-layer aggregated tables from silver
- Create and manage multi-task Databricks Jobs with proper DAG dependencies
- Run jobs and monitor results — all from natural language

## Prerequisites

- Databricks workspace with Unity Catalog enabled
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Databricks MCP server configured (`~/.claude/mcp.json`)
- Valid Databricks PAT in `~/.databrickscfg` under `[DEFAULT]`
- Catalog already created in Unity Catalog (e.g., `claudecatalog`)

## Medallion Architecture Pattern

```
Source CSVs (GitHub / Volumes)
        │
        ▼
  [RAW layer]          claudecatalog.raw.*
  Delta tables         (bookings, passengers, airports)
        │
        ├──────────────────────────┐
        ▼                          ▼
  [SILVER layer]             [SILVER layer]
  bookings_passengers        bookings_airports
  (join on passenger_id)     (join on airport_id)
        │                          │
        ▼                          ▼
  [GOLD layer]               [GOLD layer]
  bookings_by_gender         bookings_by_airport
  (by month + gender)        (by airport + month)
```

## Job DAG

```
ingest_csv_to_raw
    ├── raw_to_silver_bookings_passengers → silver_to_gold_bookings_by_gender
    └── raw_to_silver_bookings_airports   → silver_to_gold_bookings_by_airport
```

## Scripts Reference

| Script | Layer | Purpose |
|--------|-------|---------|
| `ingest_csv_to_raw.py` | Raw | Reads CSVs via pandas, writes Delta tables to `raw` schema |
| `raw_to_silver_bookings_passengers.py` | Silver | Inner join bookings + passengers on `passenger_id` |
| `raw_to_silver_bookings_airports.py` | Silver | Inner join bookings + airports on `airport_id` |
| `silver_to_gold_bookings_by_gender.py` | Gold | Aggregate total bookings + amount by month and gender |
| `silver_to_gold_bookings_by_airport.py` | Gold | Aggregate total bookings + amount by airport and month |

## Key Databricks MCP Tools Used

| Tool | Purpose |
|------|---------|
| `manage_uc_objects` | Create/manage catalogs, schemas, volumes |
| `execute_sql` | Run SQL queries and DDL |
| `manage_workspace_files` | Upload Python scripts to workspace |
| `manage_jobs` | Create, update, and configure jobs |
| `manage_job_runs` | Trigger and monitor job runs |

## Prompt Patterns

### Create a schema
```
Create a new schema called "silver" in claudecatalog
```

### Join two tables and persist
```
Join [table_a] and [table_b] on [column]. Create the result as a new table 
in claudecatalog.silver. Add a task to the job "[job_name]" for this.
```

### Aggregate to gold
```
Create an aggregate table called [name] that has [metric] by [dimension1] 
by [dimension2]. Add new tasks to the existing job.
```

### Run the job
```
Run the job now
```

## Extending This Skill

- Add more silver tables (e.g., join bookings + flights)
- Add SCD Type 2 history tracking using `MERGE INTO`
- Add data quality checks between layers using Great Expectations or Delta constraints
- Schedule the job with a cron trigger
- Add email notifications on failure
