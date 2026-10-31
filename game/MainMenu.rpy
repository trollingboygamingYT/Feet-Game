# ---------------------------------------------------------------
#  sole_mates_ui.rpy  -  ALL-IN-ONE menu file  (build 5)
#
#  Main menu + Load / Save / Settings / Characters / Shop / Help /
#  History / Confirm screens, in one soft pink anime style.
#
#  SETUP (important):
#   1. Put THIS file in your game/ folder.
#   2. DELETE the old  main_menu.rpy  and  game_menu_theme.rpy
#      AND their compiled copies  main_menu.rpyc / game_menu_theme.rpyc
#      (Ren'Py keeps loading an old .rpyc even if the .rpy is gone).
#      Easiest: Ren'Py launcher -> "Force Recompile".
#   3. Start the game. Bottom right of the main menu says "menu build 5".
#
#  This file runs at init priority 2, so it also overrides the default
#  screens in screens.rpy and any older copies of these menu files.
#
#  Main menu buttons: Start, Load, Characters, Shop, Settings, Quit.
#  Hover = the word gets a white outline (no hearts, no dark bars).
#  Unlock a character from your script with:  $ mm_unlock("char_1")
#  Feet Points (FP): $ mm_add_fp(10)   (testing: Shift+O console -> mm_add_fp(500))
# ---------------------------------------------------------------

init offset = 2

# soft fades between menu pages and between menu <-> game
define config.has_sync = False          # hides the "Download Sync / Upload Sync" button
define config.intra_transition = Dissolve(0.25)
define config.game_main_transition = Dissolve(0.5)
define config.main_game_transition = Dissolve(0.5)

