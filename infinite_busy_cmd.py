#!/usr/bin/env python3
"""
infinite_busy_cmd.py

Prints an infinite stream of coherent sentences / fake process logs
to make a terminal look busy. Optional web-sourced quotes can be enabled
with --use-api (requires 'requests').

Run:
    python infinite_busy_cmd.py
    python infinite_busy_cmd.py --use-api
"""

import random
import time
import argparse
import itertools
import sys
from datetime import datetime

# Optional imports (safe to be missing)
try:
    import requests
except Exception:
    requests = None

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    COLOR = True
except Exception:
    COLOR = False
    # define no-op names
    class _C: pass
    Fore = Style = _C()

# ---------- Config ----------
TICK_MIN = 0.05
TICK_MAX = 0.5

API_QUOTE_FREQ = 0.08   # fraction of lines that will be fetched from web if enabled
CLEAR_SCREEN_EVERY = 200  # lines; set to 0 to disable clearing
SHOW_PROGRESS_BARS = True
PROGRESS_BAR_CHANCE = 0.06  # chance to print a temporary progress bar
SPINNER_CHANCE = 0.04

# ---------- Word banks & templates ----------
adjectives = [
    "optimized", "resilient", "concurrent", "deprecated", "asynchronous",
    "deterministic", "probabilistic", "scalable", "redundant", "compressed",
    "normalized", "encrypted", "authenticated", "verified", "transient",
]

verbs = [
    "initializing", "synchronizing", "compacting", "indexing", "migrating",
    "ingesting", "persisting", "validating", "replicating", "profiling",
    "seeding", "evicting", "flushing", "calibrating", "probing",
]

nouns = [
    "cluster", "shard", "manifest", "cache", "backplane", "registry", "snapshot",
    "transaction log", "pipeline", "matrix", "vector", "protocol", "kernel",
    "artifact", "handshake", "telemetry stream",
]

systems = [
    "auth service", "payment gateway", "ingest worker", "analytics node",
    "time-series engine", "replicator", "orchestrator", "scheduler", "ETL job",
]

error_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE", "CRITICAL"]

sentence_templates = [
    "The {adj} {noun} {verb} {detail}.",
    "{verb_cap} {noun} in the {system} to satisfy integrity checks.",
    "Checkpoint reached: {noun} {verb} with {num} entries processed.",
    "{verb_cap} {noun}... {status}.",
    "User-visible latency improved by {pct}% after {verb} of the {noun}.",
    "Scheduling background {noun} for {system} at {time}.",
    "Rolling update: {noun} on {system} moved to {adj} state.",
    "Telemetry: {num} events/sec for {system} (p90 {ms}ms).",
    "Cache miss ratio at {pct}%, invoking {verb} routine.",
    "{system} reported: {detail}",
]

status_phrases = [
    "OK", "COMPLETE", "FAILED (retrying)", "PENDING", "QUEUED", "ABORTED", "SUCCESS",
    "PARTIAL SUCCESS", "TIMED OUT", "DEFERRED"
]

details = [
    "waiting for quorum", "performing sanity checks", "evicting stale entries",
    "applying adaptive backoff", "rebuilding index", "rotating keys",
    "reconciling state across zones", "compressing deltas", "validating checksums"
]

# ---------- Helpers ----------
def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def pick(template):
    return template.format(
        adj=random.choice(adjectives),
        verb=random.choice(verbs),
        verb_cap=random.choice(verbs).capitalize(),
        noun=random.choice(nouns),
        system=random.choice(systems),
        num=random.randint(1, 99999),
        pct=round(random.uniform(0.1, 99.9), 2),
        ms=random.randint(1, 1200),
        status=random.choice(status_phrases),
        detail=random.choice(details),
        time=datetime.now().strftime("%H:%M:%S"),
    )

def colored(s, color):
    if not COLOR:
        return s
    return color + s + Style.RESET_ALL

