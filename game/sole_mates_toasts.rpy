# ---------------------------------------------------------------
#  sole_mates_toasts.rpy  -  in-game popups (event-driven)
#
#  No polling timer -> no mid-build None race -> no crash.
#  Each card has its own lifetime and removes itself.
# ---------------------------------------------------------------

init offset = 5

# ---------- Easy knobs ----------
define mm_toast_life   = 3.6      # seconds a card stays fully visible
define mm_toast_w      = 480
define mm_toast_xgap   = 40
define mm_toast_ytop   = 40
define mm_toast_space  = 14
define mm_toast_bar_w  = mm_toast_w - 70


# ---------- Animations ----------
transform mm_toast_slide:
    on show, appear:
        alpha 0.0
        xoffset 160
        parallel:
            ease 0.25 alpha 1.0
        parallel:
            easeout_back 0.55 xoffset 0
    on hide:
        parallel:
            ease 0.35 alpha 0.0
        parallel:
            easein 0.35 xoffset 100

transform mm_toast_shake:
    on show, appear:
        alpha 0.0
        xoffset 160
        parallel:
            ease 0.2 alpha 1.0
        parallel:
            easeout_back 0.4 xoffset 0
        linear 0.05 xoffset 16
        linear 0.05 xoffset -16
        linear 0.05 xoffset 10
        linear 0.05 xoffset -10
        linear 0.05 xoffset 4
        linear 0.05 xoffset 0
    on hide:
        parallel:
            ease 0.35 alpha 0.0
        parallel:
            easein 0.35 xoffset 100

transform mm_toast_countdown(d):
    xpos 0
    xanchor 0.0
    xzoom 1.0
    linear d xzoom 0.0

transform mm_toast_badge:
    zoom 1.0
    block:
        ease 0.8 zoom 1.12
        ease 0.8 zoom 1.0
        repeat


# ---------- Styles ----------
style mm_toast_caption:
    font mm_title_font
    size 16
    bold True
    color mm_color_soft
    kerning 3

style mm_toast_title:
    font mm_title_font
    size 36
    bold True
    color mm_color_dark
    outlines [(2, "#ffffff", 0, 0)]

style mm_toast_big:
    font mm_title_font
    size 54
    bold True
    color mm_color_dark
    outlines [(2, "#ffffff", 0, 0)]

style mm_toast_small:
    font mm_title_font
    size 21
    bold True
    color mm_color_soft


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
        mm_toasts.push(kind, **data)
        renpy.show_screen("mm_toast_stack")
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
screen mm_toast_shell(accent="#e0407f", bg="#fff3e8", bad=False):
    frame:
        at (mm_toast_shake if bad else mm_toast_slide)
        xsize mm_toast_w
        background Solid("#6b2d4a24")
        padding (0, 0, 6, 8)

        frame:
            xfill True
            background Solid("#ffffff")
            padding (3, 3)

            vbox:
                spacing 0
                xfill True

                frame:
                    xfill True
                    background Fixed(Solid(bg), Solid(accent, xsize=10))
                    padding (34, 18, 24, 18)
                    transclude

                add Solid(accent) ysize 4 xsize mm_toast_w at mm_toast_countdown(mm_toast_life)


# ---------- Character unlocked ----------
screen mm_toast_unlock(d):
    use mm_toast_shell("#e0407f"):
        hbox:
            spacing 22
            yalign 0.5

            fixed:
                xysize (76, 76)
                yalign 0.5
                add Solid("#fff0c2")
                text u"✦" size 46 color "#e6b800" xalign 0.5 yalign 0.5 at mm_toast_badge

            vbox:
                yalign 0.5
                spacing 0
                text "CHARACTER UNLOCKED" style "mm_toast_caption"
                text d["name"] style "mm_toast_title" color "#c8567f" xmaximum 320


# ---------- Feet Points ----------
screen mm_toast_fp(d):
    use mm_toast_shell("#e0407f"):
        hbox:
            xfill True
            yalign 0.5

            hbox:
                spacing 20
                yalign 0.5
                add Fp_icon yalign 0.5
                vbox:
                    spacing -6
                    yalign 0.5
                    text "FEET POINTS" style "mm_toast_caption"
                    $ amt = d["amount"]
                    text (("+" if amt >= 0 else "") + str(amt)) style "mm_toast_big" color ("#e0407f" if amt >= 0 else "#c01818")

            vbox:
                xalign 1.0
                yalign 0.5
                spacing -2
                text "TOTAL" style "mm_toast_caption" xalign 1.0
                text str(d["total"]) style "mm_toast_title" xalign 1.0


# ---------- Trust ----------
screen mm_toast_bar(old, new, w, col):
    fixed:
        xsize w
        ysize 20
        add Solid("#6b2d4a26")
        bar:
            value AnimatedValue(value=new, range=100, delay=1.2, old_value=old)
            xsize w
            ysize 20
            left_bar Solid(col)
            right_bar Solid("#00000000")
            thumb None
            thumb_shadow None
        for q in (0.25, 0.5, 0.75):
            add Solid("#ffffff99") xpos int(w * q) xsize 2 ysize 20

screen mm_toast_trust(d):
    $ diff = d["new"] - d["old"]
    $ bad = diff < 0
    $ col = "#d6153a" if bad else "#e0407f"
    $ delta = ("+" if diff > 0 else ("-" if diff < 0 else u"±")) + str(abs(diff))

    use mm_toast_shell(col, ("#ffd7e6" if bad else "#fff3e8"), bad):
        vbox:
            xfill True
            spacing 10

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
        # a per-card timer, removed the moment this entry unmounts
        timer (mm_toast_life + 0.3) action Function(mm_toast_dismiss, _tid)

        if _kind == "unlock":
            use mm_toast_unlock(d)
        elif _kind == "fp":
            use mm_toast_fp(d)
        elif _kind == "trust":
            use mm_toast_trust(d)


# ---------- The stack ----------
screen mm_toast_stack():
    zorder 160

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