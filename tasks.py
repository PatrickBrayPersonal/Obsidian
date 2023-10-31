import json
import os

from invoke import task
from loguru import logger


@task
def sync_hotkeys(c, parent_dir: str = "."):
    """
    This script crawls through a directory and finds every obsidian hotkeys.json file.
    It then combines every hotkeys file into one hotkey file and writes that file over all the existing hotkey files.
    """


import json
import os

from invoke import task
from loguru import logger


@task
def sync_hotkeys(c, parent_dir: str = "."):
    """
    This script crawls through a directory and finds every obsidian hotkeys.json file.
    It then combines every hotkeys file into one hotkey file and overwrites all the existing hotkey files
    starting with the least recently updated ones.
    """

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
        logger.info(filepath)
        with open(filepath, "r") as f:
            data = json.load(f)
        combined_hotkeys.update(data)

    # Write the combined hotkeys back to all files
    for filepath, _ in sorted_files:
        with open(filepath, "w") as f:
            json.dump(combined_hotkeys, f, indent=2)

    logger.info(
        "Combined hotkeys have been written to all 'hotkeys.json' files, starting with the least recently updated ones."
    )


@task
def clean(c):
    c.run("black .")
    c.run("isort .")
