#!/usr/bin/env bash
# Starts the local Jekyll server with the editor overlay and opens the editor
# in Chrome. Ctrl-C stops the server. See EDITING.md.

set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-4000}"
URL="http://localhost:${PORT}/_admin/"

# Sveltia's local workflow needs a Chromium browser.
open_editor() {
  if open -Ra "Google Chrome" 2>/dev/null; then
    open -a "Google Chrome" "$URL"
  else
    echo "Google Chrome not found; open $URL in Chrome, Edge, or Brave." >&2
  fi
}

# A server is already running: open the editor and stop.
if curl -fs -o /dev/null "$URL"; then
  open_editor
  exit 0
fi

# Opens the editor once the first build finishes and the server answers.
(
  for _ in $(seq 1 180); do
    if curl -fs -o /dev/null "$URL"; then
      open_editor
      exit 0
    fi
    sleep 1
  done
  echo "Server did not answer at $URL after 180 s." >&2
) &

exec bundle exec jekyll serve --config _config.yml,_config.admin.yml --drafts --port "$PORT"
