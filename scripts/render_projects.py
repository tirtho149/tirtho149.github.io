#!/usr/bin/env python3
"""Filter repos_raw.json -> projects.json, and render the "Code & Open Source"
section of index.html from it.

Filtering lives here rather than in a jq one-liner in the workflow: this is
testable locally, and jq is not installed on the dev machine, so a jq pipeline
could only ever be debugged by pushing to CI.

Scope note: this only ever rewrites the block between the CODE markers. The
hand-written Projects section above it is authored prose — richer than anything
the GitHub API returns, and it features repos under other owners (pest-id) that
a `user:tirtho149` query cannot see. It stays under human control.

Mirrors the scraper_gs_direct.py -> scholar_publications.json pattern.
"""

import html
import json
import pathlib
import re
import sys
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
RAW = ROOT / "repos_raw.json"
DATA = ROOT / "projects.json"

TOPIC = "portfolio"

START = "<!-- CODE:START -->"
END = "<!-- CODE:END -->"

# Matches the existing tables in index.html.
TABLE_OPEN = (
    '<table style="width:100%;border:0px;border-spacing:0px 10px;'
    'border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>'
)


def esc(s):
    return html.escape(s or "", quote=True)


def humanize(iso):
    """'2026-07-15T10:00:00Z' -> 'Jul 2026'."""
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%b %Y")
    except (ValueError, AttributeError):
        return ""


def row(repo):
    name = esc(repo["name"])
    url = esc(repo["url"])
    desc = esc(repo.get("description") or "")
    lang = esc(repo.get("lang") or "")
    stars = repo.get("stars") or 0
    when = humanize(repo.get("pushed", ""))

    # Badge mirrors .pub-badge/.venue/.year used by the Projects entries.
    badge = f'<span class="venue">{lang or "Code"}</span>'
    badge += f'<span class="year">{when}</span>' if when else ""

    star_bit = f' &nbsp;<span class="muted">&#9733; {stars}</span>' if stars else ""
    topics = [t for t in (repo.get("topics") or []) if t != "portfolio"]
    topic_bit = (
        f'<br><span class="muted">{esc(" · ".join(topics))}</span>' if topics else ""
    )

    return f"""          <tr>
            <td style="padding:16px;width:20%;vertical-align:middle"><div class="pub-badge">{badge}</div></td>
            <td style="padding:8px;width:80%;vertical-align:middle">
              <a href="{url}" target="_blank" rel="noopener"><span class="papertitle">{name}</span></a>{star_bit}<br>
              <em>{desc}</em>{topic_bit}
            </td>
          </tr>"""


IND = " " * 10  # matches the surrounding index.html indentation


def build(repos):
    if not repos:
        # Emit nothing rather than an empty heading.
        return f"{START}\n{IND}{END}"

    rows = "\n".join(row(r) for r in repos)
    return f"""{START}
          <table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
            <tr>
              <td style="padding:16px;width:100%;vertical-align:middle">
                <h2>Code &amp; Open Source</h2>
                <p>
                  Public repositories, refreshed automatically from
                  <span class="highlight">GitHub</span>.
                </p>
              </td>
            </tr>
          </tbody></table>

          {TABLE_OPEN}
{rows}
          </tbody></table>
{IND}{END}"""


def select(raw):
    """Flatten `gh api --paginate --slurp` output and apply the opt-in filter.

    --slurp yields one array PER PAGE, so the payload is a list of lists; a
    single page still arrives nested.
    """
    if raw and isinstance(raw[0], list):
        raw = [r for page in raw for r in page]

    picked = [
        r
        for r in raw
        if not r.get("fork")
        and not r.get("archived")
        and TOPIC in (r.get("topics") or [])
    ]
    picked.sort(key=lambda r: (-(r.get("stargazers_count") or 0), r["name"].lower()))

    return [
        {
            "name": r["name"],
            "description": r.get("description"),
            "url": r["html_url"],
            "stars": r.get("stargazers_count") or 0,
            "lang": r.get("language"),
            "topics": r.get("topics") or [],
            "pushed": r.get("pushed_at"),
        }
        for r in picked
    ]


def main():
    if not RAW.exists():
        sys.exit(f"missing {RAW} — the fetch step must run first")

    repos = select(json.loads(RAW.read_text()))
    DATA.write_text(json.dumps(repos, indent=2) + "\n")
    print(f"selected {len(repos)} repo(s) tagged '{TOPIC}'")

    text = INDEX.read_text()

    if START not in text or END not in text:
        sys.exit(
            f"markers not found in {INDEX}.\n"
            f"Add these two lines where the section should appear:\n"
            f"  {START}\n  {END}"
        )

    new = build(repos)
    out = re.sub(
        re.escape(START) + r".*?" + re.escape(END), lambda _: new, text, flags=re.S
    )

    if out == text:
        print("no change")
        return

    INDEX.write_text(out)
    print(f"rendered {len(repos)} repo(s) into {INDEX.name}")


if __name__ == "__main__":
    main()
