# ---------------------------------------------------------------
#  main_menu.rpy  -  a soft, animated main menu (no image assets needed)
#
#  SETUP:
#   1. Drop this file in your game/ folder.
#   2. Open screens.rpy and DELETE the original `screen main_menu():` block
#      (Ren'Py doesn't allow two screens with the same name).
#   3. Optional: put a character/logo PNG at  game/gui/menu_art.png
#      and it will float in on the right side automatically.
#   4. Optional: define config.main_menu_music = "audio/menu.ogg"
# ---------------------------------------------------------------

# ---------- Easy knobs ----------
define mm_tagline     = "A  S T O R Y  O F  S T E P S"   # small text above the title
define mm_title_font  = gui.text_font                   # swap for a pretty .ttf, e.g. "fonts/Pacifico.ttf"
define mm_color_dark  = "#6b2d4a"                       # main text (deep plum)
define mm_color_soft  = "#b5688a"                       # secondary text (dusty rose)

init python:
    import random

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

    # Fixed random layout for the floating bubbles: (x, size, delay, duration, colour)
    _rng = random.Random(11)
    mm_bubbles = []
    for _i in range(18):
        mm_bubbles.append((
            _rng.uniform(0.05, 0.97),
            _rng.choice([26, 34, 46, 60, 80, 110]),
            _rng.uniform(0.0, 14.0),
            _rng.uniform(14.0, 26.0),
            _rng.choice(["#ffffff55", "#ffffff44", "#ffe3ecaa", "#ffd0b855"]),
        ))

define mm_bg = mm_vgradient("#fff3e8", "#f7a8c2")


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
    on show, appear:
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


# ---------- Styles ----------
style mm_tagline:
    font mm_title_font
    size 24
    color mm_color_soft
    kerning 2

style mm_title:
    font mm_title_font
    size 104
    color mm_color_dark
    line_spacing -8
    outlines [(0, "#ffffff", 0, 0), (6, "#ffffff55", 0, 3)]

style mm_btn_text:
    font mm_title_font
    size 46
    idle_color mm_color_dark
    hover_color "#ffffff"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(3, "#c8567f", 0, 2)]

style mm_flower:
    size 36
    idle_color "#ffffff00"
    hover_color "#ffffff"
    yalign 0.5

style mm_version:
    size 20
    color "#8a4b6a99"


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
            text "✿" style "mm_flower"
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

    # optional character art on the right
    if renpy.loadable("gui/menu_art.png"):
        add "gui/menu_art.png" xalign 0.93 yalign 1.0 at mm_art_float

    # frosted left panel
    add Solid("#ffffff3c") xsize 760 ysize config.screen_height
    add Solid("#ffffffaa") xsize 3 ysize config.screen_height xpos 760

    # title block
    vbox:
        xpos 110
        ypos 120
        spacing 14
        at mm_fade_in(0.1)

        text "✿  [mm_tagline]  ✿" style "mm_tagline"
        text "[config.name!t]" style "mm_title" xmaximum 600

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

    # version
    text "v[config.version]" style "mm_version" xalign 0.985 yalign 0.985