# ---------- Easy knobs ----------
define mm_title_words = ["Sole", "Mates"]                # two lines of the title (change me!)
define mm_tagline     = "A  S T O R Y  O F  S T E P S"   # small text above the title
define mm_extras_in_game_menu = True                      # True = also list Characters/Shop in the Load/Settings page navigation
define mm_start_fp      = 0                                 # Feet Points a brand-new player starts with
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

    # ---- Anime-style cherry-blossom tree (cel-shaded: shadow / body / highlight) ----
    mm_tree_sparkles = []     # filled by mm_build_tree: (x, y, size, delay, duration)

    def mm_build_tree(base_x, base_y, seed=5):
        rng = random.Random(seed)
        W = float(config.screen_width)
        H = float(config.screen_height)
        bars = []
        tips = []                 # (x, y) ends of the thinnest branches
        mids = []                 # (x, y) ends of thicker branches
        shared = {}

        def tx(glyph, size, col):
            # re-use identical text objects so the tree stays light on memory
            key = (glyph, size, col)
            if key not in shared:
                shared[key] = Text(glyph, size=size, color=col)
            return shared[key]

        def place(glyph, size, col, cx, cy):
            return Transform(tx(glyph, size, col), xanchor=0.5, yanchor=0.5,
                            xpos=int(cx), ypos=int(cy))

        def bar(x, y, length, thick, ang, depth):
            col = mm_mix("#3f1c31", "#9a4d70", (5 - depth) / 5.0)
            b = Solid(col, xsize=max(int(thick), 2), ysize=int(length) + 3)
            bars.append(Transform(b, rotate=ang, transform_anchor=True,
                                anchor=(0.5, 1.0), rotate_pad=False,
                                xpos=int(x), ypos=int(y)))
            return (x + length * math.sin(math.radians(ang)),
                    y - length * math.cos(math.radians(ang)))

        def grow(x, y, length, thick, ang, depth):
            x1, y1 = bar(x, y, length * 0.55, thick, ang + rng.uniform(-9, 9), depth)
            ex, ey = bar(x1, y1, length * 0.50, thick * 0.86, ang + rng.uniform(-9, 9), depth)
            if depth == 0:
                tips.append((ex, ey))
                return
            if depth <= 2:
                mids.append((ex, ey))
            for side in (-1, 1):
                grow(ex, ey, length * rng.uniform(0.68, 0.76), thick * 0.66,
                    ang + side * rng.uniform(16, 30) + rng.uniform(-5, 5), depth - 1)

        # thick, curving trunk (anime trees always have a graceful S-curve)
        tx0, ty0 = base_x, base_y
        for (ln, th, an) in ((88, 56, -10), (80, 50, 6), (74, 44, -9), (66, 36, 7)):
            tx0, ty0 = bar(tx0, ty0, ln, th, an, 5)
        # four sweeping limbs make a wide umbrella
        for (ln, th, an) in ((150, 26, -58), (160, 28, -24), (155, 28, 14), (140, 24, 50)):
            grow(tx0, ty0, ln, th, an + rng.uniform(-4, 4), 3)

        # ---- the canopy: fluffy clumps, drawn in three tones for a cel-shaded look
        blobs = []                                   # (x, y, radius)
        for (ex, ey) in tips:
            for k in range(3):
                blobs.append((ex + rng.gauss(0, 34), ey + rng.gauss(0, 30), rng.choice([62, 74, 86])))
        for (ex, ey) in mids:
            for k in range(2):
                blobs.append((ex + rng.gauss(0, 24), ey + rng.gauss(0, 24), rng.choice([50, 62])))
        for k in range(22):                          # fill the gaps in the middle
            (x1, y1), (x2, y2) = rng.choice(tips), rng.choice(tips)
            blobs.append(((x1 + x2) / 2.0 + rng.gauss(0, 20), (y1 + y2) / 2.0 + rng.gauss(0, 20),
                        rng.choice([74, 86])))

        dark, body, light = "#f08bb0", "#ffb7d1", "#ffe3ee"
        shadows, bodies, lights, flowers = [], [], [], []
        petal_cols = ["#ffffff", "#ffeef4", "#ffd0e0", "#ffadc8", "#ff8fb5", "#ffffff"]
        for (bx, by, r) in blobs:
            size = int(2 * r / 0.7)
            shadows.append(place(u"●", size, dark, bx + r * 0.10, by + r * 0.22))
            bodies.append(place(u"●", size, body, bx, by))
            lights.append(place(u"●", int(size * 0.55), light, bx - r * 0.28, by - r * 0.34))
            for k in range(2):
                flowers.append(place(rng.choice([u"✿", u"❀"]), rng.choice([22, 28, 34]),
                                    rng.choice(petal_cols),
                                    bx + rng.gauss(0, r * 0.55), by + rng.gauss(0, r * 0.55)))

        # sparkles hovering over the canopy
        del mm_tree_sparkles[:]
        for k in range(9):
            (bx, by, r) = rng.choice(blobs)
            mm_tree_sparkles.append(((bx + rng.uniform(-40, 40)) / W, (by + rng.uniform(-40, 40)) / H,
                                    rng.choice([22, 28, 36]), rng.uniform(0.0, 4.0), rng.uniform(1.6, 2.6)))

        # ground: soft shadow + fallen petals
        ground = [Transform(tx(u"●", 420, "#b5688a30"), xanchor=0.5, yanchor=0.5,
                            xpos=int(base_x), ypos=int(base_y - 12), xzoom=2.8, yzoom=0.2)]
        for k in range(30):
            ground.append(place(rng.choice([u"✿", u"❀"]), rng.choice([16, 20, 24, 28]),
                                rng.choice(petal_cols),
                                base_x + rng.gauss(0, 200), H - rng.uniform(4, 58)))

        return Fixed(*(ground + bars + shadows + bodies + lights + flowers),
                    xysize=(config.screen_width, config.screen_height))

    # A heart drawn from rotated squares (diamond + two rounded lobes) with a white rim.
    # An optional label ("FP") is written inside. No font or image needed.
    def mm_heart_icon(s, col="#e0407f", label=None, rim="#ffffff"):
        so = s * 1.16
        W = int(1.74 * so) + 2
        H = int(1.6 * so) + 2
        cx = W // 2
        cy = int(0.87 * so)

        def shapes(sz, color):
            out = []
            r = sz / 2.0

            # diamond (a square turned 45 degrees)
            out.append(Transform(Solid(color, xsize=int(sz), ysize=int(sz)),
                                rotate=45, transform_anchor=True,
                                anchor=(0.5, 0.5), rotate_pad=False,
                                xpos=int(cx), ypos=int(cy)))

            # two round lobes, built from thin horizontal strips of a circle
            n = max(4, int(r / 1.5))
            step = r / float(n)
            for ox in (-0.354 * sz, 0.354 * sz):
                for i in range(2 * n):
                    yc = -r + (i + 0.5) * step
                    hw = math.sqrt(max(r * r - yc * yc, 0.0))
                    out.append(Transform(Solid(color, xsize=max(int(hw * 2) + 1, 1),
                                            ysize=int(step) + 1),
                                        xanchor=0.5, yanchor=0.5,
                                        xpos=int(cx + ox), ypos=int(cy - 0.354 * sz + yc)))
            return out

        kids = shapes(so, rim) + shapes(s, col)
        if label:
            kids.append(Transform(Text(label, size=int(s * 0.6), bold=True, color="#ffffff",
                                    outlines=[(2, "#a8245c", 0, 0)]),
                                xanchor=0.5, yanchor=0.5, xpos=cx, ypos=cy - int(0.14 * s)))
        return Fixed(*kids, xysize=(W, H))

    # Falling petals: (x, x_end, y_start, delay, duration, spin, glyph, size, colour)
    mm_prng = random.Random(21)
    mm_petals = []
    for mm_i in range(44):
        px = mm_prng.uniform(0.55, 0.98)
        near = mm_prng.random() < 0.35          # bigger, faster petals "in front"
        mm_petals.append((
            px,
            px - mm_prng.uniform(0.15, 0.42),    # the wind blows them to the left
            mm_prng.uniform(0.18, 0.55),
            mm_prng.uniform(0.0, 12.0),
            mm_prng.uniform(6.0, 9.0) if near else mm_prng.uniform(9.0, 14.0),
            mm_prng.uniform(-500, 500),
            mm_prng.choice([u"✿", u"❀", u"●"]),
            mm_prng.choice([30, 36, 42]) if near else mm_prng.choice([16, 20, 24]),
            mm_prng.choice(["#ffffffdd", "#ffc2d6ee", "#ff9fbfdd", "#ffe3ecee", "#ffadc8dd"]),
        ))

    # Fixed random layout for the floating bubbles: (x, size, delay, duration, colour)
    mm_rng = random.Random(11)
    mm_bubbles = []
    for mm_j in range(18):
        mm_bubbles.append((
            mm_rng.uniform(0.05, 0.97),
            mm_rng.choice([26, 34, 46, 60, 80, 110]),
            mm_rng.uniform(0.0, 14.0),
            mm_rng.uniform(14.0, 26.0),
            mm_rng.choice(["#ffffff55", "#ffffff44", "#ffe3ecaa", "#ffd0b855"]),
        ))

    # Sparkles around the title: (x, y, size, delay, duration)
    mm_sparkles = [
        (0.30, 0.13, 34, 0.0, 2.6),
        (0.01, 0.30, 24, 1.1, 3.1),
        (0.34, 0.33, 28, 0.6, 2.8),
        (0.22, 0.04, 20, 1.7, 3.4),
    ]

