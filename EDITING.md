# Editing posts in a browser

The site ships with [Sveltia CMS](https://sveltiacms.app/), a single-page editor that runs in the
browser and writes Markdown files into this working copy. It is loaded from a CDN by
`_admin/index.html`; there is nothing to install and no extra process to run.

## Start it

```bash
bundle exec jekyll serve --config _config.yml,_config.admin.yml --drafts
```

Open <http://localhost:4000/_admin/> in Chrome, Edge, or Brave, click **Work with Local
Repository**, and pick the repository root (`/Users/arihershowitz/Documents/workspace/aih/blog`).
The browser remembers the folder for the next session.

Firefox and Safari do not implement the File System Access API and cannot use the local mode.
Brave needs `chrome://flags/#file-system-access-api` enabled.

## What it edits

**Posts** — `.md` files in `_posts`, named `YYYY-MM-DD-title.md`. The 100 legacy `.html` posts
imported from Blogger are not listed.

**Drafts** — files in `_drafts`. They appear on the local site when `jekyll serve` is run with
`--drafts` and are skipped by the production build.

Fields are title, subtitle, author, date, last-updated, tags, thumbnail-img, cover-img, share-img,
and the body. The body editor is WYSIWYG: a formatting toolbar, drag-and-drop images, Markdown
shortcuts such as `##` and `- `, and a Markdown source view behind the mode toggle. Images dropped
into a post are written to `assets/img/uploads/` and referenced as `/assets/img/uploads/<name>`.

Saving writes the file to disk. Jekyll picks the change up on its next scan, so a reload of
<http://localhost:4000/> shows the post. The editor never runs Git: `git add`, `git commit`, and
`git push` are yours, and pushing to `main` triggers the build-and-publish workflow.

Changing `_admin/config.yml` requires a reload of the editor page.

## Adding a field

Add an entry to the `fields:` list of the collection in `_admin/config.yml` with the front matter
key as `name`. Widget names are at <https://sveltiacms.app/en/docs/fields>.

## Deployment

`.github/workflows/blog-build-and-publish.yml` builds with `_config.yml` alone. `_admin/` starts
with an underscore, so Jekyll skips it unless `_config.admin.yml` adds it back with `include:`.
The editor is never published to blog.linkedlegislation.org.

## Decap CMS instead

`_admin/config.yml` is also a valid [Decap CMS](https://decapcms.org/) configuration. To swap:

1. In `_admin/index.html`, comment out the Sveltia `<script>` and uncomment the Decap one.
2. Run `npx decap-server` in a second terminal. It listens on port 8081 and performs the file
   writes that Sveltia does through the browser.
3. Open <http://localhost:4000/_admin/> in any browser.

Decap works in Firefox and Safari. Its body editor is a rich text editor over Markdown with a raw
Markdown toggle.
