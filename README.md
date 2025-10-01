# infinite-busy-terminal

A tiny Python utility that prints an infinite stream of coherent, technical-sounding sentences and fake process logs to the terminal
Perfect as a prop for movies, demos, livestream overlays, or just to make a terminal look busy.
![demo](https://github.com/user-attachments/assets/acf6c01a-d244-4ba6-af5e-d0043f670cd6)

This repository includes:

* `infinite_busy_cmd.py` — the main script (single-file, ready to run)
* `requirements.txt` — optional dependencies
* `README.md` — usage, installation, example commands, and tips
* `LICENSE` — MIT (recommended)
* `.gitignore` — standard Python ignores
* `contrib/` — tips for film / prop use cases and example overlays
* `examples/` — sample command invocations and a small Windows .bat wrapper

---

## Quickstart

```bash
# create virtual env (optional)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python infinite_busy_cmd.py
```

### Example Windows command (run in cmd.exe)

```
python infinite_busy_cmd.py --clear-every 150
```

Or build a single-file executable for distribution:

```bash
pip install pyinstaller
pyinstaller --onefile infinite_busy_cmd.py
# dist\infinite_busy_cmd.exe can be distributed for Windows film props
```

---

## Files included (high level)

### `infinite_busy_cmd.py`

Single-file script with options:

* `--use-api` optionally fetches occasional real quotes (requires `requests`)
* `--no-color` disables color output
* `--clear-every N` clear the screen every N lines
* built-in progress bar & spinner simulation

### `requirements.txt`

```
requests
colorama
```

(only if you want colors/API; the script runs without them)

### `LICENSE`

MIT license text. Permissive for film and commercial usage.

### `contrib/film-prop.md`

Short guidelines for film/prop use — recommended font sizes, full-screen display tips, lower-thirds overlay suggestions, and how to record terminal output to video for post.

---

## Tips for "movie" usage

1. Increase `PROGRESS_BAR_CHANCE` and `CLEAR_SCREEN_EVERY` to look dramatic.
2. Use `pyinstaller` to freeze the script into an .exe you can hand to a crew.
3. Pipe output to a file or `ffmpeg` to create a background video (e.g., `python infinite_busy_cmd.py | ffmpeg -f lavfi -i color=c=black:s=1920x1080 -...`).
4. Use `--no-color` and choose a monospaced display font for on-camera clarity.
5. To fake a logged-in session, start the script inside `start /B` on Windows and show the terminal window full-screen.

---

## Contributing

PRs welcome. If you'd like specific domain templates (e.g., compiler logs, network scans, sci-fi console), add a `templates/` folder and submit a PR; include sample outputs and suggested defaults.

---

## License

MIT © Akash Bilgi


