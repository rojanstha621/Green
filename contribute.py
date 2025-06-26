import os
import subprocess
import random
from datetime import datetime, timedelta

# ==== CONFIGURATION ====

REPO_DIR = "C:/Users/user/OneDrive/Desktop/Green"
FILE_NAME = ".activity"
AUTHOR_NAME = "rojanstha621"
AUTHOR_EMAIL = "rojanstha621@gmail.com"

# GitHub contribution grid: 7 rows (Sun-Sat), multiple columns (weeks)
HACKER_GRID = [
    # H
    [1,0,1,0,1],
    [1,0,1,0,1],
    [1,1,1,1,1],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [0,0,0,0,0],  # space
    # A
    [0,1,1,1,0],
    [1,0,0,0,1],
    [1,1,1,1,1],
    [1,0,0,0,1],
    [1,0,0,0,1],
    [0,0,0,0,0],  # space
    # C
    [0,1,1,1,1],
    [1,0,0,0,0],
    [1,0,0,0,0],
    [1,0,0,0,0],
    [0,1,1,1,1],
    [0,0,0,0,0],  # space
    # K
    [1,0,0,0,1],
    [1,0,0,1,0],
    [1,1,1,0,0],
    [1,0,0,1,0],
    [1,0,0,0,1],
    [0,0,0,0,0],  # space
    # E
    [1,1,1,1,1],
    [1,0,0,0,0],
    [1,1,1,1,0],
    [1,0,0,0,0],
    [1,1,1,1,1],
    [0,0,0,0,0],  # space
    # R
    [1,1,1,1,0],
    [1,0,0,0,1],
    [1,1,1,1,0],
    [1,0,1,0,0],
    [1,0,0,1,0],
]

START_DATE = datetime(2024, 1, 7)  # must be a Sunday


def run_git_command(command, env=None):
    try:
        subprocess.run(command, check=True, shell=isinstance(command, str), env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        exit(1)


def make_commit(commit_date):
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    full_datetime = commit_date.replace(hour=hour, minute=minute, second=second)
    formatted_date = full_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    with open(FILE_NAME, "a") as f:
        f.write(f"{commit_date.strftime('%Y-%m-%d')}\n")

    run_git_command(["git", "add", FILE_NAME])
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
    run_git_command(["git", "commit", "-m", "Hacker"], env=env)


def get_commit_dates_from_grid(grid, start_date):
    dates = []
    for col, week in enumerate(grid):
        for row, cell in enumerate(week):
            if cell == 1:
                commit_date = start_date + timedelta(weeks=col, days=row)
                dates.append(commit_date)
    return dates


# ==== MAIN EXECUTION ====

os.chdir(REPO_DIR)
if not os.path.isdir(".git"):
    print("❗ Not a git repository!")
    exit(1)

commit_dates = get_commit_dates_from_grid(HACKER_GRID, START_DATE)

for date in commit_dates:
    make_commit(date)

run_git_command("git push origin main")

print(f"✅ {len(commit_dates)} commits made to draw 'HACKER' on your contribution graph.")
