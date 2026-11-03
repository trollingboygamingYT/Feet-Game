define y = Character("YOU", color="#6b2d4a")
define a = Character("ADRASTEA", color="#e0407f")

# | Backgrounds | #
image bg_Park_Wo_A = "images/Adrastea/Scenes/Park_without_Adrastea.png"
image Adrastea_Park_Annoyed = "images/Adrastea/Character/Adrastea_Park_Annoyed.png"

# | Transforms | #
transform screen_shake:
    linear 0.05 xoffset 15 yoffset 10
    linear 0.05 xoffset -15 yoffset -10
    linear 0.05 xoffset 10 yoffset -5
    linear 0.05 xoffset -10 yoffset 5
    linear 0.05 xoffset 0 yoffset 0

transform left_side:
    zoom 0.85
    xalign 0.5
    yalign 1.0
    yoffset 40
    matrixcolor TintMatrix("#fff5e6") * BrightnessMatrix(-0.05) * ContrastMatrix(0.95)

transform center_grounded:
    zoom 0.85
    xalign 0.5
    yalign 1.0
    yoffset 40
    matrixcolor TintMatrix("#fff5e6") * BrightnessMatrix(-0.05) * ContrastMatrix(0.95)

transform adrastea_enter:
    left_side
    alpha 0.0
    xoffset -60
    parallel:
        ease 0.4 alpha 1.0
    parallel:
        easeout 0.4 xoffset 0


# ---------- Credit text styles ----------
style mm_credit_title:
    font mm_title_font
    size 78
    bold True
    color mm_color_dark
    outlines [(4, "#ffffff", 0, 0), (11, "#c8567f66", 0, 6)]

style mm_credit_sub:
    font mm_title_font
    size 26
    color mm_color_soft
    kerning 4
    outlines [(3, "#ffffffbb", 0, 0)]

style mm_credit_small:
    font mm_title_font
    size 22
    color "#8a4b6acc"
    kerning 2


# ---------- Simple, pretty credits background ----------
screen mm_credits_bg():
    zorder -10

    # same soft gradient as the main menu
    add mm_bg

    # slow-pulsing soft glows for depth
    text "●" size 900 color "#ffffff2a" at mm_glow(0.75, 0.25, 8.0)
    text "●" size 620 color "#ffd2b633" at mm_glow(0.25, 0.90, 10.0)
    text "●" size 480 color "#ffffff22" at mm_glow(0.10, 0.15, 9.0)
    text "●" size 700 color "#ffe3ee44" at mm_glow(0.92, 0.78, 11.0)

    # sunrays from the top-right, very subtle
    for (rx, rw, rd) in mm_rays:
        add Solid("#ffffff22", xsize=rw, ysize=1500) at mm_ray(rx, rd)

    # rising bubbles (already exist in MainMenu.rpy)
    for (bx, bsize, bdelay, bdur, bcol) in mm_bubbles:
        text "●" size bsize color bcol at mm_float(bx, bdelay, bdur)

    # drifting petals (already exist in MainMenu.rpy)
    for (ptx, ptx2, pty, ptdelay, ptdur, ptspin, ptglyph, ptsize, ptcol) in mm_petals:
        text ptglyph size ptsize color ptcol at mm_petal(ptx, ptx2, pty, ptdelay, ptdur, ptspin)


# ---------- One credit "slide" ----------
screen mm_credits_line(header, sub):
    add Solid("#6b2d4a1a")   # faint plum wash to darken the centre a touch

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 18
        at mm_fade_in(0.0)

        text header style "mm_credit_sub" xalign 0.5

        text sub style "mm_credit_title" xalign 0.5

        null height 6

        hbox:
            xalign 0.5
            spacing 16
            add Solid("#c8567f99") xsize 160 ysize 3 yalign 0.5
            text "✿" size 30 color "#e0407f" yalign 0.5
            add Solid("#c8567f99") xsize 160 ysize 3 yalign 0.5


label start:

    $ mm_reset_progress()
    $ persistent.game_started = True
    $ renpy.save_persistent()

    # 1. Start the intro song.
    play music "Music/Intro_Song.ogg" fadein 1.0 noloop volume 0.35

    # --- Auto-playing credit sequence, clean pink backdrop ---
    scene black with fade
    show screen mm_credits_bg
    with Dissolve(0.8)

    show screen mm_credits_line("{size=30}MADE BY{/size}", "Your Name Here")
    with Dissolve(0.6)
    $ renpy.pause(3.0, hard=True)
    hide screen mm_credits_line
    with Dissolve(0.6)

    show screen mm_credits_line("{size=30}A SHORT STORY ABOUT{/size}", "bumping into someone")
    with Dissolve(0.6)
    $ renpy.pause(3.0, hard=True)
    hide screen mm_credits_line
    with Dissolve(0.6)

    show screen mm_credits_line("{size=30}STARRING{/size}", "ADRASTEA")
    with Dissolve(0.6)
    $ renpy.pause(3.0, hard=True)
    hide screen mm_credits_line
    with Dissolve(0.6)

    # fade the pink backdrop away and cut to the park
    hide screen mm_credits_bg
    with Dissolve(0.8)

    # --- Now the actual scene begins ---
    scene bg_Park_Wo_A with fade
    "The sun is out, the park is quiet, and you've got nowhere to be until later."
    y "What a lovely day!"
    "You close your eyes for a second, smiling up at the sky and not looking where you're walking..."

    # --- The bump (music stops here) ---
    "*THUD*" with vpunch
    stop music fadeout 2.0
    pause 2.0

    "You stumble backwards, heart racing."
    show Adrastea_Park_Annoyed at adrastea_enter with dissolve
    "You bumped into a girl!"
    a "Oh, watch where you're going!"

    menu:
        y "What should I reply?"

        "I'm so sorry, I didn't see you there!":

            $ mm_add_fp(1)
            show screen fp_popup(1)
            pause 2.8

            if not mm_is_unlocked("char_1"):
                $ mm_unlock("char_1")
                $ mm_show_unlock("ADRASTEA")
                pause 2.8

            $ mm_give_trust("char_1", 10)
            pause 2.8

            a "...That's alright. Just be more careful next time."
            a "Where are you heading off to, anyway?"

        "Hey, never touch me again!":

            if not mm_is_unlocked("char_1"):
                $ mm_unlock("char_1")
                $ mm_show_unlock("ADRASTEA")
                pause 2.8

            "You made her angry. No Feet Points this time."

            $ mm_give_trust("char_1", -10)
            pause 2.8

            a "Wow, there's no need to be so aggressive!"
            y "Sorry... I'm just not in the mood right now."

    y "Well, I'm actually going downtown. Wanna come?"

    return