define mm_rays = [(0.66, 90, 0.0), (0.77, 160, 1.2), (0.88, 70, 2.4), (0.99, 140, 0.6)]

define mm_bg = mm_vgradient("#fff3e8", "#f7a8c2")
define mm_hill_far = Transform(Text(u"●", size=1000, color="#f7b3c8"), xanchor=0.5, yanchor=0.5,
                            xpos=int(0.80 * config.screen_width), ypos=config.screen_height + 20,
                            xzoom=2.3, yzoom=0.5)
define mm_hill_near = Transform(Text(u"●", size=800, color="#f19bb8"), xanchor=0.5, yanchor=0.5,
                                xpos=int(0.86 * config.screen_width), ypos=config.screen_height + 50,
                                xzoom=2.0, yzoom=0.5)
define Fp_icon = mm_heart_icon(34, label="FP")
define Fp_icon_small = mm_heart_icon(11)
define Fp_tree = mm_build_tree(0.74 * config.screen_width, config.screen_height + 10)


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

# A slow-pulsing sunbeam
transform mm_ray(x, delay):
    transform_anchor True
    anchor (0.5, 0.0)
    rotate_pad False
    xpos x
    ypos -0.05
    rotate 27
    alpha 0.3
    pause delay
    block:
        ease 4.0 alpha 1.0
        ease 4.0 alpha 0.3
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

    # big pale sun in the corner + sunbeams
    text "●" size 900 color "#ffffff22" at mm_glow(0.90, 0.06, 12.0)
    text "●" size 520 color "#fff4d8aa" at mm_glow(0.90, 0.06, 10.0)
    for (rx, rw, rd) in mm_rays:
        add Solid("#ffffff30", xsize=rw, ysize=1500) at mm_ray(rx, rd)

    # soft light behind the canopy
    text "●" size 700 color "#ffffff3a" at mm_glow(0.735, 0.34, 8.0)
    text "●" size 420 color "#ffd9e644" at mm_glow(0.80, 0.30, 6.0)

    # rolling hills
    add mm_hill_far
    add mm_hill_near

    # cherry-blossom tree on the right, with petals drifting down
    add mm_tree at mm_tree_sway(int(0.74 * config.screen_width), config.screen_height + 10)
    for (tsx, tsy, tssize, tsdelay, tsdur) in mm_tree_sparkles:
        text "✦" size tssize color "#ffffff" xpos tsx ypos tsy xanchor 0.5 yanchor 0.5 at mm_twinkle(tsdelay + 2.0, tsdur)
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
        text "✿" size 30 color "#e0407f" yalign 0.5
        add Solid("#c8567f99") xsize 200 ysize 3 yalign 0.5

    # navigation
    vbox:
        xpos 100
        ypos 500
        spacing 4

        use mm_button(_("Start"), Start(), 0)
        use mm_button(_("Load"), ShowMenu("load"), 1)
        use mm_button(_("Characters"), ShowMenu("characters"), 2)
        use mm_button(_("Shop"), ShowMenu("shop"), 3)
        use mm_button(_("Settings"), ShowMenu("preferences"), 4)

        if renpy.variant("pc") or renpy.variant("web"):
            use mm_button(_("Quit"), Quit(confirm=not main_menu), 5)

    # Feet Points, top right (click it to open the Shop)
    use Fp_hud

    # credit + version
    if mm_credit:
        text "[mm_credit!t]" style "mm_credit" xpos 110 yalign 0.985
    text "v[config.version]   |   menu build 4" style "mm_version" xalign 0.985 yalign 0.985


