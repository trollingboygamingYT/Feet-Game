# ---------------------------------------------------------------
#  sole_mates_toasts.rpy  -  in-game popups (event-driven)
#
#  No polling timer -> no mid-build None race -> no crash.
#  Each card has its own lifetime and removes itself.
# ---------------------------------------------------------------

init offset = 5

# ---------- Easy knobs ----------
define mm_toast_life   = 3.8      # seconds a card stays visible
define mm_toast_w      = 440
define mm_toast_xgap   = 32
define mm_toast_ytop   = 32
define mm_toast_space  = 12
define mm_toast_bar_w  = mm_toast_w - 64


# ---------- Animations ----------
transform mm_toast_slide:
    on show, appear:
        alpha 0.0
        xoffset 48
        parallel:
            ease 0.22 alpha 1.0
        parallel:
            easeout 0.3 xoffset 0
    on hide:
        parallel:
            ease 0.22 alpha 0.0
        parallel:
            easein 0.22 xoffset 28

transform mm_toast_countdown(d):
    xpos 0
    xanchor 0.0
    xzoom 1.0
    linear d xzoom 0.0

# ---------- Styles ----------
style mm_toast_caption:
    font mm_title_font
    size 14
    bold True
    color "#895e70"
    kerning 2

style mm_toast_title:
    font mm_title_font
    size 30
    bold True
    color "#4a2439"

style mm_toast_big:
    font mm_title_font
    size 44
    bold True
    color "#4a2439"

style mm_toast_small:
    font mm_title_font
    size 18
    bold True
    color "#895e70"


# ---------- State ----------
init python:
    import time

    class MMToasts(NoRollback):
        def __init__(self):
            # each entry: {"id": int, "kind": "unlock"/"fp"/"trust", ...fields}
            self.items = []
            self._next_id = 0

        def push(self, kind, **data):
            self._next_id += 1
            data["id"] = self._next_id
            data["kind"] = kind
            self.items.append(data)
            return data["id"]

        def remove(self, toast_id):
            self.items = [t for t in self.items if t["id"] != toast_id]

    mm_toasts = MMToasts()

    def mm_toast_push(kind, **data):
        data["expires_at"] = time.monotonic() + mm_toast_life
        mm_toasts.push(kind, **data)
        renpy.show_screen("mm_toast_stack")
        renpy.restart_interaction()

    def mm_toast_prune():
        now = time.monotonic()
        active = [item for item in mm_toasts.items if item["expires_at"] > now]

        if len(active) != len(mm_toasts.items):
            mm_toasts.items = active
            if not active:
                renpy.hide_screen("mm_toast_stack")
            renpy.restart_interaction()

    def mm_toast_dismiss(toast_id):
        mm_toasts.remove(toast_id)
        if not mm_toasts.items:
            renpy.hide_screen("mm_toast_stack")
        renpy.restart_interaction()

    # ---- public API (used by your script / trust system) ----
    def mm_show_unlock(name):
        mm_toast_push("unlock", name=name)

    def mm_show_fp(amount=1):
        mm_toast_push("fp", amount=amount, total=Fp())

    def mm_show_trust(cname, old, new):
        mm_toast_push("trust", name=cname, old=old, new=new)


# ---------- Shared card shell ----------
screen mm_toast_shell(accent="#c8567f", bg="#fff7fa"):
    frame:
        at mm_toast_slide
        xsize mm_toast_w
        background Solid("#4a24392a")
        padding (0, 0, 4, 6)

        frame:
            xfill True
            background Solid("#fffdfd")
            padding (1, 1)

            vbox:
                spacing 0
                xfill True

                frame:
                    xfill True
                    background Fixed(Solid(bg), Solid(accent, xsize=6))
                    padding (24, 16, 20, 16)
                    transclude

                add Solid(accent) ysize 3 xsize mm_toast_w at mm_toast_countdown(mm_toast_life)


