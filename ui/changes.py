import tkinter as tk
from tkinter import ttk
import webbrowser

from config import BG2, BORDER, TEXT, TEXT_DIM, ACCENT2, YELLOW, STATUS_COLORS


def build_changes_panel(parent, app):
    """
    Build the left changes panel inside `parent`.
    Returns (canvas, inner_frame, last_check_lbl, toggle_btn).
    """
    lhdr = tk.Frame(parent, bg=BG2, pady=10, padx=14)
    lhdr.pack(fill="x")

    lhdr_top = tk.Frame(lhdr, bg=BG2)
    lhdr_top.pack(fill="x")

    tk.Label(lhdr_top, text="DERNIERS CHANGEMENTS", bg=BG2,
             fg=ACCENT2, font=("Courier New", 9, "bold")).pack(side="left", anchor="w")

    toggle_btn = tk.Button(
        lhdr_top, text="◀", bg=BG2, fg=TEXT_DIM,
        font=("Courier New", 8), relief="flat", cursor="hand2",
        padx=4, pady=0, activebackground="#1f2937", activeforeground=TEXT,
        command=app._toggle_left_panel)
    toggle_btn.pack(side="right")

    last_check_lbl = tk.Label(lhdr, text="Jamais vérifié",
                              bg=BG2, fg=TEXT_DIM, font=("Courier New", 8))
    last_check_lbl.pack(anchor="w")

    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

    changes_frame = tk.Frame(parent, bg=BG2)
    changes_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(changes_frame, bg=BG2, highlightthickness=0)
    sb = ttk.Scrollbar(changes_frame, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG2)
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    return canvas, inner, last_check_lbl, toggle_btn


def refresh_changes(inner, changes, register_scroll_fn, scroll_cb):
    """Repopulate the changes inner frame."""
    for w in inner.winfo_children():
        w.destroy()

    if not changes:
        tk.Label(inner, text="Aucun changement détecté",
                 bg=BG2, fg=TEXT_DIM, font=("Courier New", 9),
                 padx=14, pady=10).pack(anchor="w")
        return

    for entry in changes:
        icon    = entry[0]
        tab     = entry[1]
        game    = entry[2]
        status  = entry[3]
        desc    = entry[4]
        rel_url = entry[5] if len(entry) > 5 else ""

        row = tk.Frame(inner, bg=BG2, pady=6, padx=14)
        row.pack(fill="x")
        register_scroll_fn(row, scroll_cb)

        top_row = tk.Frame(row, bg=BG2)
        top_row.pack(fill="x")
        register_scroll_fn(top_row, scroll_cb)

        tk.Label(top_row, text=icon, bg=BG2,
                 font=("Segoe UI Emoji", 11)).pack(side="left")
        tk.Label(top_row, text="  " + game, bg=BG2, fg=TEXT,
                 font=("Courier New", 9, "bold"),
                 wraplength=260, justify="left").pack(side="left")

        bot_row = tk.Frame(row, bg=BG2)
        bot_row.pack(fill="x")
        register_scroll_fn(bot_row, scroll_cb)

        color = YELLOW if icon == "🏷️" else STATUS_COLORS.get(status, TEXT_DIM)
        tk.Label(bot_row, text="   " + tab + " — " + desc,
                 bg=BG2, fg=color, font=("Courier New", 8)).pack(side="left")

        if rel_url:
            lnk = tk.Label(bot_row, text=" ↗", bg=BG2, fg=ACCENT2,
                           font=("Courier New", 8, "underline"), cursor="hand2")
            lnk.pack(side="left")
            lnk.bind("<Button-1>", lambda e, u=rel_url: webbrowser.open(u))

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=14)