# Placeholder picture for empty save slots
define mm_empty_slot = Fixed(
    Solid("#ffffff55"),
    Text(u"✿", size=80, color="#ffffffcc", xalign=0.5, yalign=0.5),
    xysize=(config.thumbnail_width, config.thumbnail_height))


# ---------- Characters: data + unlocking ----------
# One entry per character:  (id, name, image or None, short description)
# Locked characters show as a gray card with a lock. Unlock one from your
# script with:   $ mm_unlock("char_1")
define mm_characters = [
    ("char_1", "Character 1", None, "Add a description here."),
    ("char_2", "Character 2", None, "Add a description here."),
    ("char_3", "Character 3", None, "Add a description here."),
    ("char_4", "Character 4", None, "Add a description here."),
    ("char_5", "Character 5", None, "Add a description here."),
    ("char_6", "Character 6", None, "Add a description here."),
    ("char_7", "Character 7", None, "Add a description here."),
    ("char_8", "Character 8", None, "Add a description here."),
]

default persistent.mm_unlocked = set()

init python:
    def mm_unlock(cid):
        persistent.mm_unlocked = set(persistent.mm_unlocked or []) | set([cid])

    def mm_is_unlocked(cid):
        return cid in (persistent.mm_unlocked or [])

# A simple padlock drawn from rectangles (no image needed)
define mm_lock = Fixed(
    Solid("#6d6d6d", xsize=10, ysize=36, xpos=14, ypos=0),
    Solid("#6d6d6d", xsize=10, ysize=36, xpos=46, ypos=0),
    Solid("#6d6d6d", xsize=42, ysize=10, xpos=14, ypos=0),
    Solid("#575757", xsize=70, ysize=54, xpos=0, ypos=32),
    Solid("#c9c9c9", xsize=10, ysize=22, xpos=30, ypos=46),
    xysize=(70, 86))

