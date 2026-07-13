# Leverage tracker

Measures what this system produces for you, so it improves over time.

## log.jsonl — one line per application
```json
{"date": "2026-07-01", "target": "Program X", "url": "...", "questions": 6, "words_drafted": 800, "minutes_saved": 50, "status": "submitted", "outcome": "pending", "framings": ["..."], "notes": ""}
```
- status: drafted | filled | submitted | abandoned
- outcome: pending | accepted | rejected | waitlisted | interview

## learnings.md — the improvement loop
When an outcome lands, /apply log records which framing was used and whether it won, as explicit WORKS/MISTAKE rules. The drafting stage reads this file before writing anything, so every acceptance or rejection sharpens the next application.
