init offset = 4

# ---------- Trust system ----------
# Trust is stored per character in persistent (like Feet Points).
default persistent.mm_trust = {}
define mm_trust_start = 20      # trust every character starts with
define mm_trust_max   = 100

init python:

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
            cname = cid
            for c in mm_characters:
                if c[0] == cid:
                    cname = c[1]
            renpy.show_screen("mm_trust_popup", cname=cname, old=old, new=new)


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


# Popup shown in-game, same style as the Feet Point popup
screen mm_trust_popup(cname, old, new):
    zorder 155
    $ diff = new - old
    $ delta = ("+" if diff > 0 else "") + str(diff)

    frame:
        xalign 0.5
        ypos 120
        padding (40, 22)
        background Solid("#fff3e8f2")
        at fp_pop

        vbox:
            spacing 12
            xsize 520
            hbox:
                xfill True
                text "✿ Trust: [cname]" style "mm_trust_text"
                text "[delta]" style "mm_trust_text" xalign 1.0 color ("#3aa66b" if diff >= 0 else "#c01818")
            use mm_trust_bar(old, new, 520)
            text "[new] / 100" style "mm_trust_text" size 22 color "#b5688a"

    timer 2.8 action Hide("mm_trust_popup")