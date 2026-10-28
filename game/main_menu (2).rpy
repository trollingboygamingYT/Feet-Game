# ---------------------------------------------------------------
#  main_menu.rpy  -  "Sole Mates" animated main menu (no image assets needed)
#
#  SETUP:
#   1. Replace your old main_menu.rpy in the game/ folder with this one.
#   2. Make sure screens.rpy does NOT also contain `screen main_menu():`
#      (Ren'Py doesn't allow two screens with the same name).
#   3. Optional: put a character/logo PNG at  game/gui/menu_art.png
#      and it will float in on the right side automatically.
#   4. Optional: define config.main_menu_music = "audio/menu.ogg"
#
#  NEW IN THIS VERSION
#   - Unique title "Sole Mates": every letter drops in with a bounce, then
#     gently bobs in a wave. Letters are a plum -> rose gradient with a
#     white rim and a soft pink glow.
#   - A trail of footprints "walks" across the right side of the screen.
#   - Twinkling sparkles around the title and a heart divider.
#   - Fixed: the character art now floats up and down (the old animation
#     got stuck after sliding in).
# ---------------------------------------------------------------

# ---------- Easy knobs ----------
define mm_title_words = ["Sole", "Mates"]                # two lines of the title (change me!)
define mm_tagline     = "A  S T O R Y  O F  S T E P S"   # small text above the title
define mm_credit      = ""                               # e.g. "made with ♥ by Name & Name"
define mm_title_size  = 130
define mm_title_font  = gui.text_font                    # swap for a pretty .ttf, e.g. "fonts/Pacifico.ttf"
define mm_color_dark  = "#6b2d4a"                        # main text (deep plum)
define mm_color_soft  = "#b5688a"                        # secondary text (dusty rose)
define mm_title_c1    = "#6b2d4a"                        # title gradient start (plum)
define mm_title_c2    = "#e0407f"                        # title gradient end (hot rose)

init python:
    import random
    import math

    # Smooth vertical gradient built from thin strips (no image files needed)
    def mm_vgradient(top, bottom, steps=96):
        w, h = config.screen_width, config.screen_height
        c1, c2 = Color(top), Color(bottom)
        strip = h // steps + 1
        kids = []
        for i in range(steps):
            col = c1.interpolate(c2, i / float(steps - 1))
            kids.append(Solid(col, xsize=w, ysize=strip, ypos=int(i * h / steps)))
        return Fixed(*kids, xysize=(w, h))

    # Colour between two hex colours (used for the title letters)
    def mm_mix(a, b, t):
        return Color(a).interpolate(Color(b), t)

    # A footprint drawn from soft dots (sole + heel + 5 toes), no image needed.
    # Tweak the numbers in blob(...) if you want a different foot shape.
    def mm_footprint(col, mirror=False):
        parts = []
        m = -1 if mirror else 1

        def blob(cx, cy, size, zx=1.0, zy=1.0):
            t = Text(u"●", size=size, color=col)
            parts.append(Transform(t, xanchor=0.5, yanchor=0.5,
                                xpos=100 + m * cx, ypos=100 + cy,
                                xzoom=zx, yzoom=zy))

        blob(5, -14, 105, 0.75, 0.85)    # ball of the foot
        blob(8, 18, 70, 0.70, 1.00)      # arch
        blob(5, 44, 62)                  # heel
        blob(-17, -55, 38)               # big toe
        blob(2, -65, 30)
        blob(17, -59, 26)
        blob(29, -47, 23)
        blob(37, -32, 19)                # little toe
        return Fixed(*parts, xysize=(200, 200))

    # Fixed random layout for the floating bubbles: (x, size, delay, duration, colour)
    mm_rng = random.Random(11)
    mm_bubbles = []
    for mm_i in range(18):
        mm_bubbles.append((
            mm_rng.uniform(0.05, 0.97),
            mm_rng.choice([26, 34, 46, 60, 80, 110]),
            mm_rng.uniform(0.0, 14.0),
            mm_rng.uniform(14.0, 26.0),
            mm_rng.choice(["#ffffff55", "#ffffff44", "#ffe3ecaa", "#ffd0b855"]),
        ))

    # The footprint trail: a diagonal path across the right side of the screen,
    # alternating left/right foot.  (x, y, rotation, is_left_foot, delay)
    def mm_build_steps(n=11):
        W = float(config.screen_width)
        H = float(config.screen_height)
        x0, y0 = 0.50 * W, 0.93 * H
        x1, y1 = 0.90 * W, 0.14 * H
        ang = math.atan2(x1 - x0, -(y1 - y0))
        out = []
        for i in range(n):
            t = i / (n - 1.0)
            side = -1 if i % 2 == 0 else 1
            px = x0 + (x1 - x0) * t + side * 44 * math.cos(ang)
            py = y0 + (y1 - y0) * t + side * 44 * math.sin(ang)
            out.append((px / W, py / H, math.degrees(ang) + side * 6, side < 0, i * 0.9))
        return out

    mm_steps = mm_build_steps(11)
    mm_step_cycle = 11 * 0.9 + 5.5

    # Sparkles around the title: (x, y, size, delay, duration)
    mm_sparkles = [
        (0.30, 0.13, 34, 0.0, 2.6),
        (0.01, 0.30, 24, 1.1, 3.1),
        (0.34, 0.33, 28, 0.6, 2.8),
        (0.22, 0.04, 20, 1.7, 3.4),
    ]

