import json
import random
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEDULE_FILE = Path(__file__).parent / "schedule.json"

START_HOUR = 8
END_HOUR = 23


def load_schedule():
    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)


def save_schedule(schedule):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=2)
        f.write("\n")


def generate_random_time():
    tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)

    random_hour = random.randint(START_HOUR, END_HOUR - 1)
    random_minute = random.randint(0, 59)

    next_run = datetime(
        tomorrow.year,
        tomorrow.month,
        tomorrow.day,
        random_hour,
        random_minute,
        tzinfo=timezone.utc,
    )

    return next_run


def run_fancy_job():
    script_path = Path(__file__).parent.parent / "update_number.py"

    print("Execution is due.")
    print("Running update_number.py...")

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
    )

    print("Fancy job completed successfully.")


def main():
    schedule = load_schedule()

    if schedule["next_run"] is None:
        next_run = generate_random_time()
        schedule["next_run"] = next_run.isoformat()
        save_schedule(schedule)

        print(f"Generated first random execution time: {next_run}")
        return

    next_run = datetime.fromisoformat(schedule["next_run"])
    now = datetime.now(timezone.utc)

    if now < next_run:
        print("Not due yet.")
        print(f"Current time: {now}")
        print(f"Next run: {next_run}")
        return

    print(f"Execution is due: {next_run}")

    # Only generate the next schedule after the job succeeds.
    run_fancy_job()

    next_run = generate_random_time()
    schedule["next_run"] = next_run.isoformat()
    save_schedule(schedule)

    print(f"Next random execution time: {next_run}")


if __name__ == "__main__":
    main()