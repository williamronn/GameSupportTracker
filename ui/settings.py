import tkinter as tk
from tkinter import ttk
import threading
import webbrowser

from config import (
    BG, BG3, ACCENT, ACCENT2, TEXT, TEXT_DIM, BORDER, GREEN, RED, YELLOW
)
from cache import load_settings, save_settings, load_cache, save_cache
from data import fetch_steam_owned


def open_settings(app):
    """Open the ⚙ settings Toplevel window."""
    win = tk.Toplevel(app)
    win.title("Paramètres")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    tk.Frame(win, bg=ACCENT, height=3).pack(fill="x")

    # Scrollable container
    outer = tk.Frame(win, bg=BG)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0, width=560)
    sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    def _scroll(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: win.bind("<MouseWheel>", _scroll))
    canvas.bind("<Leave>", lambda e: win.unbind("<MouseWheel>"))
    inner.bind("<Enter>",  lambda e: win.bind("<MouseWheel>", _scroll))
    inner.bind("<Leave>",  lambda e: win.unbind("<MouseWheel>"))

    pad = tk.Frame(inner, bg=BG, padx=24, pady=20)
    pad.pack(fill="both", expand=True)

    tk.Label(pad, text="PARAMÈTRES", bg=BG, fg=ACCENT2,
             font=("Courier New", 11, "bold")).pack(anchor="w", pady=(0, 16))

    # ── GitHub releases ────────────────────────────────────────────────────
    _section_sep(pad)
    releases_var = tk.BooleanVar(value=app._check_releases)
    rel_row = tk.Frame(pad, bg=BG)
    rel_row.pack(fill="x", pady=(0, 4))
    tk.Checkbutton(rel_row, text="Vérifier les releases GitHub lors du check",
                   variable=releases_var,
                   bg=BG, fg=TEXT, selectcolor=BG3,
                   activebackground=BG, activeforeground=TEXT,
                   font=("Courier New", 9, "bold")).pack(side="left")
    tk.Label(pad,
             text="Effectue un appel API GitHub par jeu (~400 requêtes). Désactivé par défaut.\n"
                  "Recommandé : activer uniquement avec un token configuré ci-dessous.",
             bg=BG, fg=TEXT_DIM, font=("Courier New", 8),
             justify="left").pack(anchor="w", pady=(0, 10))

    tk.Label(pad, text="GitHub Personal Access Token",
             bg=BG, fg=TEXT, font=("Courier New", 9, "bold")).pack(anchor="w")
    tk.Label(pad,
             text="Nécessaire pour dépasser la limite de 60 req/h de l'API GitHub.\n"
                  "Token requis : scope 'public_repo' (lecture seule suffit).",
             bg=BG, fg=TEXT_DIM, font=("Courier New", 8),
             justify="left").pack(anchor="w", pady=(2, 6))

    token_var = tk.StringVar(value=app._github_token)
    token_frame = tk.Frame(pad, bg=BG)
    token_frame.pack(fill="x")
    token_entry = tk.Entry(token_frame, textvariable=token_var,
                           bg=BG3, fg=TEXT, insertbackground=TEXT,
                           relief="flat", font=("Courier New", 9),
                           width=48, show="•")
    token_entry.pack(side="left", ipady=5, padx=(0, 6))
    show_var = tk.BooleanVar(value=False)
    tk.Checkbutton(token_frame, text="Afficher", variable=show_var,
                   command=lambda: token_entry.config(
                       show="" if show_var.get() else "•"),
                   bg=BG, fg=TEXT_DIM, selectcolor=BG3,
                   activebackground=BG, font=("Courier New", 8)).pack(side="left")

    lnk = tk.Label(pad, text="→ Créer un token sur github.com/settings/tokens",
                   bg=BG, fg=ACCENT2, font=("Courier New", 8, "underline"),
                   cursor="hand2")
    lnk.pack(anchor="w", pady=(4, 0))
    lnk.bind("<Button-1>", lambda e: webbrowser.open(
        "https://github.com/settings/tokens/new"
        "?description=ArchipelagoTracker&scopes=public_repo"))

    # ── Steam ──────────────────────────────────────────────────────────────
    _section_sep(pad)
    tk.Label(pad, text="Steam", bg=BG, fg=TEXT,
             font=("Courier New", 9, "bold")).pack(anchor="w")
    tk.Label(pad,
             text="Permet d'afficher la colonne Owned (jeux possédés sur Steam).",
             bg=BG, fg=TEXT_DIM, font=("Courier New", 8),
             justify="left").pack(anchor="w", pady=(2, 8))

    _s = load_settings()

    tk.Label(pad, text="Steam Web API Key :", bg=BG, fg=TEXT_DIM,
             font=("Courier New", 8)).pack(anchor="w")
    steam_key_var = tk.StringVar(value=_s.get("steam_api_key", ""))
    steam_key_entry = tk.Entry(pad, textvariable=steam_key_var,
                               bg=BG3, fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=("Courier New", 9),
                               width=48, show="•")
    steam_key_entry.pack(anchor="w", ipady=5, pady=(2, 2))
    show_sk = tk.BooleanVar(value=False)
    tk.Checkbutton(pad, text="Afficher la clé", variable=show_sk,
                   command=lambda: steam_key_entry.config(
                       show="" if show_sk.get() else "•"),
                   bg=BG, fg=TEXT_DIM, selectcolor=BG3,
                   activebackground=BG, font=("Courier New", 8)).pack(anchor="w")

    sk_lnk = tk.Label(pad,
                      text="→ Obtenir une clé sur steamcommunity.com/dev/apikey",
                      bg=BG, fg=ACCENT2, font=("Courier New", 8, "underline"),
                      cursor="hand2")
    sk_lnk.pack(anchor="w", pady=(2, 10))
    sk_lnk.bind("<Button-1>", lambda e: webbrowser.open(
        "https://steamcommunity.com/dev/apikey"))

    tk.Label(pad, text="Steam ID(s) — un par ligne (compte unique ou famille) :",
             bg=BG, fg=TEXT_DIM, font=("Courier New", 8)).pack(anchor="w")
    steam_ids_txt = tk.Text(pad, bg=BG3, fg=TEXT, insertbackground=TEXT,
                            relief="flat", font=("Courier New", 9),
                            width=48, height=4)
    steam_ids_txt.insert("1.0", _s.get("steam_ids", ""))
    steam_ids_txt.pack(anchor="w", pady=(2, 4))
    tk.Label(pad, text="Trouver votre Steam ID : steamidfinder.com",
             bg=BG, fg=TEXT_DIM, font=("Courier New", 8)).pack(anchor="w")

    steam_status_lbl = tk.Label(pad, text="", bg=BG, fg=TEXT_DIM,
                                font=("Courier New", 8))
    steam_status_lbl.pack(anchor="w", pady=(4, 0))

    if app._steam_owned:
        steam_status_lbl.config(
            text=f"Cache actuel : {len(app._steam_owned)} jeux.", fg=TEXT_DIM)

    def _do_steam_refresh(btn):
        key = steam_key_var.get().strip()
        ids = [x.strip() for x in steam_ids_txt.get("1.0", "end").splitlines()
               if x.strip()]
        if not key or not ids:
            steam_status_lbl.config(
                text="⚠ Clé API et au moins un Steam ID requis.", fg=YELLOW)
            return
        btn.config(state="disabled", text="🎮  Chargement...")
        steam_status_lbl.config(text="Connexion à Steam...", fg=TEXT_DIM)

        def _thread():
            owned = fetch_steam_owned(key, ids)
            def _done():
                if owned:
                    app._steam_owned = owned
                    c = load_cache()
                    c["_steam_owned"] = list(owned)
                    save_cache(c)
                    steam_status_lbl.config(
                        text=f"✓ {len(owned)} jeux détectés et sauvegardés.",
                        fg=GREEN)
                    app._refresh_table()
                else:
                    steam_status_lbl.config(
                        text="✗ Échec — vérifiez la clé et les Steam IDs.",
                        fg=RED)
                btn.config(state="normal", text="🎮  Actualiser Steam")
            win.after(0, _done)
        threading.Thread(target=_thread, daemon=True).start()

    steam_btn = tk.Button(pad, text="🎮  Actualiser Steam",
                          bg=BG3, fg=TEXT, font=("Courier New", 9, "bold"),
                          relief="flat", padx=12, pady=5, cursor="hand2",
                          activebackground=ACCENT, activeforeground="white")
    steam_btn.config(command=lambda: _do_steam_refresh(steam_btn))
    steam_btn.pack(anchor="w", pady=(6, 0))

    # ── Save / Cancel ──────────────────────────────────────────────────────
    _section_sep(pad)
    btn_row = tk.Frame(pad, bg=BG)
    btn_row.pack(fill="x")

    def _save():
        app._github_token   = token_var.get().strip()
        app._check_releases = releases_var.get()
        s = load_settings()
        s["github_token"]   = app._github_token
        s["check_releases"] = app._check_releases
        s["steam_api_key"]  = steam_key_var.get().strip()
        s["steam_ids"]      = steam_ids_txt.get("1.0", "end").strip()
        save_settings(s)
        win.destroy()

    tk.Button(btn_row, text="Enregistrer", command=_save,
              bg=ACCENT, fg="white", font=("Courier New", 9, "bold"),
              relief="flat", padx=14, pady=5, cursor="hand2",
              activebackground=ACCENT2, activeforeground="white").pack(side="right")
    tk.Button(btn_row, text="Annuler", command=win.destroy,
              bg=BG3, fg=TEXT_DIM, font=("Courier New", 9),
              relief="flat", padx=14, pady=5, cursor="hand2",
              activebackground=BG3, activeforeground=TEXT).pack(side="right", padx=(0, 8))

    win.update_idletasks()
    h = min(inner.winfo_reqheight() + 40,
            int(app.winfo_screenheight() * 0.80))
    win.geometry(f"610x{h}")


def _section_sep(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=(0, 12))