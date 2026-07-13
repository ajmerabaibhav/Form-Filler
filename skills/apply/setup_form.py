#!/usr/bin/env python3
"""Full-screen terminal form for /apply setup and /apply update.

A boxed table: every field is a row, you fill values in place, and a leopard
walks along the top edge as you progress. Date of birth opens a calendar
picker. Saves to ~/application-agent/store/basics.md.

Pure standard library (curses + calendar). No network. Nothing leaves this machine.

Run:  python3 setup_form.py            (full-screen form; remembers previous answers)
      python3 setup_form.py --simple   (plain question-by-question fallback)
"""

import calendar as cal
import datetime as dt
import os
import re
import sys
import time

BASE = os.path.expanduser(os.environ.get("APPLY_BASE", "~/application-agent"))
BASICS = os.path.join(BASE, "store", "basics.md")
LEOPARD = "🐆"
DOB_KEY = "Date of birth"

# (short label, storage key, hint) — key None marks a section header row
FIELDS = [
    ("Identity", None, None),
    ("First name", "First name", ""),
    ("Last name", "Last name", ""),
    ("Display name", "Preferred/display name", "optional"),
    ("Date of birth", DOB_KEY, "Enter opens calendar"),
    ("Gender", "Gender (as you give it on forms)", "optional"),
    ("Contact", None, None),
    ("Email", "Email", ""),
    ("Phone", "Phone (with country code)", "+91 ..."),
    ("City", "City", ""),
    ("Country", "Country of residence", ""),
    ("Nationality", "Nationality / citizenship", "optional"),
    ("Links", None, None),
    ("LinkedIn", "LinkedIn", "full URL"),
    ("X (Twitter)", "X (Twitter)", "optional"),
    ("GitHub", "GitHub", "optional"),
    ("Website", "Personal website / portfolio", "optional"),
    ("Telegram/Discord", "Telegram / Discord (if you use them for communities)", "optional"),
    ("Current status", None, None),
    ("Role & org", "Current role & organisation (e.g. \"Founder, Acme\" / \"Student, XYZ University\")", "Founder, Acme"),
    ("One-line bio", "One-line bio (how you introduce yourself on a form)", "sound like you"),
    ("Extras", None, None),
    ("Dietary", "Dietary preference (events ask)", "optional"),
    ("T-shirt size", "T-shirt size (hackathons ask)", "optional"),
    ("Emergency contact", "Emergency contact (residencies ask)", "name + phone"),
]
INPUT_FIELDS = [f for f in FIELDS if f[1]]
TOTAL = len(INPUT_FIELDS)


def load_existing():
    values = {}
    if not os.path.exists(BASICS):
        return values
    with open(BASICS, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"-\s*(.+?):\s*(.*)$", line.strip())
            if m and m.group(2).strip():
                values[m.group(1).strip()] = m.group(2).strip()
    return values