# ---------- Feet Points (FP) + Shop data ----------
# FP is stored in `persistent`, so it is shared by every save.
#   give FP in your script:   $ mm_add_fp(10)
default persistent.Fp = mm_start_fp
default persistent.mm_owned = set()

# One entry per shop item:  (id, name, price or None, character it unlocks or None)
# price None = shows "Coming soon" and can't be bought yet. 8 items = a 4 + 4 layout
# (any number works: rows are added automatically).
define mm_shop_items = [
    ("buy_char_1", "Character 1", 100, "char_1"),
    ("buy_char_2", "Character 2", 150, "char_2"),
    ("buy_char_3", "Character 3", 200, "char_3"),
    ("buy_char_4", "Character 4", 250, "char_4"),
    ("bonus_scene", "Bonus Scene", None, None),
    ("new_outfit", "New Outfit", None, None),
    ("wallpaper", "Wallpaper", None, None),
    ("mystery_box", "Mystery Box", None, None),
]

init python:
    def Fp():
        return persistent.Fp or 0

    def mm_add_fp(n):
        persistent.Fp = (persistent.Fp or 0) + n

    def mm_unlocked_count():
        return len([c for c in mm_characters if mm_is_unlocked(c[0])])

    def mm_buy(item_id, name, price, unlock):
        owned = set(persistent.mm_owned or [])
        if item_id in owned:
            renpy.notify("You already own " + name + "!")
        elif price is None:
            renpy.notify("Coming soon!")
        elif Fp() < price:
            renpy.notify("Not enough Feet Points!")
        else:
            persistent.Fp = Fp() - price
            persistent.mm_owned = owned | set([item_id])
            if unlock:
                mm_unlock(unlock)
            renpy.notify("Purchased: " + name)

transform mm_card_hover:
    on hover:
        ease 0.15 yoffset -8
    on idle:
        ease 0.2 yoffset 0

style Fp_caption:
    font mm_title_font
    size 16
    color mm_color_soft
    kerning 2

style Fp_amount:
    font mm_title_font
    size 46
    bold True
    color mm_color_dark
    outlines [(2, "#ffffff", 0, 0)]

style mm_section_text:
    font mm_title_font
    size 34
    color "#c8567f"
    outlines [(3, "#ffffffaa", 0, 1)]

style mm_pill_text:
    font mm_title_font
    size 24
    color "#ffffff"
    bold True

style mm_card_name:
    font mm_title_font
    size 32
    color "#ffffff"
    outlines [(0, "#00000000", 0, 0)]

# ---------- Animation for the navigation buttons ----------
transform mm_nav_btn:
    on hover, selected_hover:
        ease 0.15 xoffset 14
    on idle, selected_idle:
        ease 0.2 xoffset 0


# ---------- Styles ----------
style mm_gm_title:
    font mm_title_font
    size 80
    bold True
    color mm_color_dark
    outlines [(4, "#ffffff", 0, 0), (9, "#c8567f55", 0, 5)]

style mm_nav_text:
    font mm_title_font
    size 38
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(5, "#ffffff", 0, 0)]

style mm_content_frame is empty:
    xpos 450
    ypos 160
    xsize 1440
    ysize 880
    xpadding 30
    ypadding 20
    background Solid("#ffffff33")

# --- save / load slots ---
style slot_button:
    background Solid("#ffffff55")
    hover_background Solid("#ffffffb0")

style slot_button_text:
    font mm_title_font
    size 22
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color mm_color_dark
    selected_hover_color "#c8567f"

style slot_time_text:
    xalign 0.5

style slot_name_text:
    xalign 0.5
    idle_color mm_color_soft

style page_label_text:
    font mm_title_font
    size 40
    color "#c8567f"
    hover_color "#e0407f"
    outlines [(3, "#ffffffaa", 0, 1)]

style page_button:
    background None
    hover_background None
    selected_background None