def fetch_quote():
    """Fetch a short sentence/quote from the webs. Uses quotable.io if available."""
    if requests is None:
        return None
    try:
        resp = requests.get("https://api.quotable.io/random", timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            return f"\"{data.get('content')}\" — {data.get('author')}"
    except Exception:
        return None
    return None

# ---------- Fancy bits ----------
def progress_bar_simulation(duration=1.4, width=30):
    """Simulates a progress bar across 'duration' seconds."""
    start = time.time()
    while True:
        elapsed = time.time() - start
        frac = min(1.0, elapsed / duration)
        done = int(frac * width)
        bar = "[" + "#" * done + "." * (width - done) + f"] {int(frac*100):3d}%"
        print(colored(f"{now_ts()} {bar}  (updating...)", Fore.GREEN if COLOR else ""), end="\r")
        sys.stdout.flush()
        if frac >= 1.0:
            break
        time.sleep(0.06 + random.random() * 0.08)
    print()  # finish line

def spinner(duration=1.2):
    seq = "|/-\\"
    t0 = time.time()
    i = 0
    while time.time() - t0 < duration:
        print(f"{now_ts()} {seq[i % len(seq)]} working...", end="\r")
        i += 1
        time.sleep(0.08)
    print()

# ---------- Main infinite loop ----------
def main(use_api=False, clear_every=CLEAR_SCREEN_EVERY):
    line_counter = 0
    try:
        while True:
            # occasional screen clear to emulate screens changing
            if clear_every and clear_every > 0 and line_counter and line_counter % clear_every == 0:
                # clear screen (cross-platform)
                if sys.platform.startswith("win"):
                    _ = __import__("os").system("cls")
                else:
                    _ = __import__("os").system("clear")
                print(colored(f"{now_ts()} [SYSTEM] Switched display buffer.", Fore.CYAN) if COLOR else f"{now_ts()} [SYSTEM] Switched display buffer.")

            # sometimes do a progress bar or spinner
            if SHOW_PROGRESS_BARS and random.random() < PROGRESS_BAR_CHANCE:
                progress_bar_simulation(duration=random.uniform(0.8, 2.5))
                line_counter += 3
                continue
            if random.random() < SPINNER_CHANCE:
                spinner(duration=random.uniform(0.6, 1.8))
                line_counter += 2
                continue

            # sometimes fetch a real coherent sentence (quote) from web
            if use_api and requests is not None and random.random() < API_QUOTE_FREQ:
                q = fetch_quote()
                if q:
                    # print as a quoted log
                    print(colored(f"{now_ts()} QUOTE: {q}", Fore.MAGENTA) if COLOR else f"{now_ts()} QUOTE: {q}")
                    line_counter += 1
                    time.sleep(random.uniform(TICK_MIN, TICK_MAX) + 0.15)
                    continue

            # build multi-clause "coherent" sentence: sometimes chain 2 templates
            if random.random() < 0.35:
                s = pick(random.choice(sentence_templates)) + " " + pick(random.choice(sentence_templates)).lower()
            else:
                s = pick(random.choice(sentence_templates))

            # Prepend a fake process id or log-level
            lvl = random.choices(error_levels, weights=[40, 25, 15, 8, 8, 4])[0]
            pid = random.randint(1000, 99999)
            log_line = f"{now_ts()} [{lvl}] (pid:{pid}) {s}"

            # occasionally append a fake command + argument
            if random.random() < 0.22:
                cmd = random.choice([
                    "run-migration", "sync-index", "rotate-keys", "reconcile --fast",
                    "snapshot --compress", "audit --level=high", "throttle --limit=200",
                ])
                log_line += f"  cmd: {cmd}"

            # print with subtle color differences for realism
            if COLOR:
                if lvl in ("ERROR", "CRITICAL"):
                    print(colored(log_line, Fore.RED))
                elif lvl == "WARN":
                    print(colored(log_line, Fore.YELLOW))
                elif lvl == "DEBUG":
                    print(colored(log_line, Fore.CYAN))
                else:
                    print(colored(log_line, Fore.WHITE))
            else:
                print(log_line)

            line_counter += 1
            # small random pause
            time.sleep(random.uniform(TICK_MIN, TICK_MAX) * (0.6 + random.random()))

    except KeyboardInterrupt:
        print("\n" + colored(f"{now_ts()} [SYSTEM] Interrupted by user. Exiting.", Fore.CYAN) if COLOR else f"\n{now_ts()} [SYSTEM] Interrupted by user. Exiting.")
        return

# ---------- CLI ----------
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Infinite busy terminal generator")
    p.add_argument("--use-api", action="store_true", help="Occasionally fetch real sentences from the web (requires requests)")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    p.add_argument("--clear-every", type=int, default=CLEAR_SCREEN_EVERY, help="Clear screen every N lines (0 to disable)")
    args = p.parse_args()

    if args.no_color:
        COLOR = False

    if args.use_api and requests is None:
        print("Warning: requests library not found. Install with: pip install requests")
        print("Continuing without API.")
        args.use_api = False

    main(use_api=args.use_api, clear_every=args.clear_every)
