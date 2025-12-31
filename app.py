"""League Table Manager - Interactive Gradio Interface"""
import json
import threading
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import pandas as pd
import gradio as gr
from huggingface_hub import HfApi

# Constants
TEAMS = ["Seelam", "Akhil", "Kartheek", "Shiva"]

# Dataset storage setup
DATASET_DIR = Path("league_data")
DATASET_DIR.mkdir(parents=True, exist_ok=True)

MATCHES_FILE = DATASET_DIR / f"matches-{uuid4()}.jsonl"
DELETION_LOG_FILE = DATASET_DIR / f"deletions-{uuid4()}.jsonl"

# Initialize HfApi for immediate uploads
api = HfApi()
REPO_ID = "asvs/league-table-data"
REPO_TYPE = "dataset"
PATH_IN_REPO = "data"

# Thread lock for safe concurrent writes
file_lock = threading.Lock()

# Global matches storage
matches = []


def ensure_repo_exists():
    """Create the HuggingFace dataset repository if it doesn't exist."""
    try:
        # Check if repo exists by trying to get repo info
        api.repo_info(repo_id=REPO_ID, repo_type=REPO_TYPE)
        print(f"Repository '{REPO_ID}' already exists")
    except Exception:
        # Repository doesn't exist, create it
        try:
            api.create_repo(
                repo_id=REPO_ID,
                repo_type=REPO_TYPE,
                private=True,
                exist_ok=True
            )
            print(f"Created new dataset repository: '{REPO_ID}'")
        except Exception as e:
            print(f"Error creating repository: {e}")
            print("Please create the repository manually or check your HF_TOKEN permissions")


def initialize_matches_from_league_scores():
    """Initialize matches from league_scores.py data."""
    initial_matches = [
        ["Seelam", "Akhil", 5, 3],
        ["Seelam", "Kartheek", 4, 4],
        ["Shiva", "Akhil", 1, 6],
        ["Shiva", "Kartheek", 8, 3],
        ["Shiva", "Kartheek", 4, 1],
        ["Seelam", "Kartheek", 5, 1],
        ["Seelam", "Kartheek", 1, 6],
        ["Akhil", "Kartheek", 1, 5],
        ["Shiva", "Akhil", 3, 1],
        ["Shiva", "Akhil", 3, 3],
        ["Seelam", "Kartheek", 1, 3],
    ]
    return initial_matches


def load_matches():
    """Load matches from all JSONL files in dataset directory."""
    global matches
    matches = []

    # Load deleted match IDs
    deleted_ids = set()
    deletion_files = sorted(DATASET_DIR.glob("deletions-*.jsonl"))
    for deletion_file in deletion_files:
        try:
            with deletion_file.open("r") as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        deleted_ids.add(record["match_id"])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading {deletion_file}: {e}")
            continue

    # Load all match records from JSONL files
    match_files = sorted(DATASET_DIR.glob("matches-*.jsonl"))

    if not match_files:
        # Initialize with data from league_scores.py if no files exist
        initial_matches = initialize_matches_from_league_scores()
        # Save initial matches
        for match in initial_matches:
            match_id = str(uuid4())
            with file_lock:
                with MATCHES_FILE.open("a") as f:
                    record = {
                        "id": match_id,
                        "home": match[0],
                        "away": match[1],
                        "home_goals": match[2],
                        "away_goals": match[3],
                        "datetime": datetime.now().isoformat()
                    }
                    json.dump(record, f)
                    f.write("\n")
                    matches.append([match_id, match[0], match[1], match[2], match[3], record["datetime"]])

        # Upload initial matches file immediately
        try:
            api.upload_file(
                path_or_fileobj=str(MATCHES_FILE),
                path_in_repo=f"{PATH_IN_REPO}/{MATCHES_FILE.name}",
                repo_id=REPO_ID,
                repo_type=REPO_TYPE,
            )
        except Exception as e:
            print(f"Error uploading initial matches: {e}")
    else:
        # Load matches from all JSONL files, excluding deleted ones
        for match_file in match_files:
            try:
                with match_file.open("r") as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            match_id = record["id"]
                            # Skip deleted matches
                            if match_id not in deleted_ids:
                                matches.append([
                                    match_id,
                                    record["home"],
                                    record["away"],
                                    record["home_goals"],
                                    record["away_goals"],
                                    record.get("datetime", datetime.now().isoformat())  # Default to now if missing
                                ])
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading {match_file}: {e}")
                continue

    return matches




