# Finance Montréal — Adaptation Ecosystem Navigator

A tool for FM relationship managers to show SME clients relevant organizations
in Québec's climate-adaptation ecosystem, browsed either as a grid
(Panorama) or a guided "pick a stage, pick a role" finder.

## Files in here

| File | What it is | Do you need to touch it? |
|---|---|---|
| **`index.html`** | The whole website. One file, no install needed. | This is what you upload/host. Don't hand-edit it. |
| **`finance-mtl-navigator.jsx`** | The actual source code. | Only if you're changing how the site *works* (not its content). |
| **`build_index.py`** | Turns the `.jsx` file into `index.html`. | Only run this after editing the `.jsx` file. |
| **`actors_template.csv`** | Starter spreadsheet of all organizations. | Copy into Google Sheets once, to start editing content. |
| **`real-actor-data-backup.txt`** | A backup copy of the real 144-organization list. | Only needed if you want to restore it as the fallback data — see "The red banner" below. |

## 1. Hosting the site

Put **`index.html`** at the root of a GitHub repo, turn on GitHub Pages
(Settings → Pages → deploy from branch, root folder). That's it — no build
step, no dependencies to install.

## 2. Updating the organizations (no code required)

This is how FM staff should make day-to-day changes — adding an org, fixing
a link, editing a description:

1. Copy `actors_template.csv` into a new Google Sheet.
2. Edit it like any spreadsheet. Each row is one organization at one stage —
   an org active in 3 stages gets 3 rows with the same Name.
   - **Stage** must be one of: Risk Understanding, Value / Opportunity
     Assessment, Adaptation Strategy, Strategy Implementation,
     Post-Implementation Analysis.
   - **Functional Role** must be one of: Knowledge & research orgs,
     Technical & advisory providers, Financial institutions, Government &
     public agencies, Ecosystem.
3. **File → Share → Publish to web**, choose CSV format, copy the link it
   gives you.
4. Send that link to whoever maintains the code, so it can be pasted into
   `SHEET_CSV_URL` near the top of `finance-mtl-navigator.jsx` (then
   `finance-mtl-navigator.jsx` → run `build_index.py` → re-upload the new
   `index.html`). After that one-time setup, everyone can just edit the
   Google Sheet — no more code changes needed for content updates.

## 3. The red banner

If you see a red bar across the top of the site, it means it's **not**
showing real data — either no Google Sheet is connected yet, or it couldn't
be reached. This is intentional: it's there so a broken connection is
obvious instead of silently showing stale or fake-looking content.

## 4. Changing the code itself

Only needed for structural changes (new features, design tweaks, adding a
new view) — not for updating organizations.

1. Edit `finance-mtl-navigator.jsx`.
2. Run `python3 build_index.py` to regenerate `index.html`.
3. Re-upload `index.html` to the repo.

Never hand-edit `index.html` directly — it's generated, so edits get wiped
out the next time `build_index.py` runs.
