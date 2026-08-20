#!/usr/bin/env python3
"""Repoint blog self-links at the current domain and permalink scheme.

Posts migrated from Blogger still link to each other through the blog's two
former domains, blog.tabulaw.com and blog.linkedlegislation.com, using Blogger
paths of the form /YYYY/MM/slug.html. Jekyll now serves those posts at
/YYYY-MM-DD-slug/, so the old links 404.

A domain sweep moved some of these to blog.linkedlegislation.org without
touching the path, so the current domain carries broken Blogger paths too. Only
links that use a Blogger path are rewritten; ordinary links to the live domain
are left alone.

Each such link is rewritten to a root-relative path, which stays correct if the
domain changes again. Links whose Blogger path matches no post in _posts or
_drafts are left alone and reported.

blogger_orig_url front matter is not touched: it records where a post lived on
Blogger, and is a provenance record rather than a live link.

Exit codes: 0 success, 2 --check found links still needing a fix.
"""

import argparse
import glob
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

BLOG_HOSTS = r"(?:blog\.tabulaw\.com|blog\.linkedlegislation\.(?:com|org))"
# Hosts that are dead outright, for the leftovers report.
FORMER_HOSTS = r"(?:blog\.tabulaw\.com|blog\.linkedlegislation\.com)"
SELF_LINK = re.compile(
    r"https?://" + BLOG_HOSTS + r"/(\d{4})/(\d{2})/([^\s\"'<>)]+?)\.html"
)
# Some links were pasted as Google redirect wrappers, with the real target
# percent-encoded in a query parameter. Replace the whole href, not just the
# inner URL: the wrapper is as dead as the host it points at.
WRAPPED = re.compile(
    r'href="[^"]*%2F%2F(?:blog\.tabulaw\.com|blog\.linkedlegislation\.(?:com|org))'
    r'%2F(\d{4})%2F(\d{2})%2F([^"&]+?)\.html[^"]*"'
)
# Any surviving reference to a former host, for the leftovers report.
ANY_FORMER = re.compile(r"https?://" + FORMER_HOSTS + r"[^\s\"'<>)]*")


# Links that carry no Blogger path, so the map above cannot resolve them.
SPECIAL_CASES = [
    (
        "_posts/2011-06-27-quora-post-nontechnical-barriers-to.html",
        # Pasted from Quora, which split the visible URL with a <wbr>. The href
        # is repointed by the map; this is the text the reader sees.
        re.compile(r"https://blog\.tabulaw\.com/2<wbr[^>]*>\s*</wbr>011/04/\.\.\."),
        "/2011-04-29-congress-commits-to-e-data-formats/",
    ),
    (
        "_posts/2011-08-01-hackathon-anyone-california-opens.html",
        # Blogger label archive. Jekyll serves a tag index at /tags/ instead.
        re.compile(r"https://blog\.tabulaw\.com/search/label/California%20Legislation"),
        "/tags/",
    ),
]


def apply_special_cases(check):
    done = 0
    for path, pattern, target in SPECIAL_CASES:
        src = open(path, encoding="utf-8").read()
        out, n = pattern.subn(target, src)
        if n and not check:
            open(path, "w", encoding="utf-8").write(out)
        done += n
    return done


def site_timezone():
    """Jekyll renders permalink dates in site.timezone, not the file's offset."""
    m = re.search(r'^timezone:\s*"?([\w/]+)"?', open("_config.yml").read(), re.M)
    return ZoneInfo(m.group(1)) if m else None


def build_map(tz):
    """Blogger path 'YYYY/MM/slug' -> current permalink '/YYYY-MM-DD-slug/'.

    The permalink date comes from the post's own date front matter converted to
    the site timezone. A post filed late in the day in a western offset shifts
    to the next day, so the filename date is not always the published date.
    """
    permalinks = {}
    for path in glob.glob("_posts/*") + glob.glob("_drafts/*"):
        m = re.match(
            r"(\d{4})-(\d{2})-(\d{2})-(.+)\.(?:html|md|markdown)$",
            os.path.basename(path),
        )
        if not m:
            continue
        y, mo, d, slug = m.groups()
        stamp = re.search(
            r"^date:\s*'?\"?([\d T:.+-]+?)'?\"?\s*$",
            open(path, encoding="utf-8").read(),
            re.M,
        )
        if stamp and tz:
            try:
                when = datetime.fromisoformat(stamp.group(1).strip())
                if when.tzinfo:
                    when = when.astimezone(tz)
                y, mo, d = f"{when.year:04d}", f"{when.month:02d}", f"{when.day:02d}"
            except ValueError:
                pass
        # Key on the Blogger path, which uses the original publication month.
        permalinks[f"{m.group(1)}/{m.group(2)}/{slug}"] = f"/{y}-{mo}-{d}-{slug}/"
    return permalinks


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    permalinks = build_map(site_timezone())
    print(f"{len(permalinks)} posts and drafts indexed\n")
    special = apply_special_cases(args.check)

    rewritten = 0
    files_changed = []
    unmatched = {}
    leftovers = {}

    for path in sorted(glob.glob("_posts/*") + glob.glob("_drafts/*")):
        src = open(path, encoding="utf-8").read()
        # Shield the provenance line so the rewrite cannot reach it.
        body = re.sub(
            r"^(blogger_orig_url:.*)$",
            lambda m: m.group(1).replace("://", ":\x00//"),
            src,
            flags=re.M,
        )

        def repl(m):
            nonlocal rewritten
            key = f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
            target = permalinks.get(key)
            if not target:
                unmatched.setdefault(m.group(0), []).append(path)
                return m.group(0)
            rewritten += 1
            return target

        def repl_wrapped(m):
            nonlocal rewritten
            key = f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
            target = permalinks.get(key)
            if not target:
                unmatched.setdefault(m.group(0), []).append(path)
                return m.group(0)
            rewritten += 1
            return f'href="{target}"'

        body = WRAPPED.sub(repl_wrapped, body)
        body = SELF_LINK.sub(repl, body)
        body = body.replace(":\x00//", "://")

        if body != src:
            files_changed.append(path)
            if not args.check:
                open(path, "w", encoding="utf-8").write(body)

        after = body if not args.check else body
        for hit in ANY_FORMER.findall(
            re.sub(r"^blogger_orig_url:.*$", "", after, flags=re.M)
        ):
            leftovers.setdefault(hit, []).append(path)

    rewritten += special
    verb = "would rewrite" if args.check else "rewrote"
    print(f"{verb} {rewritten} self-links across {len(files_changed) + bool(special)} files")
    if special:
        print(f"  (including {special} special-case links)")

    if unmatched:
        print(f"\nBlogger paths with no matching post ({len(unmatched)}), left as-is:")
        for url, files in sorted(unmatched.items()):
            print(f"  {url}\n      in {', '.join(sorted(set(files)))}")

    if leftovers:
        print(f"\nOther former-host references ({len(leftovers)}), left as-is:")
        for url, files in sorted(leftovers.items()):
            print(f"  {url}  ({len(files)} file(s))")

    return 2 if (args.check and rewritten) else 0


if __name__ == "__main__":
    sys.exit(main())