style page_button_text:
    font mm_title_font
    size 32
    idle_color mm_color_soft
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    insensitive_color "#b5688a66"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(4, "#ffffff", 0, 0)]

# --- preferences ---
style mm_pref_label:
    top_margin 10
    bottom_margin 4

style mm_pref_label_text:
    font mm_title_font
    size 40
    color "#c8567f"
    outlines [(3, "#ffffffaa", 0, 1)]

style mm_choice_button is empty:
    ysize 56
    xminimum 300

style mm_choice_text:
    font mm_title_font
    size 36
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(5, "#ffffff", 0, 0)]
    yalign 0.5

style mm_small_button is empty:
    left_margin 20
    yalign 0.5

style mm_small_button_text:
    font mm_title_font
    size 30
    idle_color mm_color_soft
    hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]

style mm_slider:
    xsize 520
    ysize 34
    left_bar Fixed(Solid("#c8567f", ysize=10, yalign=0.5))
    right_bar Fixed(Solid("#ffffff99", ysize=10, yalign=0.5))
    thumb Solid("#6b2d4a", xsize=22, ysize=34)
    hover_thumb Solid("#e0407f", xsize=22, ysize=34)

# --- scrollbars (several names so every Ren'Py version picks it up) ---
style vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style gui_vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style game_menu_scrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style game_menu_vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

# --- about / help / history text colours (default theme is light-on-dark) ---
style about_text:
    color mm_color_dark

style about_label_text:
    color "#c8567f"

style help_text:
    color mm_color_dark

style help_label_text:
    color "#c8567f"

style help_button:
    background None
    hover_background None
    selected_background None

style help_button_text:
    idle_color mm_color_soft
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(4, "#ffffff", 0, 0)]

style history_text:
    color mm_color_dark

style history_name_text:
    color "#c8567f"

style history_label_text:
    color "#c8567f"

# --- confirm popup ---
style mm_confirm_frame:
    xalign 0.5
    yalign 0.5
    xminimum 900
    xpadding 60
    ypadding 50
    background Solid("#fff3e8f2")

style mm_confirm_prompt:
    xalign 0.5

style mm_confirm_button is empty:
    xminimum 120

style mm_confirm_prompt_text:
    font mm_title_font
    size 40
    color mm_color_dark
    text_align 0.5

style mm_confirm_button_text:
    font mm_title_font
    size 46
    idle_color mm_color_dark
    hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]


# ---------- One navigation button (just the label) ----------
screen mm_nav_button(label, act):
    button:
        action act
        style "mm_plain_button"
        xsize 380
        ysize 72
        at mm_nav_btn
        hover_sound None

        text label style "mm_nav_text" yalign 0.5


# ---------- Radio / check choice (rose + white outline when selected) ----------
screen mm_choice(lbl, act):
    button:
        action act
        style "mm_choice_button"

        text lbl style "mm_choice_text"


# ---------- Navigation (left column of every menu page) ----------
screen navigation():

    vbox:
        xpos 50
        yalign 0.5
        spacing 6

        if main_menu:

            use mm_nav_button(_("Start"), Start())

        else:

            use mm_nav_button(_("History"), ShowMenu("history"))

            use mm_nav_button(_("Save"), ShowMenu("save"))

        use mm_nav_button(_("Load"), ShowMenu("load"))

        if mm_extras_in_game_menu:

            use mm_nav_button(_("Characters"), ShowMenu("characters"))

            use mm_nav_button(_("Shop"), ShowMenu("shop"))

        use mm_nav_button(_("Settings"), ShowMenu("preferences"))

        if _in_replay:

            use mm_nav_button(_("End Replay"), EndReplay(confirm=True))

        elif not main_menu:

            use mm_nav_button(_("Main Menu"), MainMenu())

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            use mm_nav_button(_("Help"), ShowMenu("help"))

        if renpy.variant("pc"):

            use mm_nav_button(_("Quit"), Quit(confirm=not main_menu))


