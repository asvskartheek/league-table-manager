"""CRUD operations: add, update, and delete matches via Supabase."""
from datetime import datetime

from config import supabase, IST, logger
import data


def add_match(home, away, home_goals, away_goals):
    """Validate and insert a new match into Supabase and the in-memory cache."""
    if not home or not away or not home.strip() or not away.strip():
        return "Error: Team names cannot be empty!"

    home = home.strip()
    away = away.strip()

    if home == away:
        return "Error: Home and away teams must be different!"

    if home_goals < 0 or away_goals < 0:
        return "Error: Goals must be non-negative!"

    logger.info(f"-> Adding match: {home} {int(home_goals)} - {int(away_goals)} {away}")

    try:
        match_datetime = datetime.now(IST).isoformat()
        response = supabase.table("matches").insert({
            "home": home,
            "away": away,
            "home_goals": int(home_goals),
            "away_goals": int(away_goals),
            "datetime": match_datetime
        }).execute()

        if response.data:
            record = response.data[0]
            match_id = str(record["id"])
            match_entry = [match_id, home, away, int(home_goals), int(away_goals), record["datetime"]]
            data.matches.append(match_entry)
            logger.info(f"  ✓ Match ID: {match_id}")
            return f"Match added: {home} {int(home_goals)} – {int(away_goals)} {away}"
        else:
            return "Match added locally but Supabase returned no data"

    except Exception as e:
        logger.error(f"  ✗ Error saving to Supabase: {e}")
        return f"Error: Failed to save match — {e}"


def delete_match_by_id(match_id):
    """Delete a match from Supabase and remove it from the in-memory cache."""
    try:
        supabase.table("matches").delete().eq("id", match_id).execute()
        for i, match in enumerate(data.matches):
            if match[0] == match_id:
                data.matches.pop(i)
                break
        logger.info(f"  ✓ Match {match_id} deleted")
        return True
    except Exception as e:
        logger.error(f"  ✗ Error deleting: {e}")
        return False


def update_match(row_number, new_home, new_away, new_home_goals, new_away_goals):
    """Update an existing match (identified by display row number) in Supabase and the cache."""
    if row_number is None or row_number < 1:
        return "Error: Please enter a valid row number!"

    sorted_matches = sorted(data.matches, key=lambda x: x[5], reverse=True)
    row_idx = int(row_number) - 1

    if row_idx >= len(sorted_matches) or row_idx < 0:
        return f"Error: Row {int(row_number)} does not exist! Valid rows: 1–{len(sorted_matches)}"

    if not new_home or not new_away or not new_home.strip() or not new_away.strip():
        return "Error: Team names cannot be empty!"

    new_home = new_home.strip()
    new_away = new_away.strip()

    if new_home == new_away:
        return "Error: Home and away teams must be different!"

    if new_home_goals < 0 or new_away_goals < 0:
        return "Error: Goals must be non-negative!"

    sorted_match = sorted_matches[row_idx]
    match_id = sorted_match[0]

    try:
        update_datetime = datetime.now(IST).isoformat()
        response = supabase.table("matches").update({
            "home": new_home,
            "away": new_away,
            "home_goals": int(new_home_goals),
            "away_goals": int(new_away_goals),
            "updated_at": update_datetime
        }).eq("id", match_id).execute()

        if response.data:
            for i, match in enumerate(data.matches):
                if match[0] == match_id:
                    data.matches[i][1] = new_home
                    data.matches[i][2] = new_away
                    data.matches[i][3] = int(new_home_goals)
                    data.matches[i][4] = int(new_away_goals)
                    break
            return f"Updated row {int(row_number)}: {new_home} {int(new_home_goals)} – {int(new_away_goals)} {new_away}"
        else:
            return "Error: Update returned no data"

    except Exception as e:
        logger.error(f"  ✗ Error updating: {e}")
        return f"Error: Failed to update match — {e}"
