import json
import os

from invoke import task
from loguru import logger


def safe_update(new, old):
    for key, val in new.items():
        if key in old.keys() and val is not old[key]:
            logger.warning(f"New {key} value:\n{val}\nOld {key} value {old[key]}")


@task
def sync_hotkeys(c, parent_dir: str = "."):
    """
    This script crawls through a directory and finds every obsidian hotkeys.json file.
    It then combines every hotkeys file into one hotkey file and writes that file over all the existing hotkey files.
    """

    combined_hotkeys = {}

    for dirpath, dirnames, filenames in os.walk(parent_dir):
        for filename in filenames:
            if filename == "hotkeys.json":
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r") as f:
                    data = json.load(f)
                combined_hotkeys.update(data)
    logger.info("\n" + json.dumps(combined_hotkeys, indent=2))


@task
def clean(c):
    c.run("black .")
    c.run("isort .")
