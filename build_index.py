#!/usr/bin/env python3
"""
Builds /mnt/user-data/outputs/index.html from
/mnt/user-data/outputs/finance-mtl-navigator.jsx

- Strips the `import ... from "react"` / `"lucide-react"` lines
- Removes `export default` before `function App()`
- Prepends hand-drawn inline SVG replacements for the 8 lucide-react icons used
- Wraps everything in a single HTML file loading React/ReactDOM/Babel (stable 7.x) from cdnjs,
  Tailwind from its play CDN, and Montserrat from Google Fonts.
"""

SRC = "/mnt/user-data/outputs/finance-mtl-navigator.jsx"
OUT = "/mnt/user-data/outputs/index.html"

IMPORT_BLOCK = '''import React, { useState, useEffect, useRef, useMemo } from "react";
import {
  Globe,
  X,
  ExternalLink,
  ChevronDown,
  Search,
  Compass,
  LayoutGrid,
  ArrowRight,
} from "lucide-react";
import Papa from "papaparse";

'''

ICONS_CODE = '''
/* ============================================================
   INLINE ICONS (small hand-drawn set in Lucide's stroke style,
   replacing the lucide-react npm import for a build-free page)
   ============================================================ */
function IconBase({ size = 16, color = "currentColor", style, children }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color}
      strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={style}>
      {children}
    </svg>
  );
}
function Globe(props) {
  return (
    <IconBase {...props}>
      <circle cx="12" cy="12" r="10" />
      <line x1="2" y1="12" x2="22" y2="12" />
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
    </IconBase>
  );
}
function X(props) {
  return (
    <IconBase {...props}>
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </IconBase>
  );
}
function ExternalLink(props) {
  return (
    <IconBase {...props}>
      <path d="M15 3h6v6" />
      <line x1="10" y1="14" x2="21" y2="3" />
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    </IconBase>
  );
}
function ChevronDown(props) {
  return (
    <IconBase {...props}>
      <polyline points="6 9 12 15 18 9" />
    </IconBase>
  );
}
function Search(props) {
  return (
    <IconBase {...props}>
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </IconBase>
  );
}
function Compass(props) {
  return (
    <IconBase {...props}>
      <circle cx="12" cy="12" r="10" />
      <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
    </IconBase>
  );
}
function LayoutGrid(props) {
  return (
    <IconBase {...props}>
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
    </IconBase>
  );
}
function ArrowRight(props) {
  return (
    <IconBase {...props}>
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </IconBase>
  );
}

'''

MOUNT_CODE = '''
/* ============================================================
   MOUNT
   ============================================================ */
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
'''

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Finance Montréal — Navigateur de l'écosystème d'adaptation</title>
<meta name="description" content="Outil interactif pour orienter les PME dans l'écosystème québécois de l'adaptation climatique." />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js" crossorigin></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.26.3/babel.min.js" crossorigin></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.5.4/papaparse.min.js" crossorigin></script>
<style>
  html, body {{ margin: 0; padding: 0; background: #F5F6FB; }}
  #root {{ min-height: 100vh; }}
</style>
</head>
<body>
<div id="root">
  <div style="display:flex;align-items:center;justify-content:center;min-height:100vh;font-family:'Montserrat',sans-serif;color:#5B6178;">
    Chargement… / Loading…
  </div>
</div>

<script type="text/babel" data-presets="react">
{script}
</script>
</body>
</html>
'''


def main():
    with open(SRC, encoding="utf-8") as f:
        src = f.read()

    if not src.startswith(IMPORT_BLOCK):
        raise SystemExit(
            "ERROR: top-of-file import block doesn't match expected text.\n"
            "The .jsx source's import lines changed — update IMPORT_BLOCK in build_index.py to match, then rerun."
        )
    body = src[len(IMPORT_BLOCK):]

    marker = "export default function App()"
    if marker not in body:
        raise SystemExit("ERROR: could not find 'export default function App()' in source.")
    body = body.replace(marker, "function App()")

    hooks_line = "const { useState, useEffect, useRef, useMemo } = React;\n\n"
    full_script = hooks_line + ICONS_CODE + body + "\n" + MOUNT_CODE

    html = HTML_TEMPLATE.format(script=full_script)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {OUT} ({len(html)} chars)")


if __name__ == "__main__":
    main()
