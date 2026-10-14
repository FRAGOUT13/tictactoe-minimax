"""
stats.py
--------
Tracks wins / losses / draws and saves them to a JSON file
so your record survives between runs.
"""

import json
import os

# stats.json is saved in the same folder as this file
STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.json")


def load_stats():
    # if file exists read it, otherwise start from 0
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass  # corrupted file -> start fresh
    return {"wins": 0, "losses": 0, "draws": 0}


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def record_result(stats, result, human="X", ai="O"):
    """Update the stats dict with a finished game's result and save it."""
    # add 1 to wins, losses or draws
    if result == human:
        stats["wins"] += 1
    elif result == ai:
        stats["losses"] += 1
    else:
        stats["draws"] += 1
    save_stats(stats)
    return stats


def reset_stats():
    # set everything back to 0
    stats = {"wins": 0, "losses": 0, "draws": 0}
    save_stats(stats)
    return stats


def format_stats(stats):
    # add them up to get total games
    total = stats["wins"] + stats["losses"] + stats["draws"]
    return (f"Games: {total} | Wins: {stats['wins']} | "
            f"Losses: {stats['losses']} | Draws: {stats['draws']}")
