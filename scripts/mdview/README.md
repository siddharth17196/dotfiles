# Shared Markdown previews

A local preview page with file tabs, live refresh, and optional side-by-side reading.
Commands from different terminal or agent sessions share the same server. Rendering
uses `markdown-it-py`; everything else uses Python's standard library. No Node,
GitHub API, CDN, or browser package is required.

## Run

Use Python 3.10 or newer from an environment with `markdown-it-py` installed:

```sh
python3 scripts/mdview/mdview.py /path/to/PLAN.md
```

The first command starts a background server and opens
`http://127.0.0.1:8765/`. Later commands add files to the same page:

```sh
python3 scripts/mdview/mdview.py /other/project/REVIEW.md /other/project/NOTES.md
```

For a convenient command, add this function to your shell configuration, adjusting
the interpreter if your package is installed in a virtual environment:

```sh
mdview() {
    python3 /Users/siddharth/projects/dotfiles/scripts/mdview/mdview.py "$@"
}
```

Then use `mdview PLAN.md` from any session. Click **Side by side** and select
the second file to compare. Tabs retain their scroll position; the browser remembers
your active files and split layout. Closing a tab removes it from the shared page.
The file list lasts until the server stops; restarting begins with an empty list.

```sh
mdview                  # Reopen the browser page
mdview --no-browser PLAN.md
mdview --stop           # Stop the background server
mdview --port 8766 PLAN.md  # Separate workspace, if needed
```

The server continues running when the invoking terminal closes. Startup errors are
logged to `mdview-<user-id>-<port>.log` under `$TMPDIR`, or `/tmp`.
For debugging, `mdview --serve PLAN.md` runs it in the foreground; use Ctrl+C to stop.

## Links and formatting

Relative links and images resolve against the original file location. The serving
boundary is the closest Git root (including Git worktrees), or the file's directory
for standalone files. If standalone files link to a parent directory, select that
boundary explicitly:

```sh
mdview --root /path/to/notes /path/to/notes/subfolder/PLAN.md
```

Clicking a relative Markdown link opens it in another tab in the shared page.
Heading fragments work. Modified clicks use normal browser navigation. Other links
open a separate browser tab. Only Markdown, common image formats, and PDF assets
within registered roots are served; paths and symlinks cannot escape those roots.

Supports headings and anchors, tables, task lists, strikethrough, blockquotes,
images, links, and fenced code blocks. The initial theme follows your system's
light/dark preference. Use the **Light mode** / **Dark mode** button to switch;
your choice is remembered and applies to all preview panes.
Code blocks are formatted without syntax coloring. Raw HTML is escaped; Mermaid,
math rendering, GitHub alerts, and bare-URL autolinking are not implemented.

Simple YAML front matter at the very start of a file is displayed as a metadata
table. Only flat key/value fields and simple quoted strings are interpreted;
complex metadata is shown as an escaped code block. A closing `---` delimiter
is required. Separators elsewhere in a document keep their Markdown meaning.

Files are checked once per second. Only changed Markdown is rendered again, and
only the affected preview updates. Atomic saves and temporary deletion are handled;
the last preview remains visible until the file becomes readable again. Rendering
and bundled UI assets make no external requests. External images explicitly linked
in your Markdown are still fetched by the browser.

The server binds only to `127.0.0.1` and rejects foreign browser origins and hosts.
It has no remote-access or authentication mode.

## Verify

```sh
python3 -m unittest discover -s scripts/mdview -v
```
