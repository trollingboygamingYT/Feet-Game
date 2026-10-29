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
#   - A cherry-blossom tree fills the right side and drops petals that
#     drift down the screen.
#   - Twinkling sparkles around the title and a heart divider.
#   - Hovering a word gives it a white outline (no hearts, no dark bars).
#   - Fixed: the character art now floats up and down, and the rising
#     bubbles now keep looping (the old animations stopped after one pass).
#
#  The Load / Save / Preferences / About / Help screens are styled in
#  game_menu_theme.rpy (put both files in the game/ folder).
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

    # ---- Cherry-blossom tree, drawn from rotated bars (branches) and flower glyphs ----
    def mm_build_tree(base_x, base_y, seed=3):
        rng = random.Random(seed)
        bars = []
        blossoms = []          # (x, y, radius, flower_count)

        def bar(x, y, length, thick, ang, depth):
            col = mm_mix("#4f2038", "#a45a7a", (5 - depth) / 5.0)
            b = Solid(col, xsize=max(int(thick), 2), ysize=int(length) + 3)
            bars.append(Transform(b, rotate=ang, transform_anchor=True,
                                anchor=(0.5, 1.0), rotate_pad=False,
                                xpos=int(x), ypos=int(y)))
            return (x + length * math.sin(math.radians(ang)),
                    y - length * math.cos(math.radians(ang)))

        def grow(x, y, length, thick, ang, depth, tip_r=70):
            # every limb is two slightly bent pieces, so nothing looks stiff
            x1, y1 = bar(x, y, length * 0.55, thick, ang + rng.uniform(-7, 7), depth)
            ex, ey = bar(x1, y1, length * 0.50, thick * 0.86, ang + rng.uniform(-7, 7), depth)
            if depth == 0:
                blossoms.append((ex, ey, tip_r, 6))
                return
            if depth <= 1:
                blossoms.append((ex, ey, 40, 3))
            # small side twig
            if depth in (1, 2) and rng.random() < 0.35:
                side = rng.choice((-1, 1))
                grow(x1, y1, length * 0.40, thick * 0.55,
                    ang + side * rng.uniform(42, 62), 0, 52)
            kids = [(-1, rng.uniform(18, 32)), (1, rng.uniform(18, 32))]
            if depth == 3 and rng.random() < 0.35:
                kids.append((0, rng.uniform(-6, 6)))
            for side, da in kids:
                grow(ex, ey, length * rng.uniform(0.67, 0.74) * (0.85 if side == 0 else 1.0),
                    thick * 0.68, ang + side * da + rng.uniform(-4, 4), depth - 1, tip_r)

        # trunk: three pieces with a gentle S-bend
        tx, ty = base_x, base_y
        for (ln, th, an) in ((95, 46, -3), (88, 40, 4), (80, 35, -2)):
            tx, ty = bar(tx, ty, ln, th, an, 5)
        # main limbs
        grow(tx, ty, 190, 28, -33 + rng.uniform(-4, 4), 4)
        grow(tx, ty, 182, 28, 29 + rng.uniform(-4, 4), 4)
        if rng.random() < 0.9:
            grow(tx, ty, 140, 22, rng.uniform(-6, 6), 4)

        palette = ["#ffffff", "#ffe9f0", "#ffd0e0", "#ffc2d6", "#ffadc8", "#ff8fb5", "#ffffff", "#ffd9e6"]
        puff_cols = ["#ffb3cd66", "#ffc9dc70", "#ffd9e680", "#ff9fc060"]
        puffs = []
        flowers = []

        def put(lst, text, size, col, cx, cy):
            lst.append(Transform(Text(text, size=size, color=col),
                                xanchor=0.5, yanchor=0.5,
                                xpos=int(cx), ypos=int(cy)))

        for (bx, by, r, n) in blossoms:
            for k in range(1):
                put(puffs, u"●", rng.choice([56, 70, 84]), rng.choice(puff_cols),
                    bx + rng.gauss(0, r * 0.4), by + rng.gauss(0, r * 0.4))
            for k in range(n):
                put(flowers, rng.choice([u"✿", u"❀", u"✿"]), rng.choice([20, 26, 32, 38]),
                    rng.choice(palette),
                    bx + rng.gauss(0, r * 0.5), by + rng.gauss(0, r * 0.5))

        # ground: soft shadow + fallen petals around the trunk
        ground = []
        ground.append(Transform(Text(u"●", size=420, color="#b5688a30"),
                                xanchor=0.5, yanchor=0.5, xpos=int(base_x),
                                ypos=int(config.screen_height - 12), xzoom=2.8, yzoom=0.2))
        for k in range(30):
            put(ground, rng.choice([u"✿", u"❀"]), rng.choice([16, 20, 24, 28]),
                rng.choice(palette),
                base_x + rng.gauss(0, 190), config.screen_height - rng.uniform(4, 58))

        return Fixed(*(ground + bars + puffs + flowers),
                    xysize=(config.screen_width, config.screen_height))

    # Falling petals: (x, x_end, y_start, delay, duration, spin, glyph, size, colour)
    mm_prng = random.Random(21)
    mm_petals = []
    for mm_i in range(36):
        px = mm_prng.uniform(0.58, 0.97)
        near = mm_prng.random() < 0.35          # bigger, faster petals "in front"
        mm_petals.append((
            px,
            px + mm_prng.uniform(-0.16, 0.04),
            mm_prng.uniform(0.22, 0.52),
            mm_prng.uniform(0.0, 12.0),
            mm_prng.uniform(7.0, 10.0) if near else mm_prng.uniform(10.0, 15.0),
            mm_prng.uniform(-420, 420),
            mm_prng.choice([u"✿", u"❀", u"●"]),
            mm_prng.choice([30, 36, 42]) if near else mm_prng.choice([16, 20, 24]),
            mm_prng.choice(["#ffffffdd", "#ffc2d6ee", "#ff9fbfdd", "#ffe3ecee", "#ffadc8dd"]),
        ))

