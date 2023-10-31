"""
CRON Job
*/30 * * * * cd /home/brayps/Documents/Obsidian && /home/brayps/.cache/pypoetry/virtualenvs/obsidian-d0oIucnu-py3.10/bin/python3 tasks.py &> /home/brayps/Documents/Obsidian/tasks.log
"""

import json
import os

from loguru import logger
import sys

def sync_hotkeys(c, parent_dir: str = "."):
    """
    This script crawls through a directory and finds every obsidian hotkeys.json file.
    It then combines every hotkeys file into one hotkey file and overwrites all the existing hotkey files
    starting with the least recently updated ones.
    """
    logger.info("Syncing hotkeys...")

    combined_hotkeys = {}
    file_modification_times = {}

    # Collect modification times of 'hotkeys.json' files
    for dirpath, dirnames, filenames in os.walk(parent_dir):
        for filename in filenames:
            if filename == "hotkeys.json":
                filepath = os.path.join(dirpath, filename)
                file_modification_times[filepath] = os.stat(filepath).st_mtime

    # Sort files by modification time, in ascending order (oldest first)
    sorted_files = sorted(file_modification_times.items(), key=lambda x: x[1])

    for filepath, _ in sorted_files:
        logger.debug(filepath)
        with open(filepath, "r") as f:
            data = json.load(f)
        combined_hotkeys.update(data)

    # Write the combined hotkeys back to all files
    for filepath, _ in sorted_files:
        with open(filepath, "w") as f:
            json.dump(combined_hotkeys, f, indent=2)

    logger.info("Hotkeys sunc")


def clean(c):
    c.run("black .")
    c.run("isort .")

if __name__ == "__main__":
    sync_hotkeys("")
