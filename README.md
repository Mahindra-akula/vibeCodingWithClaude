# Vibe Coding a Medallion Pipeline with Claude Code + Databricks

Build a complete **Bronze → Silver → Gold** data pipeline on Databricks using nothing but natural language prompts — no manual coding required.

## What's Inside

| File | Purpose |
|------|---------|
| `GETTING_STARTED.md` | Step-by-step beginner guide to rebuild this from scratch |
| `PROMPT_GUIDE.md` | Every prompt used + enriched versions to copy and adapt |
| `SKILL.md` | Claude Code skill reference for this architecture pattern |
| `scripts/` | All PySpark scripts for each pipeline layer |
| `source-files/` | Sample CSV source data (bookings, passengers, airports) |

## Architecture

```
source-files/*.csv
        │
        ▼
  claudecatalog.raw          (bookings, passengers, airports)
        │
        ├──────────────────────────────┐
        ▼                              ▼
  claudecatalog.silver                claudecatalog.silver
  bookings_passengers                 bookings_airports
        │                              │
        ▼                              ▼
  claudecatalog.gold                  claudecatalog.gold
  bookings_by_gender                  bookings_by_airport
```

## Job DAG: `claude_vibe_code_medallion_flow`

```
ingest_csv_to_raw
    ├── raw_to_silver_bookings_passengers → silver_to_gold_bookings_by_gender
    └── raw_to_silver_bookings_airports   → silver_to_gold_bookings_by_airport
```

## Quick Start

1. Clone this repo
2. Follow [GETTING_STARTED.md](GETTING_STARTED.md) to set up Claude Code + Databricks MCP
3. Use the prompts in [PROMPT_GUIDE.md](PROMPT_GUIDE.md) to rebuild the pipeline conversationally

## Tools Used

- [Claude Code](https://claude.ai/code) — AI coding assistant
- [Databricks MCP Server](https://github.com/databricks-solutions/ai-dev-kit) — Databricks tools for Claude
- [Databricks Serverless](https://docs.databricks.com/en/jobs/index.html) — Compute for job tasks
- [Delta Lake](https://delta.io) — Storage format for all tables
- [Unity Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/index.html) — Data governance