def calculate_table(matches_list):
    """Calculate league table from matches list."""
    # Get all unique teams from matches
    all_teams = set()
    for match in matches_list:
        all_teams.add(match[1])  # home team (skip ID at index 0)
        all_teams.add(match[2])  # away team

    # Initialize stats for all teams
    table = {t: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "Pts": 0, "GPM": 0.0, "WP": 0.0}
             for t in all_teams}

    # Process each match
    for match in matches_list:
        match_id, h, a, gh, ga = match[0], match[1], match[2], match[3], match[4]

        table[h]["P"] += 1
        table[a]["P"] += 1
        table[h]["GF"] += gh
        table[h]["GA"] += ga
        table[a]["GF"] += ga
        table[a]["GA"] += gh

        if gh > ga:
            table[h]["W"] += 1
            table[a]["L"] += 1
            table[h]["Pts"] += 3
        elif gh < ga:
            table[a]["W"] += 1
            table[h]["L"] += 1
            table[a]["Pts"] += 3
        else:
            table[h]["D"] += 1
            table[a]["D"] += 1
            table[h]["Pts"] += 1
            table[a]["Pts"] += 1

    # Calculate derived stats
    for t in all_teams:
        if table[t]["P"] > 0:
            table[t]["GPM"] = round(table[t]["GF"] / table[t]["P"], 2)
            table[t]["WP"] = round((table[t]["W"] / table[t]["P"]) * 100, 2)

    # Create DataFrame
    df = pd.DataFrame.from_dict(table, orient="index")
    df["GD"] = df["GF"] - df["GA"]
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Team"}, inplace=True)

    # Sort by WP descending (as per requirements)
    df = df[["Team", "WP", "GPM", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]]
    df = df.sort_values(by=["WP"], ascending=False)

    return df


def calculate_head_to_head(team1, team2, matches_list):
    """Calculate head-to-head stats between two teams."""
    if not team1 or not team2 or team1 == team2:
        return pd.DataFrame()

    # Initialize stats for both teams
    stats = {
        team1: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "WP": 0.0},
        team2: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "WP": 0.0}
    }

    # Process matches between these two teams
    for match in matches_list:
        h, a, gh, ga = match[1], match[2], match[3], match[4]

        # Check if this match involves both teams
        if (h == team1 and a == team2) or (h == team2 and a == team1):
            # Update stats for home team
            stats[h]["P"] += 1
            stats[h]["GF"] += gh
            stats[h]["GA"] += ga

            # Update stats for away team
            stats[a]["P"] += 1
            stats[a]["GF"] += ga
            stats[a]["GA"] += gh

            # Update W/D/L
            if gh > ga:
                stats[h]["W"] += 1
                stats[a]["L"] += 1
            elif gh < ga:
                stats[a]["W"] += 1
                stats[h]["L"] += 1
            else:
                stats[h]["D"] += 1
                stats[a]["D"] += 1

    # Calculate win percentages
    for team in [team1, team2]:
        if stats[team]["P"] > 0:
            stats[team]["WP"] = round((stats[team]["W"] / stats[team]["P"]) * 100, 2)

    # Create a 2-column DataFrame
    data = {
        "Stat": ["P", "W", "D", "L", "Win %", "GF", "GA"],
        team1: [
            stats[team1]["P"],
            stats[team1]["W"],
            stats[team1]["D"],
            stats[team1]["L"],
            f"{stats[team1]['WP']}%",
            stats[team1]["GF"],
            stats[team1]["GA"]
        ],
        team2: [
            stats[team2]["P"],
            stats[team2]["W"],
            stats[team2]["D"],
            stats[team2]["L"],
            f"{stats[team2]['WP']}%",
            stats[team2]["GF"],
            stats[team2]["GA"]
        ]
    }

    return pd.DataFrame(data)


