import os
import subprocess
import random
from datetime import datetime, timedelta

# ==== CONFIGURATION ====

# Option 1: Single date with number of commits
# single_commit = ["2025-06-10", 7]

# Option 2: Range of dates with total number of commits
commit_range = ["2025-03-23", "2025-04-24", 80]

# Path to your local cloned repository
REPO_DIR = "C:/Users/user/OneDrive/Desktop/Green"

# Hidden file to commit (won't attract attention)
FILE_NAME = ".activity"

# Generic identity to anonymize commits
AUTHOR_NAME = "rojanstha621"
AUTHOR_EMAIL = "rojanstha621@gmail.com"

# ==== FUNCTION DEFINITIONS ====

def run_git_command(command, env=None):
    try:
        subprocess.run(command, check=True, shell=isinstance(command, str), env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        exit(1)

def make_commit(commit_date):
    # Random time for realism
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt_obj = datetime.strptime(commit_date, "%Y-%m-%d")
    full_datetime = dt_obj.replace(hour=hour, minute=minute, second=second)
    formatted_date = full_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    # Write the date to a hidden file
    with open(FILE_NAME, "a") as f:
        f.write(f"{dt_obj.strftime('%Y-%m-%d')}\n")

    # Git operations
    run_git_command(["git", "add", FILE_NAME])
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
    run_git_command(["git", "commit", "-m", "\u200B"], env=env)

# ==== MAIN LOGIC ====

os.chdir(REPO_DIR)
if not os.path.isdir(".git"):
    print("❗ This is not a Git repository!")
    exit(1)

commit_dates = []

try:
    # Try single_commit mode
    date_str, n_commits = single_commit
    commit_dates = [date_str] * int(n_commits)
except NameError:
    # Fallback to commit_range mode
    try:
        start_str, end_str, total_commits = commit_range
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        total_days = (end_date - start_date).days + 1

        if total_commits > total_days:
            print("ℹ️ More commits than days. Some days will have multiple commits.")

        # Spread commits randomly
        days_list = [start_date + timedelta(days=i) for i in range(total_days)]
        chosen_days = random.choices(days_list, k=total_commits)
        chosen_days.sort()
        commit_dates = [day.strftime("%Y-%m-%d") for day in chosen_days]
    except Exception as e:
        print("❌ Invalid configuration:", e)
        exit(1)

# Make all commits
for date in commit_dates:
    make_commit(date)

# Final push
run_git_command("git push origin main")

print(f"✅ {len(commit_dates)} stealth commits pushed.")