def save(values):
    os.makedirs(os.path.dirname(BASICS), exist_ok=True)
    lines = ["# Basics — the fields every form asks for", "",
             "(Filled by the setup form. The agent uses this to auto-fill "
             "boilerplate fields on any form. Re-run the form any time to update.)", ""]
    first = True
    for label, key, hint in FIELDS:
        if key is None:
            if not first:
                lines.append("")
            lines.append(f"## {label}")
            first = False
        else:
            lines.append(f"- {key}: {values.get(key, '')}")
    lines.append("")
    with open(BASICS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def parse_dob(text):
    for fmt in ("%d %b %Y", "%d %B %Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return dt.date.fromisoformat(dt.datetime.strptime(text.strip(), fmt).date().isoformat())
        except (ValueError, AttributeError):
            continue
    return None


def read_key(stdscr):
    """get_wch with manual ESC-sequence parsing, so arrows work on any terminal."""
    import curses
    ch = stdscr.get_wch()
    if not (isinstance(ch, str) and ch == "\x1b"):
        return ch
    seq = ""
    stdscr.nodelay(True)
    try:
        for _ in range(3):
            c2 = stdscr.get_wch()
            if isinstance(c2, str):
                seq += c2
                if seq and seq[-1].isalpha():
                    break
            else:
                break
    except curses.error:
        pass
    stdscr.nodelay(False)
    if seq.startswith("[") and len(seq) >= 2:
        return {"A": 259, "B": 258, "C": 261, "D": 260}.get(seq[1], "\x1b")
    return "\x1b"


# ── calendar picker overlay ──────────────────────────────────────────────

def pick_date(stdscr, current_text):
    import curses
    sel = parse_dob(current_text or "") or dt.date(2000, 1, 1)
    C_TITLE = curses.color_pair(1)
    C_TRACK = curses.color_pair(3)
    while True:
        h, w = stdscr.getmaxyx()
        bw, bh = 30, 13
        x0, y0 = max(1, (w - bw) // 2), max(1, (h - bh) // 2)
        win = stdscr.subwin(bh, bw, y0, x0)
        win.erase()
        win.box()
        head = f" {cal.month_name[sel.month]} {sel.year} "
        win.addstr(0, (bw - len(head)) // 2, head, C_TITLE | curses.A_BOLD)
        win.addstr(1, 2, "Mo Tu We Th Fr Sa Su", curses.A_DIM)
        y = 2
        for week in cal.monthcalendar(sel.year, sel.month):
            x = 2
            for day in week:
                if day:
                    attr = curses.A_REVERSE | curses.A_BOLD if day == sel.day else curses.A_NORMAL
                    win.addstr(y, x, f"{day:2d}", attr)
                x += 3
            y += 1
        win.addstr(bh - 3, 2, sel.strftime("→ %d %b %Y"), C_TRACK | curses.A_BOLD)
        win.addstr(bh - 2, 2, "←↑↓→ day  [ ] month  { } year", curses.A_DIM)
        win.addstr(bh - 1, 3, " Enter pick · Esc cancel ", curses.A_DIM)
        win.refresh()

        ch = read_key(stdscr)
        days_in = lambda y_, m_: cal.monthrange(y_, m_)[1]
        if isinstance(ch, str) and ch in ("\n", "\r"):
            return sel.strftime("%d %b %Y")
        if isinstance(ch, str) and ch == "\x1b":
            return None
        if isinstance(ch, int) and ch == 260 or ch == "h":          # left
            sel -= dt.timedelta(days=1)
        elif isinstance(ch, int) and ch == 261 or ch == "l":        # right
            sel += dt.timedelta(days=1)
        elif isinstance(ch, int) and ch == 259 or ch == "k":        # up
            sel -= dt.timedelta(days=7)
        elif isinstance(ch, int) and ch == 258 or ch == "j":        # down
            sel += dt.timedelta(days=7)
        elif ch == "[":                                             # month back
            m2, y2 = (12, sel.year - 1) if sel.month == 1 else (sel.month - 1, sel.year)
            sel = dt.date(y2, m2, min(sel.day, days_in(y2, m2)))
        elif ch == "]":                                             # month fwd
            m2, y2 = (1, sel.year + 1) if sel.month == 12 else (sel.month + 1, sel.year)
            sel = dt.date(y2, m2, min(sel.day, days_in(y2, m2)))
        elif ch == "{":
            sel = dt.date(sel.year - 1, sel.month, min(sel.day, days_in(sel.year - 1, sel.month)))
        elif ch == "}":
            sel = dt.date(sel.year + 1, sel.month, min(sel.day, days_in(sel.year + 1, sel.month)))
        stdscr.touchwin()


# ── full-screen table form ───────────────────────────────────────────────

def run_form(stdscr, values):
    import curses
    curses.curs_set(1)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    C_TITLE, C_OK, C_TRACK = (curses.color_pair(i) for i in (1, 2, 3))

    idx, buf, top, anim_pos = 0, None, 0, -1.0
    label_w = max(len(l) for l, k, _ in FIELDS if k) + 2

    def filled_count():
        return sum(1 for _, k, _ in INPUT_FIELDS if values.get(k, "").strip())

    def draw(glide=False):
        nonlocal top, anim_pos
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        stdscr.box()
        sep_x = 3 + label_w + 1

        title = " application agent · your basics "
        stdscr.addstr(0, max(2, (w - len(title)) // 2), title, C_TITLE | curses.A_BOLD)

        # leopard walks along the TOP of the box
        track_w = w - 14
        done = filled_count()
        target = (track_w - 1) * done / max(1, TOTAL)
        if anim_pos < 0 or not glide:
            anim_pos = target
        steps = [target] if anim_pos == target else \
            [anim_pos + (target - anim_pos) * s / 6 for s in range(1, 7)]

        # table header + divider under the leopard row
        rows_area_top = 4
        stdscr.addstr(2, 3, "Field".ljust(label_w), curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(2, sep_x + 2, "Your answer", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.hline(3, 1, curses.ACS_HLINE, w - 2)

        rows = h - rows_area_top - 2
        active_row = FIELDS.index(INPUT_FIELDS[idx])
        if active_row < top:
            top = active_row
        if active_row >= top + rows:
            top = active_row - rows + 1

        y = rows_area_top
        cursor_yx = None
        for row in range(top, min(top + rows, len(FIELDS))):
            label, key, hint = FIELDS[row]
            if key is None:
                stdscr.hline(y, 1, curses.ACS_HLINE, w - 2)
                stdscr.addstr(y, 3, f" {label} ", C_TITLE | curses.A_BOLD)
            else:
                is_active = (FIELDS[row] == INPUT_FIELDS[idx])
                mark = "*" if values.get(key, "").strip() else "?"
                attr = curses.A_REVERSE if is_active else curses.A_NORMAL
                stdscr.addstr(y, 3, f"{mark} {label}".ljust(label_w)[:label_w], attr)
                stdscr.addch(y, sep_x, curses.ACS_VLINE)
                shown = buf if (is_active and buf is not None) else values.get(key, "")
                vx = sep_x + 2
                if shown:
                    stdscr.addstr(y, vx, shown[: w - vx - 3], C_OK)
                elif hint and is_active:
                    stdscr.addstr(y, vx, hint[: w - vx - 3], curses.A_DIM)
                if is_active:
                    cursor_yx = (y, min(vx + len(shown or ""), w - 3))
            y += 1

        helpline = " type · Enter next · ↑↓ move · Enter on DOB = calendar · Ctrl+D finish "
        stdscr.addstr(h - 1, max(2, (w - len(helpline)) // 2), helpline[: w - 4], curses.A_DIM)

        for pos in steps:
            p = int(pos)
            track = "~" * p + LEOPARD + "·" * max(0, track_w - p - 2)
            stdscr.addstr(1, 3, track[: w - 14], C_TRACK)
            stdscr.addstr(1, w - 9, f"{int(100 * done / TOTAL):3d}%", C_TITLE | curses.A_BOLD)
            stdscr.refresh()
            if len(steps) > 1:
                time.sleep(0.04)
        anim_pos = target
        if cursor_yx:
            stdscr.move(*cursor_yx)
        stdscr.refresh()

    draw()
    while True:
        key = INPUT_FIELDS[idx][1]
        ch = read_key(stdscr)
        is_enter = (isinstance(ch, str) and ch in ("\n", "\r")) or (isinstance(ch, int) and ch in (10, 13, 343))
        if is_enter:
            if key == DOB_KEY and (buf is None or buf == ""):
                picked = pick_date(stdscr, values.get(DOB_KEY, ""))
                if picked:
                    values[DOB_KEY] = picked
                buf = None
                stdscr.clear()
            elif buf is not None:
                values[key] = buf.strip()
                buf = None
            if idx < TOTAL - 1:
                idx += 1
                draw(glide=True)
            else:
                return True
        elif ch == "\x04":                                          # Ctrl+D
            if buf is not None:
                values[key] = buf.strip()
            return True
        elif isinstance(ch, int) and ch == 259:                     # up
            if buf is not None:
                values[key] = buf.strip(); buf = None
            idx = max(0, idx - 1); draw()
        elif (isinstance(ch, int) and ch == 258) or ch == "\t":     # down/tab
            if buf is not None:
                values[key] = buf.strip(); buf = None
            idx = min(TOTAL - 1, idx + 1); draw()
        elif ch in ("\x7f", "\b") or (isinstance(ch, int) and ch == 263):
            buf = (values.get(key, "") if buf is None else buf)[:-1]
            draw()
        elif isinstance(ch, str) and ch.isprintable():
            buf = ("" if buf is None else buf) + ch
            draw()
        elif isinstance(ch, int) and ch == 410:                     # resize
            stdscr.clear(); draw()


def simple_mode(values):
    """Plain sequential fallback (no curses)."""
    DIM, BOLD, RESET, GREEN, YELLOW, CYAN = "\033[2m", "\033[1m", "\033[0m", "\033[32m", "\033[33m", "\033[36m"
    print(f"\n  {BOLD}{CYAN}application agent · your basics{RESET}")
    print(f"  {DIM}Saved to {BASICS} — nothing is uploaded. Enter skips/keeps.{RESET}\n")
    done = 0
    for label, key, hint in FIELDS:
        if key is None:
            print(f"\n  {BOLD}{label}{RESET}")
            continue
        current = values.get(key, "")
        suffix = f" {DIM}[{current}]{RESET}" if current else (f" {DIM}({hint}){RESET}" if hint else "")
        try:
            answer = input(f"  {GREEN}?{RESET} {label}{suffix}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YELLOW}Paused — progress saved. Run me again to continue.{RESET}")
            save(values)
            return
        if answer:
            values[key] = answer
        done += 1
        pos = int(30 * done / TOTAL)
        print(f"  {YELLOW}{'~' * pos}{LEOPARD}{'·' * (30 - pos)}{RESET} {DIM}{int(100 * done / TOTAL)}%{RESET}")
    save(values)


def main():
    values = load_existing()
    use_simple = "--simple" in sys.argv or not sys.stdout.isatty()
    if not use_simple:
        try:
            import curses
            curses.wrapper(run_form, values)
            save(values)
        except Exception:
            simple_mode(values)
    else:
        simple_mode(values)

    filled = sum(1 for v in values.values() if v)
    print(f"\n  {LEOPARD} \033[1m\033[32mThe leopard made it home. {filled}/{TOTAL} fields saved.\033[0m")
    print(f"  \033[2mSaved to {BASICS} — yours, on your disk, forever editable.\033[0m")
    print(f"\n  \033[1mNext:\033[0m in Claude Code, just paste any application link:")
    print(f"    \033[36m/apply <form-url>\033[0m\n")


if __name__ == "__main__":
    main()