# ---------- The frame every menu page lives in ----------
screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    # backdrop (same as the main menu)
    add mm_bg
    text "●" size 760 color "#ffffff2a" at mm_glow(0.85, 0.20, 7.0)
    text "●" size 520 color "#ffd2b633" at mm_glow(0.55, 0.98, 9.0)

    for (bx, bsize, bdelay, bdur, bcol) in mm_bubbles[:10]:
        text "●" size bsize color bcol at mm_float(bx, bdelay, bdur)

    for (ptx, ptx2, pty, ptdelay, ptdur, ptspin, ptglyph, ptsize, ptcol) in mm_petals[:12]:
        text ptglyph size ptsize color ptcol at mm_petal(ptx, ptx2, pty, ptdelay, ptdur, ptspin)

    # frosted navigation panel
    add Solid("#ffffff3c") xsize 420 ysize config.screen_height
    add Solid("#ffffffaa") xsize 3 ysize config.screen_height xpos 420

    # content area
    frame:
        style "mm_content_frame"

        if scroll == "viewport":

            viewport:
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                vbox:
                    spacing spacing

                    transclude

        elif scroll == "vpgrid":

            vpgrid:
                cols 1
                yinitial yinitial

                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                spacing spacing

                transclude

        else:

            transclude

    use navigation

    vbox:
        xpos 50
        yalign 0.97
        use mm_nav_button(_("Return"), Return())

    text title style "mm_gm_title" xpos 60 ypos 30

    use Fp_hud

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


# ---------- Save / Load slots ----------
screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot, empty=mm_empty_slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()


# ---------- Preferences ----------
screen preferences():

    tag menu

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            spacing 30

            hbox:
                spacing 100
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        spacing 4
                        label _("Display") style "mm_pref_label"
                        use mm_choice(_("Window"), Preference("display", "window"))
                        use mm_choice(_("Fullscreen"), Preference("display", "fullscreen"))

                vbox:
                    spacing 4
                    label _("Skip") style "mm_pref_label"
                    use mm_choice(_("Unseen Text"), Preference("skip", "toggle"))
                    use mm_choice(_("After Choices"), Preference("after choices", "toggle"))
                    use mm_choice(_("Transitions"), InvertSelected(Preference("transitions", "toggle")))

            hbox:
                spacing 100
                box_wrap True

                vbox:
                    spacing 6
                    xsize 620

                    label _("Text Speed") style "mm_pref_label"
                    bar value Preference("text speed") style "mm_slider"

                    label _("Auto-Forward Time") style "mm_pref_label"
                    bar value Preference("auto-forward time") style "mm_slider"

                vbox:
                    spacing 6
                    xsize 620

                    if config.has_music:
                        label _("Music Volume") style "mm_pref_label"
                        bar value Preference("music volume") style "mm_slider"

                    if config.has_sound:
                        label _("Sound Volume") style "mm_pref_label"
                        hbox:
                            bar value Preference("sound volume") style "mm_slider"
                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound) style "mm_small_button"

                    if config.has_voice:
                        label _("Voice Volume") style "mm_pref_label"
                        hbox:
                            bar value Preference("voice volume") style "mm_slider"
                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice) style "mm_small_button"

                    if config.has_music or config.has_sound or config.has_voice:
                        null height 16
                        use mm_choice(_("Mute All"), Preference("all mute", "toggle"))


# ---------- Yes / No popup ----------
screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    add Solid("#6b2d4a77")

    ## Right-click and escape answer "no".
    key "game_menu" action no_action

    frame:
        style "mm_confirm_frame"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 40

            label _(message):
                style "mm_confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 120

                textbutton _("Yes") action yes_action style "mm_confirm_button"
                textbutton _("No") action no_action style "mm_confirm_button"


