# Plan: reject blank note titles

Goal: `POST /notes` rejects a note whose title is empty or only whitespace with HTTP 400, as issue #12 asks.

1. In `notes.py`, `create_note` calls the existing `validators.require_text(title)` before saving. It already raises `ValidationError` on empty and whitespace-only strings.
2. `app.py` already turns `ValidationError` into HTTP 400.
3. Add `test_blank_title_rejected` to `test_notes.py`, with `""` and `"   "`.
