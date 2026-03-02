import os
import re

# ── Sheet ──────────────────────────────────────────────────────────────────────
SHEET_ID = "1iuzDTOAvdoNe8Ne8i461qGNucg5OuEoF-Ikqs8aUQZw"
TABS = {
    "Playable Worlds": "58422002",
    "Core Verified":   "1675722515",
}

POPTRACKER_API = (
    "https://archipelago.miraheze.org/w/api.php"
    "?action=query&list=categorymembers"
    "&cmtitle=Category:Games_with_PopTracker"
    "&cmlimit=500&format=json"
)

GITHUB_REPO_RE = re.compile(
    r'https?://(?:www\.)?github\.com/([^/\s]+)/([^/\s#?]+)'
)

SKIP_NAMES = {
    "Game", "Do not sort",
    "Headers are locked to prevent auto-sorts from being done",
    "If something is missing, leave a comment!"
}

# ── Status ─────────────────────────────────────────────────────────────────────
STATUS_COLORS = {
    "Stable":         "#4ade80",
    "Unstable":       "#fb923c",
    "In Review":      "#60a5fa",
    "Broken on Main": "#f87171",
    "APWorld Only":   "#c084fc",
    "Merged":         "#34d399",
}

STATUS_ORDER = {
    "Merged":         0,
    "In Review":      1,
    "Stable":         2,
    "Unstable":       3,
    "Broken on Main": 4,
    "APWorld Only":   5,
}

# ── Colors ─────────────────────────────────────────────────────────────────────
BG        = "#0d1117"
BG2       = "#161b22"
BG3       = "#1f2937"
ACCENT    = "#7c3aed"
ACCENT2   = "#a855f7"
TEXT      = "#e2e8f0"
TEXT_DIM  = "#64748b"
BORDER    = "#30363d"
GREEN     = "#4ade80"
RED       = "#f87171"
YELLOW    = "#fbbf24"

# ── Sort icons ─────────────────────────────────────────────────────────────────
SORT_ICONS = {
    None:  " -",
    True:  " ↑",
    False: " ↓",
}