define mm_bg = mm_vgradient("#fff3e8", "#f7a8c2")
define mm_foot_l = mm_footprint("#c8567f", mirror=True)
define mm_foot_r = mm_footprint("#c8567f", mirror=False)


# ---------- Animations ----------
transform mm_float(x, delay, dur):
    xanchor 0.5
    xpos x
    ypos 1.15
    alpha 0.0
    pause delay
    block:
        ypos 1.15
        alpha 0.0
        parallel:
            linear dur ypos -0.15
        parallel:
            linear dur * 0.2 alpha 1.0
            pause dur * 0.6
            linear dur * 0.2 alpha 0.0
        parallel:
            block:
                ease 3.0 xoffset 30
                ease 3.0 xoffset -30
                repeat
        repeat

transform mm_glow(x, y, dur):
    xanchor 0.5
    yanchor 0.5
    xpos x
    ypos y
    block:
        ease dur yoffset 25 xoffset 15
        ease dur yoffset -25 xoffset -15
        repeat

transform mm_fade_in(delay=0.0):
    on show, appear:
        alpha 0.0
        yoffset 30
        pause delay
        parallel:
            ease 0.8 alpha 1.0
        parallel:
            ease 0.8 yoffset 0

transform mm_btn(delay):
    on show, appear:
        alpha 0.0
        xoffset -70
        pause 0.35 + delay
        parallel:
            ease 0.6 alpha 1.0
        parallel:
            easeout_back 0.6 xoffset 0
    on hover:
        ease 0.18 xoffset 22
    on idle:
        ease 0.25 xoffset 0

transform mm_art_float:
    alpha 0.0
    xoffset 80
    pause 0.6
    parallel:
        ease 1.2 alpha 1.0
    parallel:
        ease 1.2 xoffset 0
    block:
        ease 3.5 yoffset -14
        ease 3.5 yoffset 14
        repeat

# Each title letter: drops in with a bounce, then bobs gently (staggered = wave)
transform mm_letter(delay):
    alpha 0.0
    yoffset -90
    pause delay
    parallel:
        ease 0.35 alpha 1.0
    parallel:
        easeout_back 0.9 yoffset 0
    pause 0.3
    block:
        ease 1.3 yoffset -9
        ease 1.3 yoffset 7
        repeat

# One footprint: fades in, stays, fades out, waits, repeats (trail restarts)
transform mm_step(x, y, rot, delay, cyc):
    anchor (0.5, 0.5)
    xpos x
    ypos y
    rotate rot
    zoom 1.3
    alpha 0.0
    pause delay
    block:
        ease 0.5 alpha 0.55
        pause 3.2
        ease 1.3 alpha 0.0
        pause cyc - 5.0
        repeat

# Twinkling sparkle
transform mm_twinkle(delay, dur):
    alpha 0.0
    zoom 0.6
    pause delay
    block:
        parallel:
            ease dur alpha 1.0
        parallel:
            ease dur zoom 1.2
        parallel:
            linear dur * 2 rotate 90
        ease dur alpha 0.0
        ease dur * 0.5 zoom 0.6
        pause dur
        repeat


# ---------- Styles ----------
style mm_tagline:
    font mm_title_font
    size 24
    color mm_color_soft
    kerning 2

