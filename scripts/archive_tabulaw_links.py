#!/usr/bin/env python3
"""Turn links to retired Tabulaw sites into plain text.

The Tabulaw application domains — calaw.tabulaw.com, www.tabulaw.com,
tabulaw.com, pdf2html.tabulaw.com, rasa.tabulaw.com — no longer resolve, and
nothing replaced them. Presenting them as live hyperlinks invites a click that
cannot succeed.

Each anchor is unwrapped to its own text, followed by the host and an archived
marker: "here [pdf2html.tabulaw.com - archived]". When the link text is already
the host, the host is not repeated: "calaw.tabulaw.com [archived]".

One reference is a bare URL in prose rather than an anchor; it gets the marker
without being unwrapped. One more was mangled by Blogger's draft editor into
https://draft.blogger.com/www.tabulaw.com and is handled as the Tabulaw link it
was meant to be.

Exit codes: 0 success, 2 --check found links still needing a change.
"""

import argparse
import glob
import re
import sys

HOST = r"(?:[a-z0-9-]+\.)*tabulaw\.com"
# Blogger's draft editor rewrote some bare domains as draft.blogger.com/<domain>.
MANGLED = r"(?:https?://draft\.blogger\.com/)?"
ANCHOR = re.compile(
    r'<a\b[^>]*?href="' + MANGLED + r'(?P<url>(?:https?://)?' + HOST + r'[^"]*)"'
    r'[^>]*>(?P<text>.*?)</a>',
    re.S | re.I,
)
BARE = re.compile(r"(?<![\"'>])(?P<url>https?://" + HOST + r"/[^\s\"'<>)]+)")
MARKER = "archived"


def hostname(url):
    return re.match(r"(?:https?://)?([^/]+)", url).group(1)


def plain(html):
    return re.sub(r"<[^>]+>", "", html).strip()


def unwrap(m):
    host = hostname(m.group("url"))
    text = m.group("text")
    label = plain(text).rstrip("/").lower()
    if label == host or label == host.removeprefix("www."):
        return f"{text} [{MARKER}]"
    return f"{text} [{host} - {MARKER}]"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    anchors = bare = 0
    files = []
    for path in sorted(glob.glob("_posts/*") + glob.glob("_drafts/*")):
        src = open(path, encoding="utf-8").read()
        out, n = ANCHOR.subn(unwrap, src)
        anchors += n
        # Only prose URLs remain now that anchors are unwrapped; skip any that
        # already carry the marker so re-runs are a no-op.
        def mark(m):
            nonlocal bare
            tail = out[m.end() : m.end() + 20]
            if tail.lstrip().startswith(f"[{MARKER}]"):
                return m.group(0)
            bare += 1
            return f"{m.group('url')} [{MARKER}]"

        out = BARE.sub(mark, out)
        if out != src:
            files.append(path)
            if not args.check:
                open(path, "w", encoding="utf-8").write(out)

    verb = "would change" if args.check else "changed"
    print(f"{verb} {anchors} anchors and {bare} bare URLs across {len(files)} file(s)")
    return 2 if (args.check and (anchors or bare)) else 0


if __name__ == "__main__":
    sys.exit(main())
