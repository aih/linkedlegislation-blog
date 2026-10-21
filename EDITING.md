# Editing posts in a browser

The site ships with [Sveltia CMS](https://sveltiacms.app/), a single-page editor that runs in the
browser. `_admin/index.html` loads it from a CDN, pinned to `@sveltia/cms@0.230.1`. Sveltia reads
and writes this working copy through the browser's File System Access API. There is no proxy
server.

## Requirements

- A Chromium browser: Chrome, Edge, or Brave. Firefox and Safari do not implement the File System
  Access API. Brave needs `brave://flags/#file-system-access-api` set to Enabled.
- The Jekyll gems: `bundle install`.

## Start it

From the repository root:

```bash
bundle exec jekyll serve --config _config.yml,_config.admin.yml --drafts
```

`./edit.sh` runs the same command and opens <http://localhost:4000/_admin/> in Google Chrome once
the server answers. If a server is already running, it only opens the editor. `PORT=4001
./edit.sh` uses another port.

1. Open <http://localhost:4000/_admin/>.
2. Click **Work with Local Repository**.
3. Select the repository root, the folder that contains `.git`. The browser asks for read and
   write access; allow it. An error reading "not a repository root directory" means a subfolder was
   selected.

The browser remembers the folder for the next visit and may ask to confirm access again.

The `backend` block in `_admin/config.yml` names the GitHub repository. The local workflow does not
contact GitHub. **Sign In with GitHub** would need an OAuth client, which this repo does not
configure.

## What it edits

**Posts** — `.md` files in `_posts`, named `YYYY-MM-DD-title.md`. The 100 legacy `.html` posts
imported from Blogger are not listed.

**Drafts** — files in `_drafts`, also named `YYYY-MM-DD-title.md`. They appear on the local site
when `jekyll serve` is run with `--drafts` and are skipped by the production build.

Fields are title, subtitle, author, date, last-updated, tags, thumbnail-img, cover-img, share-img,
image-credits, and the body. Drafts have the same set minus last-updated and share-img.

The body uses the `richtext` widget: a formatting toolbar, drag-and-drop images, and a raw Markdown
view behind the mode toggle. It writes plain Markdown either way. A line break inside a paragraph
(Shift+Enter) is saved as a bare newline, which kramdown's GFM parser renders as `<br>`. Images
dropped into a post are written to `assets/img/uploads/` and referenced as
`/assets/img/uploads/<name>`.

Saving writes the file to disk. Jekyll picks the change up on its next scan, so a reload of
<http://localhost:4000/> shows the post. By default the editor runs no Git commands: `git add`,
`git commit`, and `git push` are yours. **Settings > Developer > Commit Changes to Git** makes a
local commit on each save; it does not push, and it needs `git config --local user.name` and
`user.email` set, since the browser cannot read the global Git config.

Changing `_admin/config.yml`, or pulling new commits, requires a reload of the editor page.

## Draft to published post

1. Create the entry under **Drafts**. It lands in `_drafts/YYYY-MM-DD-title.md`.
2. Review it at <http://localhost:4000/> with the `--drafts` server running.
3. Move the file: `git mv _drafts/YYYY-MM-DD-title.md _posts/YYYY-MM-DD-title.md`. The date in the
   filename sets the permalink, `/:year-:month-:day-:title/`.
4. Commit and push to `main`.

The permalink date comes from the `date` front matter converted to `site.timezone`
(`America/Toronto`), so a post filed late in the day at a western offset publishes on the
following date and the filename date will not always match.

## Deployment

Pushing to `main` triggers `.github/workflows/blog-build-and-publish.yml`. It checks out the
commit, installs the gems from `Gemfile.lock` under Ruby 3.4, runs `bundle exec jekyll build` with
`JEKYLL_ENV=production`, then hands `./blog` to `.github/workflows/blog-publish.sh`, which uploads
to S3 and invalidates the CloudFront distribution.

The build uses `_config.yml` alone. `_admin/` starts with an underscore, so Jekyll skips it unless
`_config.admin.yml` adds it back with `include:`. The editor is never published to
blog.linkedlegislation.org. `_drafts` is likewise excluded from a build without `--drafts`.

## Image credits

Every image the site shows should carry a credit. Credits live in the `image-credits` front matter
of the post or page that shows the image, and render as a list under the body, above the tags.

```yaml
image-credits:
  - role: Thumbnail
    title: The Tower of Babel
    creator: Pieter Bruegel the Elder
    year: 1563
    source: "https://commons.wikimedia.org/wiki/File:..."
    source-name: Wikimedia Commons
    license: Public domain
    license-url: "https://commons.wikimedia.org/wiki/Commons:Licensing"
```

One entry per image. `role` names which image the entry is about — `Thumbnail`, `Cover`, `In body`.
A composite gets one entry for the finished image and one `Cover source` entry per image that went
into it. Every field is optional; an entry renders whatever it has.

| Field | Content |
| --- | --- |
| `role` | Which image, shown in the left column |
| `title` | Image or artwork title, italicised, linked to `source` |
| `creator` | Photographer, painter, or author |
| `year` | Year of the work |
| `source` | URL of the page the image came from |
| `source-name` | Name of that site, rendered as "Via *name*" |
| `license` | `Public domain`, `CC BY 4.0` |
| `license-url` | URL of the licence text |
| `note` | A sentence about the image |

An AI-made image adds the model, its version, and the date it was made:

```yaml
  - role: Cover
    ai-model: Claude Opus 5 in Claude Code
    ai-version: claude-opus-5, Claude Code 2.1.257
    ai-date: 2026-09-01
    ai-role: Composited
```

That renders as an `AI` tag followed by "Composited with Claude Opus 5 in Claude Code, version
claude-opus-5, Claude Code 2.1.257, September 1, 2026." `ai-role` defaults to `Generated`; set it
to `Composited`, `Upscaled`, or whatever the model actually did. `ai-model` is what marks an image
as AI-made — an entry without it renders no tag.

The rendering lives in `_includes/image-credits.html`, pulled in by `_layouts/post.html` and
`_layouts/page.html`. Styling is under `/* --- Image credits --- */` in
`assets/css/custom-styles.css`.

## Blank optional fields

`output: omit_empty_optional_fields: true` in `_admin/config.yml` drops a cleared optional field
from the front matter. `date` is required in both collections and carries a `{{now}}` default;
Jekyll aborts the build on `date: ''`. Posts saved by the earlier Decap editor may still carry `''`
for cleared fields, which renders as empty.

## Adding a field

Add an entry to the `fields:` list of the collection in `_admin/config.yml` with the front matter
key as `name`. Field types are listed at <https://sveltiacms.app/en/docs/fields>.