define mm_bg = mm_vgradient("#fff3e8", "#f7a8c2")
define mm_tree = mm_build_tree(0.74 * config.screen_width, config.screen_height + 10)


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
                repeat 6
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

# The whole tree sways very slightly around its base
transform mm_tree_sway(px, py):
    transform_anchor True
    anchor (px, py)
    xpos px
    ypos py
    rotate_pad False
    block:
        ease 5.0 rotate 0.7
        ease 5.0 rotate -0.7
        repeat

# One falling petal: drifts down, sways, spins, fades; then starts again
transform mm_petal(x, x2, y0, delay, dur, spin):
    transform_anchor True
    anchor (0.5, 0.5)
    alpha 0.0
    xpos x
    ypos y0
    pause delay
    block:
        xpos x
        ypos y0
        alpha 0.0
        rotate 0
        parallel:
            linear dur ypos 1.1
        parallel:
            linear dur xpos x2
        parallel:
            linear dur * 0.12 alpha 1.0
            pause dur * 0.68
            linear dur * 0.2 alpha 0.0
        parallel:
            linear dur rotate spin
        parallel:
            block:
                ease 2.0 xoffset 26
                ease 2.0 xoffset -26
                repeat 5
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

style mm_plain_button is empty

style mm_btn_text:
    font mm_title_font
    size 46
    idle_color mm_color_dark
    hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]

style mm_heart:
    size 36
    idle_color "#ffffff00"
    hover_color "#ffffff"
    selected_idle_color "#e0407f"
    selected_hover_color "#ffffff"
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
        style "mm_plain_button"
        at mm_btn(idx * 0.09)
        hover_sound None

        text label style "mm_btn_text" yalign 0.5

        # thin underline
        add Solid("#ffffff88") xsize 500 ysize 2 yalign 1.0 xpos 8


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

    # soft light behind the canopy
    text "●" size 700 color "#ffffff3a" at mm_glow(0.735, 0.34, 8.0)
    text "●" size 420 color "#ffd9e644" at mm_glow(0.80, 0.30, 6.0)

    # cherry-blossom tree on the right, with petals drifting down
    add mm_tree at mm_tree_sway(int(0.74 * config.screen_width), config.screen_height + 10)
    for (ptx, ptx2, pty, ptdelay, ptdur, ptspin, ptglyph, ptsize, ptcol) in mm_petals:
        text ptglyph size ptsize color ptcol at mm_petal(ptx, ptx2, pty, ptdelay, ptdur, ptspin)

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
