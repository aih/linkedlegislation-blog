# Editing posts in a browser

The site ships with [Decap CMS](https://decapcms.org/), a single-page editor that runs in the
browser. `_admin/index.html` loads it from a CDN. Saving goes through
[`decap-server`](https://decapcms.org/docs/decap-proxy/), a small local proxy that writes Markdown
files into this working copy.

## Start it

Two terminals, both from the repository root.

```bash
npx decap-server
```

```bash
bundle exec jekyll serve --config _config.yml,_config.admin.yml --drafts
```

Open <http://localhost:4000/_admin/>. Any browser works, including Firefox and Safari.

The proxy listens on port 8081 and serves the repository it was started in. `PORT=8082 npx
decap-server` moves it; the matching editor setting is `local_backend: {url: ...}` in
`_admin/config.yml`.

`_admin/index.html` pins `decap-cms@3.8.0`. Releases from 3.8.4 up build malformed blob URLs for
media, of the form `https://host/path/blob:https:/host/<uuid>`, which 404. Every media surface
renders from that blob, so the media library grid, the image widget previews, and images in the
body all come up empty. Tracked as
[decap-cms#7639](https://github.com/decaporg/decap-cms/issues/7639).

The pin is why the body is the `markdown` widget rather than `richtext`, which arrived in 3.12.0.

Decap uses the proxy only when the editor page is served from localhost. Loaded from any other
host it falls back to the `backend` block, which is the GitHub API and needs an OAuth client this
repo does not configure. If the editor asks you to log in with GitHub, `decap-server` is not
running.

## What it edits

**Posts** — `.md` files in `_posts`, named `YYYY-MM-DD-title.md`. The 100 legacy `.html` posts
imported from Blogger are not listed.

**Drafts** — files in `_drafts`, also named `YYYY-MM-DD-title.md`. They appear on the local site
when `jekyll serve` is run with `--drafts` and are skipped by the production build.

Fields are title, subtitle, author, date, last-updated, tags, thumbnail-img, cover-img, share-img,
and the body. Drafts have the same set minus last-updated and share-img.

The body uses the `markdown` widget: a formatting toolbar, drag-and-drop images, and a raw
Markdown view behind the mode toggle. It writes plain Markdown either way. Images dropped into a
post are written to `assets/img/uploads/` and referenced as `/assets/img/uploads/<name>`.

Saving writes the file to disk. Jekyll picks the change up on its next scan, so a reload of
<http://localhost:4000/> shows the post. The editor never runs Git: `git add`, `git commit`, and
`git push` are yours.

Changing `_admin/config.yml` requires a reload of the editor page.

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

## Blank optional fields

Decap writes a cleared optional field as an empty string rather than dropping the key. `date: ''`
aborts the Jekyll build, so `date` is a required field in both collections and carries a
`{{now}}` default. For the other optional fields an empty string is merely rendered as empty —
delete the line in the raw Markdown view to remove it.

## Adding a field

Add an entry to the `fields:` list of the collection in `_admin/config.yml` with the front matter
key as `name`. Widget names are at <https://decapcms.org/docs/widgets/>.