def get_matches_dataframe(matches_list):
    """Convert matches list to DataFrame for display."""
    if not matches_list:
        return pd.DataFrame(columns=["#", "Timestamp", "Home", "Away", "Home Goals", "Away Goals"])

    # Sort matches by datetime (most recent first)
    sorted_matches = sorted(matches_list, key=lambda x: x[5], reverse=True)

    data = []
    for i, match in enumerate(sorted_matches, 1):
        match_id, h, a, gh, ga, dt = match

        # Format datetime as DD-MM-YY HH:MM AM/PM
        dt_obj = datetime.fromisoformat(dt)
        formatted_dt = dt_obj.strftime("%d-%m-%y %I:%M %p")

        data.append({
            "#": i,
            "Timestamp": formatted_dt,
            "Home": h,
            "Away": a,
            "Home Goals": gh,
            "Away Goals": ga
        })

    return pd.DataFrame(data)


def add_match(home, away, home_goals, away_goals):
    """Add a new match and update tables."""
    # Validation
    if not home or not away or not home.strip() or not away.strip():
        return (
            calculate_table(matches),
            get_matches_dataframe(matches),
            "Error: Team names cannot be empty!"
        )

    # Clean up team names
    home = home.strip()
    away = away.strip()

    if home == away:
        return (
            calculate_table(matches),
            get_matches_dataframe(matches),
            "Error: Home and away teams must be different!"
        )

    if home_goals < 0 or away_goals < 0:
        return (
            calculate_table(matches),
            get_matches_dataframe(matches),
            "Error: Goals must be non-negative!"
        )

    # Add match with file lock for thread-safe writes
    match_id = str(uuid4())
    match_datetime = datetime.now().isoformat()
    match_data = [match_id, home, away, int(home_goals), int(away_goals), match_datetime]
    matches.append(match_data)

    # Persist to dataset
    with file_lock:
        with MATCHES_FILE.open("a") as f:
            record = {
                "id": match_id,
                "home": home,
                "away": away,
                "home_goals": int(home_goals),
                "away_goals": int(away_goals),
                "datetime": match_datetime
            }
            json.dump(record, f)
            f.write("\n")

    # Upload file immediately to HuggingFace
    try:
        api.upload_file(
            path_or_fileobj=str(MATCHES_FILE),
            path_in_repo=f"{PATH_IN_REPO}/{MATCHES_FILE.name}",
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
        )
        upload_status = " (uploaded to HF)"
    except Exception as e:
        print(f"Error uploading match: {e}")
        upload_status = " (upload failed)"

    # Return updated tables and status
    league_table = calculate_table(matches)
    matches_table = get_matches_dataframe(matches)
    status = f"Match added: {home} {int(home_goals)} - {int(away_goals)} {away}{upload_status}"

    return league_table, matches_table, status


def delete_match(row_number):
    """Delete a match from history by row number."""
    if row_number is None or row_number < 1:
        return (
            calculate_table(matches),
            get_matches_dataframe(matches),
            "Error: Please enter a valid row number!"
        )

    # Convert to 0-based index
    row_idx = int(row_number) - 1

    if row_idx >= len(matches) or row_idx < 0:
        return (
            calculate_table(matches),
            get_matches_dataframe(matches),
            f"Error: Row {int(row_number)} does not exist! Valid rows: 1-{len(matches)}"
        )

    # Get match details for logging
    match = matches[row_idx]
    match_id, h, a, gh, ga = match[0], match[1], match[2], match[3], match[4]

    # Log deletion with file lock
    with file_lock:
        with DELETION_LOG_FILE.open("a") as f:
            deletion_record = {
                "match_id": match_id,
                "home": h,
                "away": a,
                "home_goals": gh,
                "away_goals": ga,
                "datetime": datetime.now().isoformat()
            }
            json.dump(deletion_record, f)
            f.write("\n")

    # Upload deletion log immediately to HuggingFace
    try:
        api.upload_file(
            path_or_fileobj=str(DELETION_LOG_FILE),
            path_in_repo=f"{PATH_IN_REPO}/{DELETION_LOG_FILE.name}",
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
        )
        upload_status = " (uploaded to HF)"
    except Exception as e:
        print(f"Error uploading deletion log: {e}")
        upload_status = " (upload failed)"

    # Remove match from in-memory list
    matches.pop(row_idx)

    # Return updated tables and status
    league_table = calculate_table(matches)
    matches_table = get_matches_dataframe(matches)
    status = f"Deleted row {int(row_number)}: {h} vs {a} ({gh}-{ga}){upload_status}"

    return league_table, matches_table, status


