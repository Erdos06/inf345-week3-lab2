#!/usr/bin/env python3
"""
INF 345 - roster validator.

This is the script that marks your Week 1 submission.

Usage:
    python3 scripts/validate_roster.py                  # check every file in students/
    python3 scripts/validate_roster.py --author NAME    # also require a file for NAME

Exit code 0 = pass, 1 = fail. That exit code is what GitHub Actions turns into
the green tick or the red cross on your pull request.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

STUDENTS_DIR = Path("students")
EXAMPLE_FILE = "EXAMPLE.yml"

REQUIRED_FIELDS = ("name", "github", "group", "os")
VALID_GROUPS = ("A", "B")
VALID_OS = ("windows", "macos", "linux")

# GitHub's own rule: 1-39 chars, alphanumeric or hyphen, no leading/trailing or
# doubled hyphen. Filenames must match this exactly, lowercase.
GITHUB_USERNAME_RE = re.compile(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$")
SDU_EMAIL_RE = re.compile(r"^[^@\s]+@(?:stu\.)?sdu\.edu\.kz$", re.IGNORECASE)


class Problem(Exception):
    """One thing wrong with one file, phrased so a student can fix it."""


def load_yaml(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Problem(
            "the file is not valid UTF-8 text. If you created it in Notepad on "
            "Windows, save it again with encoding set to UTF-8."
        )

    if not raw.strip():
        raise Problem("the file is empty.")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise Problem(
            f"this is not valid YAML. Python says: {exc}\n"
            "      Most common cause: a missing space after the colon. "
            "Write 'name: Aisha', not 'name:Aisha'."
        )

    if not isinstance(data, dict):
        raise Problem(
            "the file must be a set of 'key: value' lines. "
            "Copy students/EXAMPLE.yml and edit the values."
        )
    return data


def check_file(path: Path) -> None:
    """Raise Problem on the first thing wrong. Never raise anything else."""
    # Not path.stem: for 'aisha.yml.txt' (Notepad helpfully appending .txt)
    # path.stem is 'aisha.yml', which would suggest renaming to 'aisha.yml.yml'.
    stem = path.name.split(".", 1)[0]

    if path.suffix != ".yml" or path.name.count(".") != 1:
        raise Problem(
            f"the filename must be exactly '<your-github-username>.yml'. "
            f"Yours is '{path.name}'. Rename it to {stem}.yml\n"
            "      On Windows, turn on 'File name extensions' in Explorer's View "
            "menu first, or you will not see the extension you are fixing."
        )

    if not GITHUB_USERNAME_RE.match(stem):
        raise Problem(
            f"'{stem}' is not a valid GitHub username, so it cannot be the filename. "
            "Use your username exactly as it appears in your profile URL, in "
            "lowercase, with no spaces, no '@' and no .yml inside the name."
        )

    data = load_yaml(path)

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise Problem(
            f"missing required field(s): {', '.join(missing)}. "
            "Compare your file with students/EXAMPLE.yml"
        )

    unknown = [k for k in data if k not in (*REQUIRED_FIELDS, "email")]
    if unknown:
        raise Problem(
            f"unexpected field(s): {', '.join(sorted(unknown))}. "
            f"Allowed fields are: {', '.join((*REQUIRED_FIELDS, 'email'))}"
        )

    github = data["github"]
    if not isinstance(github, str) or github.strip().lower().lstrip("@") != stem:
        raise Problem(
            f"the 'github:' value ({github!r}) does not match the filename "
            f"('{stem}.yml'). These two must be the same username."
        )

    name = data["name"]
    if not isinstance(name, str) or len(name.strip()) < 3:
        raise Problem(
            "'name:' must be your real full name, as it appears in the student "
            "system - at least 3 characters."
        )

    group = data["group"]
    if isinstance(group, str):
        group = group.strip().upper()
    if group not in VALID_GROUPS:
        raise Problem(
            f"'group:' must be A or B, not {data['group']!r}. "
            "Group A is the 12:30 practice, Group B is the 13:30 practice."
        )

    os_value = data["os"]
    if not isinstance(os_value, str) or os_value.strip().lower() not in VALID_OS:
        raise Problem(
            f"'os:' must be one of {', '.join(VALID_OS)}, not {data['os']!r}. "
            "This tells me which install instructions you will need."
        )

    if "email" in data:
        email = data["email"]
        if not isinstance(email, str) or not SDU_EMAIL_RE.match(email.strip()):
            raise Problem(
                f"'email:' must be your university address ending in @sdu.edu.kz "
                f"or @stu.sdu.edu.kz, not {email!r}. Personal addresses are not "
                "accepted for coursework."
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--author",
        help="GitHub username of the pull request author; if given, that "
             "student must have a file and must not have touched anyone else's.",
    )
    args = parser.parse_args()

    if not STUDENTS_DIR.is_dir():
        print(f"::error::'{STUDENTS_DIR}/' directory is missing from the repository.")
        return 1

    files = sorted(p for p in STUDENTS_DIR.iterdir() if p.name != EXAMPLE_FILE)
    failures = 0

    for path in files:
        if path.is_dir():
            print(f"::error file={path}::'{path}' is a folder. Submit a single "
                  f"file named students/<your-github-username>.yml, not a folder.")
            failures += 1
            continue
        try:
            check_file(path)
        except Problem as exc:
            # ::error:: makes GitHub annotate the exact file in the PR diff.
            print(f"::error file={path}::{path.name}: {exc}")
            failures += 1
        else:
            print(f"  ok  {path.name}")

    if args.author:
        author = args.author.strip().lower()
        expected = STUDENTS_DIR / f"{author}.yml"
        if not expected.exists():
            print(
                f"::error::You opened this pull request as '{args.author}', but "
                f"there is no students/{author}.yml in it. The file must be named "
                f"after your own GitHub username."
            )
            failures += 1

    print()
    if failures:
        print(f"FAILED - {failures} problem(s) in {len(files)} file(s).")
        print("Fix the file, commit again and push. The check re-runs by itself.")
        return 1

    print(f"PASSED - {len(files)} file(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