# ---------- Characters (locked cards) ----------
screen mm_char_card(cid, cname, cimg):

    $ unlocked = mm_is_unlocked(cid)

    button:
        style "mm_plain_button"
        xysize (290, 370)
        at mm_card_hover

        if unlocked:
            action NullAction()
        else:
            action Notify(_("This character is still locked."))

        fixed:
            clipping True

            if unlocked:

                add Solid("#ffffffe0")
                add Solid("#fff0f6") xpos 4 ypos 4 xsize 282 ysize 362
                add Solid("#ffd9e6") xpos 4 ypos 230 xsize 282 ysize 136

                if cimg:
                    add cimg xalign 0.5 yalign 0.0
                else:
                    text "✿" size 140 color "#ffc2d6" xalign 0.5 ypos 70

                add Solid("#c8567fdd") ysize 62 yalign 1.0
                text cname style "mm_card_name" xalign 0.5 yalign 0.96

            else:

                add Solid("#8f8f8f")
                add Solid("#b9b9b9") xpos 6 ypos 6 xsize 278 ysize 358

                # gray silhouette
                text "●" size 130 color "#a3a3a3" xalign 0.5 ypos 40
                text "●" size 380 color "#a3a3a3" xalign 0.5 ypos 150

                add mm_lock xalign 0.5 ypos 120

                add Solid("#00000033") ysize 62 yalign 1.0
                text _("Locked") style "mm_card_name" color "#6b6b6b" xalign 0.5 yalign 0.96


screen characters():

    tag menu

    use game_menu(_("Characters"), scroll="viewport"):

        text _("Unlocked ") + str(mm_unlocked_count()) + " / " + str(len(mm_characters)) style "mm_section_text"

        null height 16

        hbox:
            xsize 1370
            spacing 30
            box_wrap True
            box_wrap_spacing 30

            for (cid, cname, cimg, cdesc) in mm_characters:
                use mm_char_card(cid, cname, cimg)


# ---------- Shop ----------
screen mm_shop_card(iid, iname, price, unlock):

    $ owned = iid in (persistent.mm_owned or [])

    button:
        style "mm_plain_button"
        xysize (290, 330)
        at mm_card_hover
        action Function(mm_buy, iid, iname, price, unlock)

        fixed:
            clipping True

            add Solid("#ffffffe0")
            add Solid("#fff0f6") xpos 4 ypos 4 xsize 282 ysize 322
            add Solid("#ffd9e6") xpos 4 ypos 170 xsize 282 ysize 156

            text "✿" size 120 color "#ffb3cd" xalign 0.5 ypos 40

            # name plate
            add Solid("#c8567f") ysize 66 yalign 1.0
            add Solid("#ffffff88") ysize 3 ypos 261
            text iname style "mm_card_name" xalign 0.5 yalign 0.95

            # price tag (top left)
            if owned:
                frame:
                    background Solid("#6b2d4a")
                    padding (14, 5)
                    xpos 14
                    ypos 14
                    text _("OWNED") style "mm_pill_text"
            elif price is None:
                frame:
                    background Solid("#9a9a9a")
                    padding (14, 5)
                    xpos 14
                    ypos 14
                    text _("Coming soon") style "mm_pill_text"
            else:
                frame:
                    background Solid("#e0407f")
                    padding (14, 5)
                    xpos 14
                    ypos 14
                    hbox:
                        spacing 8
                        add Fp_icon_small yalign 0.5
                        text str(price) style "mm_pill_text"


screen shop():

    tag menu

    use game_menu(_("Shop"), scroll="viewport"):

        text _("Spend your Feet Points!") style "mm_section_text"

        null height 16

        $ mm_rows = (len(mm_shop_items) + 3) // 4

        grid 4 mm_rows:
            spacing 30

            for (iid, iname, iprice, iunlock) in mm_shop_items:
                use mm_shop_card(iid, iname, iprice, iunlock)

            for i in range(mm_rows * 4 - len(mm_shop_items)):
                null width 290 height 330


# ----------- Feet Points badge (top right) ----------
screen Fp_hud():

    button:
        style "mm_plain_button"
        xalign 0.985
        ypos 24
        xysize (340, 92)
        action ShowMenu("shop")
        at mm_card_hover
        hover_sound None

        fixed:
            add Solid("#ffffffd8")
            add Solid("#fff0f6") xpos 3 ypos 3 xsize 334 ysize 86
            add Solid("#e0407f") xpos 3 ypos 3 xsize 8 ysize 86

            add Fp_icon xpos 26 yalign 0.5

            vbox:
                xpos 108
                yalign 0.5
                spacing -4
                text _("FEET POINTS") style "Fp_caption"
                text str(Fp()) style "Fp_amount"
