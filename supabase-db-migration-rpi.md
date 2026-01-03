# Research: Supabase for League Table Manager Data Storage

## Current Storage Architecture

### Implementation Details

The application currently uses a **hybrid storage strategy**:

- **Local Storage**: JSONL (JSON Lines) files in `/league_data/` directory
- **Cloud Sync**: HuggingFace Dataset Repository (`asvs/league-table-data`)
- **Upload Pattern**: Immediate synchronous uploads after every CRUD operation
- **In-Memory Cache**: Python list maintains current state for calculations

### Data Models

**Match Records** (JSONL format):
```json
{
  "id": "uuid-string",
  "home": "team-name",
  "away": "team-name",
  "home_goals": 0-9,
  "away_goals": 0-9,
  "datetime": "ISO-8601-timestamp",
  "updated_at": "ISO-8601-timestamp (optional)"
}
```

**Deletion Logs** (JSONL format):
```json
{
  "match_id": "uuid-string",
  "home": "team-name",
  "away": "team-name",
  "home_goals": 0-9,
  "away_goals": 0-9,
  "datetime": "ISO-8601-timestamp"
}
```

### Current Architecture Flow

```
User Input → In-Memory List → Local JSONL File → HuggingFace Upload
                    ↓
              Calculations (League Table, H2H Stats)
```

---

## Supabase Python Integration

**Project Details:**
- Project Name: fc25
- Project URL: `https://ichhsthxaegexeogolzz.supabase.co`
- Current State: Empty (no tables)
- Installed Extensions: `uuid-ossp`, `pgcrypto`, `pg_graphql`

---

## Implementation Steps

### 1. Create Database Schema in Supabase

Create `matches` table with the following structure:
```sql
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    home TEXT NOT NULL,
    away TEXT NOT NULL,
    home_goals INTEGER NOT NULL CHECK (home_goals >= 0 AND home_goals <= 9),
    away_goals INTEGER NOT NULL CHECK (away_goals >= 0 AND away_goals <= 9),
    datetime TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add constraint to prevent same team playing itself
ALTER TABLE matches ADD CONSTRAINT different_teams CHECK (home <> away);

-- Create index for faster queries on datetime
CREATE INDEX idx_matches_datetime ON matches(datetime DESC);
```

### 2. Enable Row Level Security (RLS)

```sql
-- Enable RLS on matches table
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access (adjust as needed)
CREATE POLICY "Allow public read access" ON matches FOR SELECT USING (true);

-- policy for public insert/update/delete: anyone can do any of these actions. update and delete records must be maintained. just timestamp, activity log
```

### 3. Add supabase-py Package

```bash
uv add supabase
```

### 4. Create Supabase Client Configuration

Create environment variables for Supabase credentials:
- `SUPABASE_URL`: https://ichhsthxaegexeogolzz.supabase.co
- `SUPABASE_KEY`: (anon/public key from Supabase dashboard)

Initialize client:
```python
from supabase import create_client, Client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
```

### 5. Replace CRUD Operations in app.py

**Insert Match (replace `add_match` logic):**
```python
response = supabase.table("matches").insert({
    "home": home,
    "away": away,
    "home_goals": int(home_goals),
    "away_goals": int(away_goals)
}).execute()
```

**Select All Matches (replace `load_matches` logic):**
```python
response = supabase.table("matches").select("*").order("datetime", desc=True).execute()
matches = response.data
```

**Update Match (replace `update_match` logic):**
```python
response = supabase.table("matches").update({
    "home": new_home,
    "away": new_away,
    "home_goals": int(new_home_goals),
    "away_goals": int(new_away_goals),
    "updated_at": datetime.now(IST).isoformat()
}).eq("id", match_id).execute()
```

**Delete Match (replace `delete_match` logic - actual delete, no soft delete needed):**
```python
response = supabase.table("matches").delete().eq("id", match_id).execute()
```

### 6. Migrate Existing Data
Current matches:
Seelam	Akhil	5	3
Seelam	Kartheek	4	4
Shiva	Akhil	1	6
Shiva	Kartheek	8	3
Shiva	Kartheek	4	1
Seelam	Kartheek	5	1
Seelam	Kartheek	1	6
Akhil	Kartheek	1	5
Shiva	Akhil	3	1
Shiva	Akhil	3	3
Seelam	Kartheek	1	3
Seelam	Akhil	2	4
Seelam	Kartheek	2	1
Ashwik	Shiva	2	1
Kartheek	Seelam	4	5
Kartheek	Akhil	3	1
Kartheek	Seelam	5	1
Kartheek	Seelam	2	4
Kartheek	Seelam	4	5
Kartheek	Seelam	2	4
Seelam	Kartheek	3	7
Seelam	Kartheek	7	4
Seelam	Kartheek	3	3
Akhil	Kartheek	0	6
Seelam	Kartheek	2	2
Kartheek	Seelam	8	5
Akhil	Kane	10	2
Seelam	Kane	5	6
Kartheek	Seelam	0	9
Kane	Kartheek	5	1
Kane	Akhil	8	2
Ashwik	Akhil	4	3
Seelam	Kartheek	1	5


### 7. Remove HuggingFace Storage Code

Remove the following from `app.py`:
- `HfApi` import and initialization
- `REPO_ID`, `REPO_TYPE`, `PATH_IN_REPO` constants
- `MATCHES_FILE`, `DELETION_LOG_FILE` paths
- `ensure_repo_exists()` function
- `file_lock` threading lock
- All `api.upload_file()` calls
- All local JSONL file read/write operations

### 8. Simplify In-Memory Cache

The in-memory `matches` list can be replaced with direct Supabase queries, or kept as a cache that syncs on:
- App startup (load from Supabase)
- After each CRUD operation (refresh from Supabase or update locally)

### 9. Update Error Handling

Replace HuggingFace error handling with Supabase-specific handling:
```python
try:
    response = supabase.table("matches").insert({...}).execute()
    if response.data:
        # Success
except Exception as e:
    logger.error(f"Supabase error: {e}")
```

### 10. Test All CRUD Operations

Verify:
- Add match → appears in Supabase table and UI
- Update match → changes reflected in both
- Delete match → removed from Supabase and UI
- Load matches → correctly fetches all records on app startup
- Head-to-head stats → work with Supabase data

---