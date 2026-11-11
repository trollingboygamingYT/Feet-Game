default persistent.mm_awarded_saves = {}
default mm_playthrough_id = None
init offset = 4

# ---------- Trust system ----------
# Trust is stored per character in persistent (like Feet Points).
default persistent.mm_trust = {}
define mm_trust_start = 20      # trust every character starts with
define mm_trust_max   = 100

init python:

    import uuid

    def mm_new_playthrough_id():
        """Call this ONCE at the start of a fresh playthrough (e.g. in label start
        after mm_reset_progress). Gives this save-file a unique token so
        'one-time' rewards can fire once per playthrough without exploits."""
        pid = str(uuid.uuid4())
        store.mm_playthrough_id = pid
        persistent.mm_awarded_saves = dict(persistent.mm_awarded_saves or {})
        persistent.mm_awarded_saves[pid] = []
        renpy.save_persistent()

    def mm_award_once(key, fn):
        """Run fn() only the first time this (playthrough_id, key) pair is used.
        Safe against Main Menu → Continue exploits because the record lives in
        persistent, keyed by the save file's playthrough token."""
        pid = getattr(store, "mm_playthrough_id", None)
        if pid is None:
            # no playthrough id (shouldn't happen in normal flow) — fall back
            fn()
            return True

        awarded = persistent.mm_awarded_saves or {}
        done = set(awarded.get(pid, []))

        if key in done:
            return False

        fn()
        done.add(key)
        awarded = dict(awarded)
        awarded[pid] = list(done)
        persistent.mm_awarded_saves = awarded
        renpy.save_persistent()
        return True

    def mm_get_trust(cid):
        return (persistent.mm_trust or {}).get(cid, mm_trust_start)

    def mm_set_trust(cid, value):
        d = dict(persistent.mm_trust or {})
        d[cid] = max(0, min(mm_trust_max, value))
        persistent.mm_trust = d

    def mm_trust_label(v):
        if v >= 90: return "Devoted"
        if v >= 70: return "Close"
        if v >= 50: return "Friendly"
        if v >= 30: return "Warming up"
        if v >= 10: return "Wary"
        return "Distrustful"

    def mm_give_trust(cid, n, popup=True):
        """Change trust (negative n = lose trust) and show the bar popup."""
        old = mm_get_trust(cid)
        mm_set_trust(cid, old + n)
        new = mm_get_trust(cid)
        if popup:
            mm_show_trust(mm_display_name(cid), old, new)


    def mm_display_name(cid):
        """Return the name to show in toasts/popups.
        Real name if unlocked, '???' otherwise."""
        # mm_is_unlocked lives in MainMenu.rpy — safe to call here because
        # everything is init-time python and both files are loaded.
        if not mm_is_unlocked(cid):
            return "???"
        for c in mm_characters:
            if c[0] == cid:
                return c[1]
        return cid

style mm_trust_text:
    font gui.text_font
    size 30
    bold True
    color "#6b2d4a"
    outlines [(2, "#ffffff", 0, 0)]


# The bar itself (animates from old -> new). Use old=new for a static bar.
screen mm_trust_bar(old, new, w=460):
    fixed:
        xsize w
        ysize 26
        add Solid("#6b2d4a33")
        bar:
            value AnimatedValue(value=new, range=100, delay=1.0, old_value=old)
            xsize w
            ysize 26
            left_bar Solid("#e0407f")
            right_bar Solid("#00000000")
            thumb None
            thumb_shadow None
