default player_name = "YOU"
default walk_style = ""
define y = Character("[player_name!u]", color="#6b2d4a")
define a = Character("ADRASTEA", color="#e0407f")

# How long the credits slide stays on screen (seconds).
define credits_hold = 4.0

# How long each intro image stays on screen (seconds).
# Song is ~50s: credits (~7s) + 5 images x 8s (~40s) lines up well.
define intro_hold = 4.5

# | Backgrounds | #
image bg_Park_Wo_A = "images/Adrastea/Scenes/Park_without_Adrastea.png"

# | Adrastea | #
image Adrastea_Park_Annoyed = "images/Adrastea/Character/Adrastea_Park_Annoyed.png"

# | Intro images (change these paths to your own files) | #
image intro_1 = "images/Intro/Background1.png"
image intro_2 = "images/Intro/Background2.png"
image intro_3 = "images/Intro/Background3.png"
image intro_4 = "images/Intro/Background4.png"
image intro_5 = "images/Intro/Background5.png"

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


# ---------- Intro captions ----------
transform intro_cap_fade:
    on show:
        alpha 0.0
        yoffset 14
        parallel:
            linear 0.9 alpha 1.0
        parallel:
            easeout 0.9 yoffset 0
    on hide:
        linear 0.6 alpha 0.0

screen intro_caption(txt):
    zorder 50

    fixed:
        at intro_cap_fade

        # soft plum band so the text is readable on any image
        add Solid("#3f1c3166") ysize 190 yalign 1.0

        text txt:
            xalign 0.5
            yalign 0.93
            xmaximum 1400
            text_align 0.5
            font mm_title_font
            size 46
            color "#fff3e8"
            outlines [(3, "#6b2d4a", 0, 0)]


# ---------- Name screen (shown at the end of the intro) ----------
style intro_name_input is input:
    font mm_title_font
    size 62
    color "#6b2d4a"
    xalign 0.5

screen intro_name_input():
    modal True
    zorder 60

    add Solid("#6b2d4a66")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        padding (50, 40)
        background Solid("#fff3e8f2")
        at mm_fade_in(0.0)

        vbox:
            xalign 0.5
            spacing 24

            text "✿" size 40 color "#e0407f" xalign 0.5
            text "What's your name?" font mm_title_font size 58 color "#6b2d4a" xalign 0.5

            frame:
                xalign 0.5
                xsize 560
                padding (24, 14)
                background Solid("#ffffff")
                input:
                    style "intro_name_input"
                    value VariableInputValue("player_name", returnable=True)
                    length 14
                    exclude "{}[]<>"

            textbutton _("Continue"):
                style "mm_confirm_button"
                xalign 0.5
                sensitive player_name.strip() != ""
                text_insensitive_color "#b5688a66"
                action Return()

            text "Type your name, then press Enter":
                font mm_title_font
                size 22
                color "#8a4b6acc"
                xalign 0.5


label start:

    $ mm_reset_progress()
    $ persistent.game_started = True
    $ renpy.save_persistent()

    # Lock the intro: no skipping, no rolling back.
    $ _skipping = False
    $ config.allow_skipping = False
    $ renpy.block_rollback()

    # 1. Start the intro song.
    # play music "Music/Intro_Song.ogg" fadein 1.0 noloop volume 0.35 => remove "#" to fix sound

    # --- Short credits slide Intro ---
    scene black with fade
    show screen mm_credits_bg
    with Dissolve(0.8)

    show screen mm_credits_line("{size=30}A GAME MADE BY{/size}", "ACTUALDYNAMICS STUDIO")
    with Dissolve(0.6)
    $ renpy.pause(credits_hold, hard=True) # => credits_hold = 4 seconden
    hide screen mm_credits_line
    with Dissolve(0.6)

    hide screen mm_credits_bg
    with Dissolve(0.8)

    # --- Automatic image sequence with captions (can't be skipped) ---
    scene intro_1 with Dissolve(1.0)
    show screen intro_caption("A sunny morning in the park.\nThe kind of morning that rarely happens.")
    $ renpy.pause(intro_hold, hard=True)
    hide screen intro_caption

    scene intro_2 with Dissolve(1.0)
    show screen intro_caption("The wind is warm, and the sun\nmakes you want to drift away.")
    $ renpy.pause(intro_hold, hard=True)
    hide screen intro_caption

    scene intro_3 with Dissolve(1.0)
    show screen intro_caption("Nothing to do,\nbut just chill all day long.")
    $ renpy.pause(intro_hold, hard=True)
    hide screen intro_caption

    scene intro_4 with Dissolve(1.0)
    show screen intro_caption("Your head is somewhere in the clouds,\nnot aware of what's happening.")
    $ renpy.pause(intro_hold, hard=True)
    hide screen intro_caption

    scene intro_5 with Dissolve(1.0)
    show screen intro_caption("Every story begins with a name...")
    $ renpy.pause(2.0, hard=True)
    hide screen intro_caption

    # --- Choose your name (over the last intro image) ---
    $ player_name = ""
    while player_name == "":
        call screen intro_name_input
        $ player_name = player_name.strip()

    # Unlock skipping again for the actual game.
    $ config.allow_skipping = True

    # --- Now the actual scene begins ---
    scene bg_Park_Wo_A with fade
    "[player_name]... a good name for a good day."
    "The sun is out, the park is quiet, and you've got nowhere to be until later."
    y "What a lovely day!"

    # A small flavour choice (no points)
    menu:
        "What are you doing on your walk?"

        "Listening to my favourite playlist":
            $ walk_style = "music"
            "You slip your earbuds in and let the music carry you along the path."

        "Just enjoying the quiet":
            $ walk_style = "quiet"
            "You let the birds and the breeze be your soundtrack."

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

    # --- Both choices come together here ---
    a "...Anyway. I'm Adrastea."
    a "And you are?"

    y "I'm [player_name]."

    a "[player_name]... Alright. Not the worst way to meet someone."

    if walk_style == "music":
        a "Next time, maybe take one earbud out. You almost took me down."
    else:
        a "You really weren't looking where you were going, were you?"

    menu:
        a "So, where were you off to?"

        "Downtown, want to come with me?":
            $ mm_give_trust("char_1", 5)
            pause 2.8
            a "Hm. You're bold, I'll give you that."
            a "Fine. But you're buying the first drink."

        "Nowhere special, just walking.":
            a "Same. I came here to think."
            a "...Walk with me, then. Quietly."

    # --- Next scene ---
    # scene bg_Downtown with fade
    "To be continued..."

    return