style mm_title:
    font mm_title_font
    bold True
    # first outline sits on top: white rim, then a soft pink glow/shadow underneath
    outlines [(4, "#ffffff", 0, 0), (10, "#c8567f55", 0, 6)]

style mm_btn_text:
    font mm_title_font
    size 46
    idle_color mm_color_dark
    hover_color "#ffffff"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(3, "#c8567f", 0, 2)]

style mm_heart:
    size 36
    idle_color "#ffffff00"
    hover_color "#ffffff"
    yalign 0.5

style mm_version:
    size 20
    color "#8a4b6a99"

style mm_credit:
    size 20
    color "#8a4b6acc"


# ---------- Title (one word, letter by letter) ----------
screen mm_wave_word(word, sz, base):
    hbox:
        for i, ch in enumerate(word):
            text ch style "mm_title" size sz color mm_mix(mm_title_c1, mm_title_c2, i / max(len(word) - 1, 1.0)) at mm_letter(base + i * 0.13)


# ---------- Buttons ----------
screen mm_button(label, act, idx):
    button:
        action act
        xsize 560
        ysize 86
        at mm_btn(idx * 0.09)
        hover_sound None

        hbox:
            spacing 18
            yalign 0.5
            text "♥" style "mm_heart"
            text label style "mm_btn_text" yalign 0.5

        # thin underline
        add Solid("#ffffff88") xsize 500 ysize 2 yalign 1.0 xpos 54


# ---------- Main menu ----------
screen main_menu():
    tag menu

    # backdrop
    add mm_bg

    # big soft glows
    text "●" size 760 color "#ffffff2a" at mm_glow(0.72, 0.30, 7.0)
    text "●" size 520 color "#ffd2b633" at mm_glow(0.45, 0.95, 9.0)
    text "●" size 420 color "#ffffff22" at mm_glow(0.95, 0.85, 8.0)

    # rising bubbles
    for (bx, bsize, bdelay, bdur, bcol) in mm_bubbles:
        text "●" size bsize color bcol at mm_float(bx, bdelay, bdur)

    # walking footprint trail
    for (sx, sy, srot, sleft, sdelay) in mm_steps:
        add (mm_foot_l if sleft else mm_foot_r) at mm_step(sx, sy, srot, sdelay, mm_step_cycle)

    # optional character art on the right
    if renpy.loadable("gui/menu_art.png"):
        add "gui/menu_art.png" xalign 0.93 yalign 1.0 at mm_art_float

    # frosted left panel
    add Solid("#ffffff3c") xsize 760 ysize config.screen_height
    add Solid("#ffffffaa") xsize 3 ysize config.screen_height xpos 760

    # tagline
    vbox:
        xpos 110
        ypos 70
        at mm_fade_in(0.1)
        text "✿  [mm_tagline]  ✿" style "mm_tagline"

    # the title, one word per line, letter by letter
    vbox:
        xpos 96
        ypos 115
        spacing -30
        use mm_wave_word(mm_title_words[0], mm_title_size, 0.4)
        use mm_wave_word(mm_title_words[1], mm_title_size, 0.9)

    # sparkles around the title
    for (spx, spy, spsize, spdelay, spdur) in mm_sparkles:
        text "✦" size spsize color "#ffffff" xpos spx ypos spy xanchor 0.5 yanchor 0.5 at mm_twinkle(spdelay + 1.5, spdur)

    # heart divider under the title
    hbox:
        xpos 112
        ypos 440
        spacing 14
        at mm_fade_in(1.4)
        add Solid("#c8567f99") xsize 200 ysize 3 yalign 0.5
        text "♥" size 30 color "#e0407f" yalign 0.5
        add Solid("#c8567f99") xsize 200 ysize 3 yalign 0.5

    # navigation
    vbox:
        xpos 100
        ypos 500
        spacing 4

        use mm_button(_("Start"), Start(), 0)
        use mm_button(_("Load"), ShowMenu("load"), 1)
        use mm_button(_("Preferences"), ShowMenu("preferences"), 2)
        use mm_button(_("About"), ShowMenu("about"), 3)

        if renpy.variant("pc") or renpy.variant("web"):
            use mm_button(_("Quit"), Quit(confirm=not main_menu), 4)

    # credit + version
    if mm_credit:
        text "[mm_credit!t]" style "mm_credit" xpos 110 yalign 0.985
    text "v[config.version]" style "mm_version" xalign 0.985 yalign 0.985
