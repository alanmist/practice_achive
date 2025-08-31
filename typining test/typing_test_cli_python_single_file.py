#!/usr/bin/env python3
"""
Typing Test CLI
----------------
A single-file, cross-platform typing test you can run in the terminal.

Features
- Modes: fixed number of words (default) or timed test (e.g., 60s)
- Calculates raw WPM (5 chars = 1 word), accuracy %, and net WPM
- Highlights mistakes with a colored diff (ANSI; auto-disables if unsupported)
- Difficulty levels (easy/medium/hard) with built-in word lists
- Optional custom text or file input
- Saves results history to ~/.typing_test_history.json (disable with --no-save)
- View past results with --history N

Usage examples
  python typing_test.py                     # 25-word test (default)
  python typing_test.py --words 50          # 50-word test
  python typing_test.py --mode time --time 60  # 60-second timed test
  python typing_test.py --show-diff         # show colored diff after result
  python typing_test.py --difficulty hard   # harder word list
  python typing_test.py --text "your custom text here"
  python typing_test.py --file path/to/prompt.txt
  python typing_test.py --history 10        # show last 10 results and exit

Notes
- On Windows, ANSI color is enabled automatically when possible.
- Timed mode uses per-keystroke capture to stop exactly at the time limit.
- Words mode captures a single line: type the displayed line and press Enter.

"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import random
import sys
import textwrap
import time
from datetime import datetime

# --- Platform-specific imports for timed keystroke capture ---
_ON_WINDOWS = os.name == "nt"
if _ON_WINDOWS:
    try:
        import msvcrt  # type: ignore
        import ctypes
        import ctypes.wintypes
    except Exception:  # pragma: no cover (fallbacks if not available)
        msvcrt = None  # type: ignore
else:
    import select
    import tty
    import termios

HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".typing_test_history.json")

# --- Minimal word lists ---
_WORDS_EASY = (
    "the of and to in is you that it he was for on are as with his they I at be this".split()
    + "have from or one had by word but not what all were we when your can said there use an each which she do how their if".split()
)
_WORDS_MEDIUM = (
    "time person year way day thing man world life hand part child eye woman place work week case point government company number group problem fact".split()
    + "become interest possible beautiful though enough question against moment certain reason language believe remember character natural rather".split()
)
_WORDS_HARD = (
    "phenomenon ubiquitous ambiguous paradigm serendipity meticulous quintessential juxtapose ephemeral conundrum ubiquitous rhetoric empirical".split()
    + "aesthetic mnemonic idiosyncratic ubiquitous resilience perseverance conscientious echelon labyrinthine quintessentially".split()
)

PUNCT = [",", ".", ";", ":"]

# --- ANSI color helpers ---
class Ansi:
    RESET = "\033[0m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

    @staticmethod
    def supported(stdout_is_tty: bool) -> bool:
        if not stdout_is_tty:
            return False
        if _ON_WINDOWS:
            # Try enabling Virtual Terminal Processing for ANSI colors
            try:
                kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
                handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
                mode = ctypes.wintypes.DWORD()
                if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                    new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
                    kernel32.SetConsoleMode(handle, new_mode)
                    return True
            except Exception:
                return False
            return False
        return True


def c(s: str, color: str, enable: bool) -> str:
    return f"{color}{s}{Ansi.RESET}" if enable else s


# --- Utility functions ---
def wrap(text: str, width: int = 80) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def load_history() -> list[dict]:
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(entry: dict, enable_save: bool = True) -> None:
    if not enable_save:
        return
    hist = load_history()
    hist.append(entry)
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# --- Prompt generation ---

def build_prompt(words: int, difficulty: str = "medium", punct: bool = False, seed: int | None = None) -> str:
    rng = random.Random(seed)
    if difficulty == "easy":
        pool = _WORDS_EASY
    elif difficulty == "hard":
        pool = _WORDS_HARD
    else:
        pool = _WORDS_MEDIUM

    chosen = [rng.choice(pool) for _ in range(words)]
    if punct and words >= 6:
        # sprinkle a little punctuation
        for i in range(5, len(chosen), 6):
            chosen[i] += rng.choice(PUNCT)
    return " ".join(chosen)


# --- Metrics ---

def compute_metrics(typed: str, target: str, elapsed_s: float) -> dict:
    typed = typed.rstrip("\n")
    target = target.rstrip("\n")
    minutes = max(elapsed_s, 1e-9) / 60.0
    raw_wpm = (len(typed) / 5.0) / minutes

    # Char-by-char correctness over the target text length
    correct = sum(a == b for a, b in zip(typed, target))
    accuracy = (correct / max(len(target), 1)) * 100.0
    net_wpm = raw_wpm * (accuracy / 100.0)
    return {
        "elapsed_s": elapsed_s,
        "raw_wpm": raw_wpm,
        "accuracy": accuracy,
        "net_wpm": net_wpm,
        "chars_typed": len(typed),
        "target_chars": len(target),
        "correct_chars": correct,
    }


def diff_colored(typed: str, target: str, enable_color: bool) -> str:
    out = []
    for op, a, b in _opcodes(typed, target):
        if op == "equal":
            out.append(c(a, Ansi.DIM, enable_color))
        elif op == "replace":
            out.append(c(b, Ansi.RED, enable_color))
        elif op == "delete":
            # missing char from typed
            out.append(c(b, Ansi.RED, enable_color))
        elif op == "insert":
            # extra char in typed (mark with yellow)
            out.append(c(a, Ansi.YELLOW, enable_color))
    return "".join(out)


def _opcodes(typed: str, target: str):
    s = difflib.SequenceMatcher(a=typed, b=target, autojunk=False)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "equal":
            yield (tag, typed[i1:i2], target[j1:j2])
        elif tag == "replace":
            yield (tag, typed[i1:i2], target[j1:j2])
        elif tag == "delete":
            yield (tag, typed[i1:i2], target[j1:j2])
        elif tag == "insert":
            yield (tag, typed[i1:i2], target[j1:j2])


# --- Input capture ---

def capture_words_mode() -> str:
    # Single line entry; user presses Enter when done
    try:
        return input()
    except EOFError:
        return ""


def capture_timed_mode(seconds: int) -> str:
    deadline = time.time() + max(1, seconds)
    buf: list[str] = []

    def remaining() -> int:
        return max(0, int(deadline - time.time()))

    print()
    print("Start typing. The test will stop automatically when time is up.")
    print()

    if _ON_WINDOWS and msvcrt is not None:
        # Windows: use msvcrt.getwch for per-keystroke capture
        while time.time() < deadline:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    buf.append("\n")
                elif ch == "\x08":  # Backspace
                    if buf:
                        buf.pop()
                        # Erase a character from console
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    buf.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            # lightweight countdown indicator
            sys.stdout.write(f"\r⏱  {remaining():>2}s ")
            sys.stdout.flush()
            time.sleep(0.01)
        print("\nTime!")
        return "".join(buf)

    # POSIX: raw mode + select
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while time.time() < deadline:
            r, _, _ = select.select([sys.stdin], [], [], 0.01)
            if r:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    buf.append("\n")
                elif ch == "\x7f":  # Backspace on POSIX
                    if buf:
                        buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    buf.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            sys.stdout.write(f"\r⏱  {remaining():>2}s ")
            sys.stdout.flush()
        print("\nTime!")
        return "".join(buf)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# --- Main flow ---

def main():
    parser = argparse.ArgumentParser(description="Typing Test CLI")
    parser.add_argument("--mode", choices=["words", "time"], default="words",
                        help="Test mode: fixed word count or timed")
    parser.add_argument("--words", type=int, default=25,
                        help="Number of words for words-mode")
    parser.add_argument("--time", dest="seconds", type=int, default=60,
                        help="Seconds for time-mode")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium")
    parser.add_argument("--punct", action="store_true", help="Include some punctuation in generated text")
    parser.add_argument("--text", type=str, help="Use custom text (overrides generation)")
    parser.add_argument("--file", type=str, help="Load prompt text from a file")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--show-diff", action="store_true", help="Show a colored diff after the test")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--no-save", action="store_true", help="Do not save results to history")
    parser.add_argument("--history", type=int, metavar="N", help="Show last N history entries and exit")

    args = parser.parse_args()

    # History view
    if args.history:
        hist = load_history()
        if not hist:
            print("No history yet.")
            return
        for entry in hist[-args.history:]:
            ts = entry.get("timestamp", "?")
            mode = entry.get("mode", "?")
            raw = entry.get("raw_wpm", 0.0)
            acc = entry.get("accuracy", 0.0)
            net = entry.get("net_wpm", 0.0)
            detail = entry.get("detail", "")
            print(f"[{ts}] {mode:5}  raw: {raw:6.1f}  acc: {acc:6.1f}%  net: {net:6.1f}  {detail}")
        return

    # Color support
    enable_color = Ansi.supported(sys.stdout.isatty()) and (not args.no_color)

    # Build or load prompt text
    if args.text:
        prompt_text = args.text.strip().replace("\n", " ")
        detail = "custom-text"
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip().replace("\n", " ")
            detail = f"file:{args.file}"
        except Exception as e:
            print(f"Failed to read file: {e}")
            sys.exit(1)
    else:
        if args.mode == "time":
            # make a long stream so you don't run out mid-test
            wc = max(300, int(args.seconds * 6))
        else:
            wc = max(5, int(args.words))
        prompt_text = build_prompt(wc, args.difficulty, args.punct, seed=args.seed)
        detail = f"{args.difficulty}"

    # Display prompt
    print()
    print(c("Target text:", Ansi.CYAN + Ansi.BOLD, enable_color))
    print(wrap(prompt_text))
    print()

    # Countdown
    for n in (3, 2, 1):
        sys.stdout.write(c(f"Starting in {n}...\r", Ansi.DIM, enable_color))
        sys.stdout.flush()
        time.sleep(0.9)
    sys.stdout.write(" " * 30 + "\r")
    sys.stdout.flush()

    # Capture
    if args.mode == "time":
        start = time.time()
        typed = capture_timed_mode(args.seconds)
        elapsed = min(time.time() - start, float(args.seconds))
    else:
        print("Type the line ABOVE, then press Enter:")
        print()
        start = time.time()
        typed = capture_words_mode()
        elapsed = time.time() - start

    # Results
    metrics = compute_metrics(typed, prompt_text, elapsed)
    raw = metrics["raw_wpm"]
    acc = metrics["accuracy"]
    net = metrics["net_wpm"]

    print()
    print(c("Results:", Ansi.BOLD, enable_color))
    print(f"  Time: {metrics['elapsed_s']:.2f}s")
    print(f"  Raw WPM: {raw:.1f}")
    print(f"  Accuracy: {acc:.1f}%")
    print(f"  Net WPM: {net:.1f}")

    if args.show_diff:
        print()
        print(c("Diff (yellow = extra you typed, red = incorrect/missing):", Ansi.DIM, enable_color))
        print(diff_colored(typed, prompt_text, enable_color))

    # Save history
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": ts,
        "mode": f"{args.mode}({args.seconds}s)" if args.mode == "time" else f"{args.mode}({args.words}w)",
        "raw_wpm": raw,
        "accuracy": acc,
        "net_wpm": net,
        "elapsed_s": metrics["elapsed_s"],
        "detail": detail,
    }
    save_history(entry, enable_save=(not args.no_save))

    print()
    if not args.no_save:
        print(c(f"Saved to history at {HISTORY_PATH}", Ansi.DIM, enable_color))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
