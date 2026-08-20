#!/usr/bin/env python3
"""Repoint US Code citations away from the lapsed linkedlegislation.com domain.

Posts from 2013 cite sections of the U.S. Code through the old Linked
Legislation app at www.linkedlegislation.com. That domain has since lapsed and
now serves an unrelated online gambling site. A later domain sweep moved these
links to www.linkedlegislation.org, which resolves nowhere at all. Both forms
are matched.

Each is repointed to the same section on uscode.house.gov, the Law Revision
Counsel's official U.S. Code, which is what the citation referred to.

Exit codes: 0 success, 2 --check found links still needing a fix.
"""

import argparse
import glob
import re
import sys

DEAD = re.compile(
    r'https?://(?:www\.)?linkedlegislation\.(?:com|org)/laws/title-(\d+)/section-([\w-]+)/[^"\'<>\s]*'
)


def uscode(title, section, amp="&amp;"):
    """The posts are raw HTML, so query separators are entity-escaped."""
    return (
        "https://uscode.house.gov/view.xhtml?req=granuleid:"
        f"USC-prelim-title{title}-section{section}{amp}num=0{amp}edition=prelim"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    total, files = 0, []
    for path in sorted(glob.glob("_posts/*") + glob.glob("_drafts/*")):
        src = open(path, encoding="utf-8").read()
        hits = DEAD.findall(src)
        if not hits:
            continue
        out = DEAD.sub(lambda m: uscode(m.group(1), m.group(2)), src)
        total += len(hits)
        files.append(path)
        for title, section in sorted(set(hits)):
            print(f"  {title} USC {section} -> {uscode(title, section, '&')}")
        if not args.check:
            open(path, "w", encoding="utf-8").write(out)

    verb = "would rewrite" if args.check else "rewrote"
    print(f"\n{verb} {total} citations across {len(files)} file(s)")
    return 2 if (args.check and total) else 0


if __name__ == "__main__":
    sys.exit(main())
