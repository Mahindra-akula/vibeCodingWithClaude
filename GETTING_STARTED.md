# Getting Started: Vibe Coding a Medallion Pipeline with Claude Code + Databricks

A step-by-step guide for anyone new to Databricks, Claude Code, or vibe coding. By the end, you'll have a fully working Bronze → Silver → Gold data pipeline built entirely through conversation.

---

## What Is Vibe Coding?

Vibe coding means describing what you want in plain English and letting an AI assistant (Claude) write and execute the code for you. You direct the "what", Claude handles the "how".

---

## What You'll Build

A **Medallion Architecture** pipeline on Databricks:

| Layer | Tables | Description |
|-------|--------|-------------|
| **Raw** | `bookings`, `passengers`, `airports` | Raw CSVs ingested as Delta tables |
| **Silver** | `bookings_passengers`, `bookings_airports` | Joined, enriched datasets |
| **Gold** | `bookings_by_gender`, `bookings_by_airport` | Aggregated, business-ready metrics |

Everything is orchestrated by a single Databricks Job with 5 tasks in a DAG.

---

## Prerequisites

### 1. Databricks Account
- Sign up at [databricks.com](https://databricks.com) (free trial available)
- Create a Unity Catalog-enabled workspace
- Create a catalog (e.g., `claudecatalog`) in Unity Catalog

### 2. Generate a Databricks Personal Access Token (PAT)
1. In Databricks, go to **User Settings → Developer → Access Tokens**
2. Click **Generate new token**, give it a name, copy it

### 3. Configure `~/.databrickscfg`
Create or edit the file `~/.databrickscfg`:
```ini
[DEFAULT]
host = https://<your-workspace>.cloud.databricks.com
token = <your-pat-token>
```

### 4. Install Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```
Then authenticate:
```bash
claude
```
Follow the login prompts to connect your Anthropic account.

### 5. Install the Databricks AI Dev Kit
```bash
# Clone the dev kit
git clone https://github.com/databricks-solutions/ai-dev-kit ~/.ai-dev-kit

# Install dependencies
cd ~/.ai-dev-kit
pip install -r requirements.txt
```

### 6. Configure the Databricks MCP Server
Create or edit `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "databricks": {
      "command": "python",
      "args": ["~/.ai-dev-kit/repo/databricks-mcp-server/run_server.py"],
      "env": {
        "DATABRICKS_CONFIG_PROFILE": "DEFAULT"
      }
    }
  }
}
```
Restart Claude Code after editing this file.

---

## Step-by-Step: Building the Pipeline

### Step 1 — Prepare Your Source Data

Upload the three CSV files (`bookings.csv`, `passengers.csv`, `airports.csv`) to the `source-files/` folder in this repository, or host them somewhere accessible (GitHub raw URLs, Databricks Volume, S3, etc.).

See `source-files/` in this repo for the expected schema of each file.

---

### Step 2 — Start Claude Code

Open a terminal in your project folder and start Claude Code:
```bash
cd ~/your-project-folder
claude
```

Verify the Databricks MCP tools are loaded — you should see Databricks tools available.

---

### Step 3 — Ingest CSVs to Raw Layer

Prompt Claude:
```
I have 3 CSV files: bookings, passengers, and airports. 
Ingest them into claudecatalog.raw schema as Delta tables. 
Create a Python script and a Databricks Job called "ingest_csv_to_raw" to do this.
```

Claude will:
- Write `scripts/ingest_csv_to_raw.py`
- Upload it to your Databricks workspace
- Create a Databricks Job with a serverless Python task

---

### Step 4 — Run the Raw Ingestion Job

```
Run the job now
```

Claude triggers the job and waits for it to complete, reporting success or failure.

---

### Step 5 — Build the Silver Layer

```
I have 3 tables bookings, passengers and airports in my claudecatalog.raw schema. 
I want to join bookings and passengers tables on passenger_id column. 
Also, join bookings and airports table on airport_id column. 
Create a new schema called silver and create the new joined datasets as new tables 
in the silver schema. Add a new task in the job "ingest_csv_to_raw" for this new requirement.
```

Claude will:
- Create `claudecatalog.silver` schema
- Write two PySpark join scripts
- Upload them to the workspace
- Add two dependent tasks to the job

---

### Step 6 — Build the Gold Layer

```
Create a new schema called "gold" in the same claudecatalog. 
Then, create an aggregate table called bookings_by_gender that has bookings by month 
by gender and another table called bookings_by_airport with an aggregate of bookings 
by airport by month. Add new tasks to the existing job.
```

Claude will:
- Create `claudecatalog.gold` schema
- Write two PySpark aggregation scripts
- Upload them to the workspace
- Add two more tasks to the job (chained after silver tasks)

---

### Step 7 — Run the Full Pipeline

```
Run the job now
```

All 5 tasks execute in the correct order:
```
ingest_csv_to_raw
    ├── raw_to_silver_bookings_passengers → silver_to_gold_bookings_by_gender
    └── raw_to_silver_bookings_airports   → silver_to_gold_bookings_by_airport
```

---

### Step 8 — Rename the Job (Optional)

```
Update the job name to "claude_vibe_code_medallion_flow"
```

---

## Verify Your Tables

Once the job completes, you can query any table:
```
Query claudecatalog.gold.bookings_by_gender and show me the results
```

Or in Databricks SQL:
```sql
SELECT * FROM claudecatalog.gold.bookings_by_gender ORDER BY booking_month, gender;
SELECT * FROM claudecatalog.gold.bookings_by_airport ORDER BY total_bookings DESC LIMIT 20;
```

---

## Project Structure

```
vibeCodingWithClaude/
├── scripts/
│   ├── ingest_csv_to_raw.py                    # Raw ingestion
│   ├── raw_to_silver_bookings_passengers.py    # Silver: bookings + passengers join
│   ├── raw_to_silver_bookings_airports.py      # Silver: bookings + airports join
│   ├── silver_to_gold_bookings_by_gender.py    # Gold: bookings by month + gender
│   └── silver_to_gold_bookings_by_airport.py  # Gold: bookings by airport + month
├── source-files/
│   ├── bookings.csv
│   ├── passengers.csv
│   └── airports.csv
├── SKILL.md            # Claude Code skill reference
├── GETTING_STARTED.md  # This guide
├── PROMPT_GUIDE.md     # All prompts used in this project
└── README.md           # Project overview
```

---

## Tips for Vibe Coding on Databricks

1. **Be specific about table names and schemas** — Claude will use exactly what you say
2. **Mention the job name** when adding tasks — Claude will look it up and update it
3. **Ask Claude to run the job** after every change to verify it works
4. **Chain requests naturally** — "now do the same for airports" works perfectly
5. **Ask questions** — "what columns does the silver table have?" works too
