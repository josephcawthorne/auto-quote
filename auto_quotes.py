import random
import subprocess
from datetime import datetime, date, timedelta
from pathlib import Path

FILE_PATH = Path(__file__).parent / "quotes_log.py"

PURPOSE_LINE = (
    "The purpose of this repository is to demonstrate that GitHub commit history is not "
    "an effective measure of skill, and it cannot be trusted."
)
HEADER_TEXT = "Git hub commit history does not work for measuring skill level."
HEADER_SUMMARY_1 = (
    "A simple Python script can automate daily commits — therefore it is not a measure that can be trusted."
)
NEXT_PREFIX = "# NEXT_COMMIT_DATE: "

QUOTES = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "Whether you think you can or you think you can’t, you’re right. — Henry Ford",
    "Success is the sum of small efforts, repeated day in and day out. — Robert Collier",
    "It always seems impossible until it’s done. — Nelson Mandela",
    "You miss 100% of the shots you don’t take. — Wayne Gretzky",
    "Do what you can, with what you have, where you are. — Theodore Roosevelt",
    "Perfection is the enemy of progress. — Winston Churchill",
    "Fall seven times and stand up eight. — Japanese Proverb",
    "Action is the foundational key to all success. — Pablo Picasso",
    "The future depends on what you do today. — Mahatma Gandhi",
    "Discipline is the bridge between goals and accomplishment. — Jim Rohn",
    "Motivation gets you going, but discipline keeps you growing. — John C. Maxwell",
    "Great things are done by a series of small things brought together. — Vincent van Gogh",
    "Energy and persistence conquer all things. — Benjamin Franklin",
    "What we repeatedly do, we become. — Aristotle (paraphrased)",
    "The man who moves a mountain begins by carrying away small stones. — Confucius",
    "Courage is resistance to fear, mastery of fear, not absence of fear. — Mark Twain",
    "Dream big. Start small. But most of all, start. — Simon Sinek",
    "Small deeds done are better than great deeds planned. — Peter Marshall",
    "Done is better than perfect. — Sheryl Sandberg",
]


def create_initial_file(today: date) -> None:
    """Create the initial quotes_log.py file with a stylised header."""
    border = "#" * (len(HEADER_TEXT) + 8)
    lines = [
        f"# {PURPOSE_LINE}\n",
        "\n",
        f"{border}\n",
        f"#   {HEADER_TEXT}   #\n",
        f"{border}\n",
        f"# {HEADER_SUMMARY_1}\n",
        "\n",
        f"{NEXT_PREFIX}{today.isoformat()}\n",
        "\n",
        "\n",
        "# Quote log\n",
        "# ----------\n",
    ]
    FILE_PATH.write_text("".join(lines), encoding="utf-8")
    print("Created initial quotes_log.py")


def load_lines():
    text = FILE_PATH.read_text(encoding="utf-8")
    return text.splitlines(keepends=True)


def main():
    today = datetime.utcnow().date()
    print(f"Today (UTC): {today}")

    if not FILE_PATH.exists():
        create_initial_file(today)

    lines = load_lines()

    # Find NEXT_COMMIT_DATE line
    try:
        next_idx = next(
            i for i, line in enumerate(lines) if line.startswith(NEXT_PREFIX)
        )
    except StopIteration:
        # If somehow missing, add it after the header
        next_idx = 7
        lines.insert(next_idx, f"{NEXT_PREFIX}{today.isoformat()}\n")

    next_date_str = lines[next_idx].split(":", 1)[1].strip()
    next_date = date.fromisoformat(next_date_str)
    print(f"Next scheduled commit date: {next_date}")

    # If not yet scheduled day, skip quietly
    if today < next_date:
        print("Not a commit day. Exiting without changes.")
        return

    # It's a commit day 🎉
    num_commits = random.randint(2, 3)
    gap_days = random.randint(2, 3)
    new_next_date = today + timedelta(days=gap_days)
    lines[next_idx] = f"{NEXT_PREFIX}{new_next_date.isoformat()}\n"

    print(f"Commit day! Making {num_commits} commits.")
    print(f"Next commit scheduled for: {new_next_date}")

    # Collect existing quotes
    existing_quotes = set()
    for line in lines:
        if (
            line.startswith("# ")
            and PURPOSE_LINE not in line
            and HEADER_TEXT not in line
            and HEADER_SUMMARY_1 not in line
            and not line.startswith(NEXT_PREFIX)
            and not line.startswith("# Quote log")
            and not line.startswith("# ----------")
            and not line.startswith("###")
        ):
            existing_quotes.add(line[2:].strip())

    available = [q for q in QUOTES if q not in existing_quotes]
    selected = []

    if len(available) >= num_commits:
        selected = random.sample(available, num_commits)
    else:
        selected = available[:]
        remaining = num_commits - len(selected)
        if remaining > 0:
            selected += random.sample(QUOTES, remaining)

    existing_count = len(existing_quotes)

    for i, quote in enumerate(selected, start=1):
        quote_number = existing_count + i
        print(f"Adding quote #{quote_number}: {quote}")

        lines.append(f"# {quote}\n")
        FILE_PATH.write_text("".join(lines), encoding="utf-8")

        subprocess.run(["git", "add", str(FILE_PATH)], check=True)
        subprocess.run(["git", "commit", "-m", f"Add quote #{quote_number}"], check=True)

    print("All commits done.")


if __name__ == "__main__":
    main()