def build_interface():
    """Build and return the Gradio interface."""
    # Ensure HuggingFace repository exists
    ensure_repo_exists()

    # Load initial data
    load_matches()

    with gr.Blocks(title="League Table Manager") as demo:
        gr.Markdown("# League Table Manager")

        with gr.Tabs():
            with gr.Tab("League Manager"):
                with gr.Row():
                    # Left Column - Input Form
                    with gr.Column(scale=1):
                        home_team = gr.Dropdown(
                            choices=TEAMS,
                            label="Home Team",
                            value=TEAMS[0],
                            allow_custom_value=True
                        )
                        away_team = gr.Dropdown(
                            choices=TEAMS,
                            label="Away Team",
                            value=TEAMS[1],
                            allow_custom_value=True
                        )

                        with gr.Row():
                            home_goals = gr.Number(
                                label="Home Goals",
                                value=0,
                                minimum=0,
                                precision=0
                            )
                            away_goals = gr.Number(
                                label="Away Goals",
                                value=0,
                                minimum=0,
                                precision=0
                            )

                        submit_btn = gr.Button("Add Match", variant="primary")
                        status_msg = gr.Textbox(label="Status", interactive=False)

                    # Right Column - Tables
                    with gr.Column(scale=2):
                        league_table = gr.Dataframe(
                            label="League Table",
                            value=calculate_table(matches),
                            interactive=False,
                            wrap=True
                        )

                        matches_table = gr.Dataframe(
                            label="Match History",
                            value=get_matches_dataframe(matches),
                            interactive=False,
                            wrap=True
                        )

                        with gr.Row():
                            delete_row_input = gr.Number(
                                label="Row # to Delete",
                                value=None,
                                minimum=1,
                                precision=0,
                                scale=2
                            )
                            delete_btn = gr.Button("Delete Row", variant="stop", scale=1)

                # Event Handlers
                submit_btn.click(
                    fn=add_match,
                    inputs=[home_team, away_team, home_goals, away_goals],
                    outputs=[league_table, matches_table, status_msg]
                )

                delete_btn.click(
                    fn=delete_match,
                    inputs=[delete_row_input],
                    outputs=[league_table, matches_table, status_msg]
                )

            with gr.Tab("Team vs Team Stats"):
                gr.Markdown("### Head-to-Head Statistics")

                with gr.Row():
                    h2h_team1 = gr.Dropdown(
                        choices=TEAMS,
                        label="Team 1",
                        value=TEAMS[0],
                        allow_custom_value=True
                    )
                    h2h_team2 = gr.Dropdown(
                        choices=TEAMS,
                        label="Team 2",
                        value=TEAMS[1],
                        allow_custom_value=True
                    )

                h2h_stats = gr.Dataframe(
                    label="Head-to-Head Stats",
                    value=calculate_head_to_head(TEAMS[0], TEAMS[1], matches),
                    interactive=False,
                    wrap=True
                )

                # Event handler for team selection
                h2h_team1.change(
                    fn=lambda t1, t2: calculate_head_to_head(t1, t2, matches),
                    inputs=[h2h_team1, h2h_team2],
                    outputs=[h2h_stats]
                )

                h2h_team2.change(
                    fn=lambda t1, t2: calculate_head_to_head(t1, t2, matches),
                    inputs=[h2h_team1, h2h_team2],
                    outputs=[h2h_stats]
                )

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
