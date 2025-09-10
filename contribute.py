import os
import subprocess
import random
from datetime import datetime, timedelta

# ==== CONFIGURATION ====
# Use current repository directory by default
REPO_DIR = os.getcwd()
FILE_NAME = ".activity"
AUTHOR_NAME = "rojanstha621"
AUTHOR_EMAIL = "rojanstha621@gmail.com"

# Intensity (commits) per lit pixel
PIXEL_INTENSITY = 6

def run_git_command(args, env=None):
    subprocess.run(args, check=True, shell=False, env=env)

def detect_current_branch():
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            check=True, capture_output=True, text=True)
    branch = result.stdout.strip()
    return branch

def last_saturday(reference_date: datetime) -> datetime:
    # GitHub grid columns are weeks Sun..Sat; we end on the last complete Saturday
    weekday = reference_date.weekday()  # Mon=0 .. Sun=6
    # Days since Saturday (5)
    delta_days = (weekday - 5) % 7
    end = reference_date - timedelta(days=delta_days)
    return datetime(end.year, end.month, end.day)

def sunday_on_or_after(date_obj: datetime) -> datetime:
    # Ensure start is a Sunday to align top row=Sunday
    weekday = date_obj.weekday()  # Mon=0 .. Sun=6
    days_until_sunday = (6 - weekday) % 7
    sunday = date_obj + timedelta(days=days_until_sunday)
    return datetime(sunday.year, sunday.month, sunday.day)

def sunday_on_or_before(date_obj: datetime) -> datetime:
    weekday = date_obj.weekday()  # Mon=0 .. Sun=6
    days_since_sunday = (weekday + 1) % 7
    sunday = date_obj - timedelta(days=days_since_sunday)
    return datetime(sunday.year, sunday.month, sunday.day)

def saturday_on_or_after(date_obj: datetime) -> datetime:
    weekday = date_obj.weekday()  # Mon=0 .. Sun=6
    # Saturday is 5
    days_until_saturday = (5 - weekday) % 7
    saturday = date_obj + timedelta(days=days_until_saturday)
    return datetime(saturday.year, saturday.month, saturday.day)

def build_5x7_font():
    # 7 rows (Sun..Sat), 5 cols per letter. 1=filled, 0=empty
    return {
        "H": [
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
        ],
        "A": [
            [0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
        ],
        "C": [
            [0,1,1,1,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [0,1,1,1,1],
        ],
        "K": [
            [1,0,0,1,0],
            [1,0,1,0,0],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
        ],
        "E": [
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1],
        ],
        "R": [
            [1,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1],
        ],
        " ": [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
    }

def build_word_grid(word: str):
    font = build_5x7_font()
    rows = 7
    # Assemble letters with 1-column spacer between them
    grid = [[0] for _ in range(rows)]  # start with a spacer column to breathe
    for idx, ch in enumerate(word):
        letter = font[ch]
        for r in range(rows):
            grid[r].extend(letter[r])
        # spacer between letters
        if idx != len(word) - 1:
            for r in range(rows):
                grid[r].append(0)
    # Remove leading spacer column
    grid = [row[1:] for row in grid]
    return grid

def right_align_grid(grid, total_weeks: int):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    pad_cols = max(0, total_weeks - cols)
    padded = []
    for r in range(rows):
        padded.append([0] * pad_cols + grid[r])
    return padded

def center_align_grid(grid, total_weeks: int):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    total_pad = max(0, total_weeks - cols)
    left_pad = total_pad // 2
    right_pad = total_pad - left_pad
    padded = []
    for r in range(rows):
        padded.append([0] * left_pad + grid[r] + [0] * right_pad)
    return padded

def make_commit(commit_date: datetime, intensity: int):
    num_commits = max(0, intensity)
    for _ in range(num_commits):
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
        run_git_command(["git", "commit", "-m", "Update contribution graph"], env=env)

def get_commit_dates_from_grid(grid, start_date: datetime):
    dates_with_intensity = []
    for week in range(len(grid[0])):  # columns = weeks
        for day in range(len(grid)):  # rows = days (0=Sunday)
            intensity = grid[day][week]
            if intensity > 0:
                commit_date = start_date + timedelta(weeks=week, days=day)
                dates_with_intensity.append((commit_date, intensity))
    return dates_with_intensity

# ==== MAIN EXECUTION ====
if not os.path.isdir(".git"):
    print("❗ Not a git repository! Run this inside your repo root.")
    raise SystemExit(1)

word = "HACKER"
base_grid = build_word_grid(word)

# Choose time window mode
TARGET_YEAR = 2023 # set to an int like 2024 to target a year; None = recent 52 weeks

if TARGET_YEAR:
    # Align to full calendar year view for the selected year
    year_start = datetime(TARGET_YEAR, 1, 1)
    year_end = datetime(TARGET_YEAR, 12, 31)
    start_date = sunday_on_or_before(year_start)
    end_date = saturday_on_or_after(year_end)
    total_weeks = ((end_date - start_date).days // 7) + 1
else:
    # Determine the most recent full Saturday and align our grid to the last 52 weeks
    today = datetime.utcnow()
    end_saturday = last_saturday(today)
    total_weeks = 52  # GitHub shows ~52 weeks
    start_date = sunday_on_or_after(end_saturday - timedelta(weeks=total_weeks - 1))

# Center the word within the chosen window
grid = center_align_grid(base_grid, total_weeks)

commit_dates = get_commit_dates_from_grid(grid, start_date)
total_commits = sum(intensity for _, intensity in commit_dates) * PIXEL_INTENSITY

print(f"🚀 Creating commits to draw '{word}' ({len(commit_dates)} lit days, {total_commits} commits)...")

for date, intensity in commit_dates:
    make_commit(date, PIXEL_INTENSITY)

# Push to current branch
current_branch = detect_current_branch()
run_git_command(["git", "push", "origin", current_branch])

print(f"✅ Finished drawing '{word}' on your contribution graph!")