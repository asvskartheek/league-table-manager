"""Data layer: in-memory match cache, Supabase loading, and table calculations."""
import re
from datetime import datetime, timezone

import pandas as pd

from config import supabase, IST, logger

# Global in-memory match cache.
# Each entry is a list: [id, home, away, home_goals, away_goals, datetime_str]
matches = []


def load_matches():
    """Load all matches from Supabase into the in-memory cache."""
    global matches

    logger.info("=" * 60)
    logger.info("LOADING MATCHES FROM SUPABASE")
    logger.info("=" * 60)

    try:
        logger.info(f"-> Connecting to Supabase: {supabase.supabase_url}")
        response = supabase.table("matches").select("*").order("datetime", desc=True).execute()

        matches = []
        if response.data:
            for record in response.data:
                matches.append([
                    str(record["id"]),
                    record["home"],
                    record["away"],
                    record["home_goals"],
                    record["away_goals"],
                    record["datetime"]
                ])
            logger.info(f"✓ Successfully loaded {len(matches)} matches from Supabase")
        else:
            logger.info("✓ No matches found in database")

        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ Error accessing Supabase: {e}")
        matches = []

    return matches


def get_teams_from_matches():
    """Extract sorted unique team names from the in-memory match cache."""
    teams = set()
    for match in matches:
        teams.add(match[1])
        teams.add(match[2])
    return sorted(list(teams)) if teams else []


def calculate_table(matches_list):
    """Calculate the league table DataFrame from a list of match records."""
    all_teams = set()
    for match in matches_list:
        all_teams.add(match[1])
        all_teams.add(match[2])

    table = {
        t: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0,
            "Pts": 0, "GPM": 0.0, "GAM": 0.0, "GDM": 0.0, "WP": 0.0,
            "#WW": 0, "#5GM": 0}
        for t in all_teams
    }

    for match in matches_list:
        match_id, h, a, gh, ga = match[0], match[1], match[2], match[3], match[4]

        table[h]["P"] += 1
        table[a]["P"] += 1
        table[h]["GF"] += gh
        table[h]["GA"] += ga
        table[a]["GF"] += ga
        table[a]["GA"] += gh

        if gh >= 5:
            table[h]["#5GM"] += 1
        if ga >= 5:
            table[a]["#5GM"] += 1

        if gh > ga:
            table[h]["W"] += 1
            table[a]["L"] += 1
            table[h]["Pts"] += 3
            if ga == 0:
                table[h]["#WW"] += 1
        elif gh < ga:
            table[a]["W"] += 1
            table[h]["L"] += 1
            table[a]["Pts"] += 3
            if gh == 0:
                table[a]["#WW"] += 1
        else:
            table[h]["D"] += 1
            table[a]["D"] += 1
            table[h]["Pts"] += 1
            table[a]["Pts"] += 1

    for t in all_teams:
        if table[t]["P"] > 0:
            table[t]["GPM"] = round(table[t]["GF"] / table[t]["P"], 2)
            table[t]["GAM"] = round(table[t]["GA"] / table[t]["P"], 2)
            table[t]["GDM"] = round((table[t]["GF"] - table[t]["GA"]) / table[t]["P"], 2)
            table[t]["WP"] = round((table[t]["W"] / table[t]["P"]) * 100, 2)

    df = pd.DataFrame.from_dict(table, orient="index")
    df["GD"] = df["GF"] - df["GA"]
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Team"}, inplace=True)
    df = df[["Team", "WP", "GPM", "GAM", "GDM", "P", "W", "D", "L", "GF", "GA", "GD", "Pts", "#WW", "#5GM"]]
    df = df.sort_values(by=["WP"], ascending=False)
    return df


def _parse_datetime(dt):
    """Parse an ISO datetime string, handling variable microsecond precision."""
    try:
        return datetime.fromisoformat(dt)
    except ValueError:
        dt_normalized = re.sub(
            r'\.(\d+)', lambda m: '.' + m.group(1).ljust(6, '0')[:6], dt
        )
        return datetime.fromisoformat(dt_normalized)


def format_datetime(dt):
    """Convert a UTC/naive datetime string to an IST-formatted display string."""
    dt_obj = _parse_datetime(dt)
    if dt_obj.tzinfo is None:
        dt_obj = dt_obj.replace(tzinfo=timezone.utc).astimezone(IST)
    else:
        dt_obj = dt_obj.astimezone(IST)
    return dt_obj.strftime("%d-%m-%y %I:%M %p IST")