# ---------- Character unlocked ----------
screen mm_toast_unlock(d):
    use mm_toast_shell():
        hbox:
            spacing 18
            yalign 0.5

            fixed:
                xysize (64, 64)
                yalign 0.5
                add Solid("#fce9f0")
                text u"✦" size 38 color "#c8567f" xalign 0.5 yalign 0.5

            vbox:
                yalign 0.5
                spacing 2
                text "CHARACTER UNLOCKED" style "mm_toast_caption"
                text d["name"] style "mm_toast_title" xmaximum 300


# ---------- Feet Points ----------
screen mm_toast_fp(d):
    use mm_toast_shell():
        hbox:
            xfill True
            yalign 0.5

            hbox:
                spacing 14
                yalign 0.5
                add Fp_icon yalign 0.5
                vbox:
                    spacing -4
                    yalign 0.5
                    text "FEET POINTS" style "mm_toast_caption"
                    $ amt = d["amount"]
                    text (("+" if amt >= 0 else "") + str(amt)) style "mm_toast_big" color ("#e0407f" if amt >= 0 else "#c01818")

            vbox:
                xalign 1.0
                yalign 0.5
                spacing 0
                text "TOTAL" style "mm_toast_caption" xalign 1.0
                text str(d["total"]) style "mm_toast_title" xalign 1.0


# ---------- Trust ----------
screen mm_toast_bar(old, new, w, col):
    fixed:
        xsize w
        ysize 10
        add Solid("#6b2d4a26")
        bar:
            value AnimatedValue(value=new, range=100, delay=1.2, old_value=old)
            xsize w
            ysize 10
            left_bar Solid(col)
            right_bar Solid("#00000000")
            thumb None
            thumb_shadow None
        for q in (0.25, 0.5, 0.75):
                add Solid("#ffffff99") xpos int(w * q) xsize 2 ysize 10

screen mm_toast_trust(d):
    $ diff = d["new"] - d["old"]
    $ bad = diff < 0
    $ col = "#d6153a" if bad else "#e0407f"
    $ delta = ("+" if diff > 0 else ("-" if diff < 0 else u"±")) + str(abs(diff))

    use mm_toast_shell(col, ("#fff1f4" if bad else "#fff7fa")):
        vbox:
            xfill True
            spacing 8

            hbox:
                xfill True
                vbox:
                    spacing -2
                    yalign 0.5
                    text u"✿  TRUST" style "mm_toast_caption"
                    text d["name"] style "mm_toast_title" size 32 xmaximum 280
                text delta style "mm_toast_big" xalign 1.0 yalign 0.5 color ("#c01818" if bad else "#2f9a5e")

            use mm_toast_bar(d["old"], d["new"], mm_toast_bar_w, col)

            hbox:
                xfill True
                text mm_trust_label(d["new"]) style "mm_toast_small"
                text (str(d["new"]) + " / 100") style "mm_toast_small" xalign 1.0


# ---------- One stacked card wrapper (owns its own timer) ----------
screen mm_toast_entry(d):
    $ _tid = d["id"]
    $ _kind = d["kind"]

    vbox:
        if _kind == "unlock":
            use mm_toast_unlock(d)
        elif _kind == "fp":
            use mm_toast_fp(d)
        elif _kind == "trust":
            use mm_toast_trust(d)


# ---------- The stack ----------
screen mm_toast_stack():
    zorder 160
    timer 0.1 repeat True action Function(mm_toast_prune)

    vbox:
        xalign 1.0
        xoffset -mm_toast_xgap
        ypos mm_toast_ytop
        spacing mm_toast_space
        xsize mm_toast_w

        # iterate a SNAPSHOT of the list, so mutation during build is safe
        for d in list(mm_toasts.items):
            use mm_toast_entry(d)


# ---------- Old-style call kept working: show screen fp_popup(1) ----------
screen fp_popup(amount=1):
    on "show" action Function(mm_show_fp, amount)
    timer 0.05 action Hide("fp_popup")