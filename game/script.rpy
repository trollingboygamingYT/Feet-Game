default player_name = "YOU"
default walk_style = "" # | Walk_style is voor een keuze later | #
default intro_active = False
define Music = [
    "Music/Music_Choice/Song1.ogg",
    "Music/Music_Choice/Song2.ogg",
    "Music/Music_Choice/Song3.ogg"

]
define y = Character("[player_name!u]", color="#6b2d4a")
define adrastea_unknown = Character("???", color="#e0407f")
define adrastea = Character("Adrastea", color="#e0407f")

# | CREDITS SLIDE DURATION (SECONDS) | #
define credits_hold = 4.0

# | INTRO IMAGE DURATION (SECONDS) | #
define intro_hold = 4.5

# | BACKGROUNDS | #
image bg_Park_Wo_A = "images/Adrastea/Scenes/Park_without_Adrastea.png"

# | ADRASTEA | #
image Adrastea Park Annoyed = "images/Adrastea/Character/Adrastea_Park_Annoyed.png"
image Adrastea Park Suprised = "images/Adrastea/Character/Adrastea_Park_Suprised.png"
image Adrastea Park Furious = "images/Adrastea/Character/Adrastea_Park_Furious.png"
image Adrastea Park Shy = "images/Adrastea/Character/Adrastea_Park_Shy.png"

# | INTRO IMAGES (CHANGE THESE PATHS TO YOUR OWN FILES) | #
image intro_1 = "images/Intro/Background1.png"
image intro_2 = "images/Intro/Background2.png"
image intro_3 = "images/Intro/Background3.png"
image intro_4 = "images/Intro/Background4.png"
image intro_5 = "images/Intro/Background5.png"

# | TRANSFORMS | #
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


# | CREDIT TEXT STYLES | #
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


# | CREDITS BACKGROUND | #
screen mm_credits_bg():
    zorder -10

    # | SOFT GRADIENT (SAME AS THE MAIN MENU) | #
    add mm_bg

    # | SLOW-PULSING SOFT GLOWS | #
    text "●" size 900 color "#ffffff2a" at mm_glow(0.75, 0.25, 8.0)
    text "●" size 620 color "#ffd2b633" at mm_glow(0.25, 0.90, 10.0)
    text "●" size 480 color "#ffffff22" at mm_glow(0.10, 0.15, 9.0)
    text "●" size 700 color "#ffe3ee44" at mm_glow(0.92, 0.78, 11.0)

    # | SUNRAYS FROM THE TOP-RIGHT | #
    for (rx, rw, rd) in mm_rays:
        add Solid("#ffffff22", xsize=rw, ysize=1500) at mm_ray(rx, rd)

    # | RISING BUBBLES (FROM MAINMENU.RPY) | #
    for (bx, bsize, bdelay, bdur, bcol) in mm_bubbles:
        text "●" size bsize color bcol at mm_float(bx, bdelay, bdur)

    # | DRIFTING PETALS (FROM MAINMENU.RPY) | #
    for (ptx, ptx2, pty, ptdelay, ptdur, ptspin, ptglyph, ptsize, ptcol) in mm_petals:
        text ptglyph size ptsize color ptcol at mm_petal(ptx, ptx2, pty, ptdelay, ptdur, ptspin)


# | CREDIT SLIDE | #
screen mm_credits_line(header, sub):
    # | FAINT PLUM WASH | #
    add Solid("#6b2d4a1a")

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


# | INTRO CAPTIONS | #
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

        # | SOFT PLUM BAND FOR READABLE TEXT | #
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


# | NAME SCREEN (END OF INTRO) | #
style intro_name_input is input:
    font "fonts/PatrickHand-Regular.ttf"
    size 68
    color "#e0407f"

screen intro_name_input():
    modal True
    zorder 60

    add Solid("#6b2d4a66")

    fixed:
        xalign 0.5
        yalign 0.5
        xysize (920, 560)
        at mm_fade_in(0.0)

        add "gui/name_paper.png"

        vbox:
            xalign 0.5
            yalign 0.5
            yoffset 10
            spacing 18

            text "What's your name?":
                font "fonts/PatrickHand-Regular.ttf"
                size 72
                color "#594632"
                xalign 0.5

            # handwritten line instead of a white box
            fixed:
                xalign 0.5
                xysize (560, 90)
                input:
                    style "intro_name_input"
                    value VariableInputValue("player_name", returnable=True)
                    length 14
                    exclude "{}[]<>"
                    xalign 0.5
                    yalign 0.5
                add Solid("#59463299") xsize 560 ysize 3 yalign 1.0

            textbutton _("Continue"):
                xalign 0.5
                sensitive player_name.strip() != ""
                action Return()
                text_font "fonts/PatrickHand-Regular.ttf"
                text_size 58
                text_idle_color "#594632"
                text_hover_color "#2878C8"
                text_insensitive_color "#59463255"

            text "Type your name, then press Enter":
                font "fonts/PatrickHand-Regular.ttf"
                size 28
                color "#8a6a5a"
                xalign 0.5

# Put this near your other screens (like mm_credits_bg)
screen music_stop_timer():
    # Wait 26 seconds, then fade the music out over 2 seconds
    timer 26.0 action [Stop("music", fadeout=2.0), Hide("music_stop_timer")]


label main_story:

    $ mm_reset_progress()
    $ mm_new_playthrough_id()      # <-- add this line
    $ persistent.game_started = True
    $ renpy.save_persistent()

    # | INTRO | #
    $ _skipping = False
    $ config.allow_skipping = False
    $ renpy.block_rollback()
    $ intro_active = True

    # | START THE INTRO SONG | #
    # play music "Music/Intro/Intro_Song.ogg" fadein 2.0 noloop volume 0.25

    # | CREDITS SLIDE INTRO | #
    scene black with fade
    show screen mm_credits_bg
    with Dissolve(0.8)

    show screen mm_credits_line("{size=30}A GAME MADE BY{/size}", "ACTUALDYNAMICS STUDIO")
    with Dissolve(0.6)
    $ renpy.pause(credits_hold, hard=True) # | CREDITS_HOLD = 4 SECONDEN | #
    hide screen mm_credits_line
    with Dissolve(0.6)

    hide screen mm_credits_bg
    with Dissolve(0.8)

    # | AUTOMATIC IMAGE SEQUENCE WITH CAPTIONS (CAN'T BE SKIPPED) | #
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
    $ renpy.pause(2.5, hard=True)
    hide screen intro_caption

label intro_choose_name:
    hide screen mm_credits_line
    hide screen mm_credits_bg
    hide screen intro_caption
    $ renpy.hide_screen("mod_menu")
    $ renpy.pause(0.3, hard=True)
    scene intro_5

    # | CHOOSE YOUR NAME (OVER THE LAST INTRO IMAGE) | #
    $ player_name = ""
    while player_name == "":
        $ intro_active = False
        call screen intro_name_input
        $ player_name = player_name.strip()

    # | UNLOCK SKIPPING AGAIN FOR THE ACTUAL GAME | #
    $ config.allow_skipping = True

    # | NOW THE ACTUAL SCENE BEGINS | #
    scene bg_Park_Wo_A with fade
    "[player_name] Huh? What an interesting name..."
    y "Ahhh what a lovely day!"
    stop music fadeout 2.0

    # | A SMALL FLAVOUR CHOICE (NO POINTS) | #
    menu:
        "What are you doing on your walk?"

        "Listening to my favourite song":
            $ walk_style = "music"

            menu:
                "Which song do you want to listen to?"

                "Crowded House - Dont Dream Its Over":
                    play music Music[0] fadein 1.0 volume 0.15
                "Cass Elliot - Make Your Own Kind Of Music":
                    play music Music[1] fadein 1.0 volume 0.15
                "The Handsome Family - Far From Any Road":
                    play music Music[2] fadein 1.0 volume 0.15

            "You slip your earbuds in and let the music carry you along the path. {w=1.0}{nw}"

        "Just enjoying the quiet":
            $ walk_style = "quiet"
            play sound "Music/SFX/Nature_SFX.ogg" fadein 1.0 volume 0.6
            "You let the birds and the breeze be your soundtrack. {w=1.0}{nw}"
            
            # Tiny 0.1 second pause to let the menu close
            $ renpy.pause(0.1, hard=True) 
            
            # Play the audio (using the 'sound' channel)
            

    # Show the text, but DO NOT wait for the player to click
    $ renpy.say(None, "You close your eyes for a second, smiling up at the sky and not looking where you're walking...", interact=False)
    
    # Lock the game for exactly 20 seconds
    $ config.allow_skipping = False
    $ renpy.pause(3.0, hard=True) # veranderen naar 20 seconds
    
    # | THE BUMP (AUDIO STOPS HERE) | #
    stop sound
    stop music
    play sound "Music/SFX/Thud_SFX.ogg"
    "*THUD*" with vpunch

    "You snap out of the moment. You look up and see..."
    show Adrastea Park Annoyed at adrastea_enter with dissolve
    "You bumped into a girl!"
    adrastea_unknown "Hey, watch where you're going weirdo!"

    menu:
        y "What should I reply?"

        "I'm so sorry, I didn't see you there!":
            show Adrastea Park Suprised with Dissolve(0.15)

            if mm_award_once("bump_sorry_fp", lambda: mm_add_fp(10)):
                $ mm_show_fp(10)

            if mm_award_once("bump_sorry_trust", lambda: mm_give_trust("char_1", 10)):
                pass                                  # mm_give_trust already shows the toast

            adrastea_unknown "...That's alright. Just be more careful next time."
            y "Maybe a bit too forward, but what is your name?"
            adrastea "Hah! The ladies must like you. I'm Adrastea. And you are?"

                # | UNLOCK ADRASTEA | #
            if not mm_is_unlocked("char_1"):
                $ mm_unlock("char_1")
                $ mm_show_unlock("ADRASTEA")

            y "I'm [player_name]. Nice to meet you. Adrastea."
            adrastea "Nice to meet you too, [player_name]. Well this is quite akward."
            show Adrastea Park Shy with Dissolve(0.15)
            y "Uhh yeah, i guess it is."






        "Hey, never touch me again!":
            show Adrastea Park Furious with Dissolve(0.15) # Fade op character image switch

            "You made her angry. No Feet Points this time."

            if mm_award_once("bump_angry_trust", lambda: mm_give_trust("char_1", -10)):
                pause 2.8

            adrastea_unknown "Wow, there's no need to be so aggressive!"
            y "Sorry... I'm just not in the mood right now."

    # | BOTH CHOICES COME TOGETHER HERE | #
    adrastea_known "...Anyway. I'm Adrastea."
    adrastea_known "And you are?"

    y "I'm [player_name]."

    adrastea_known "[player_name]... Alright. Not the worst way to meet someone."

    if walk_style == "music":
        adrastea_known "Next time, maybe take one earbud out. You almost took me down."
    else:
        adrastea_known "You really weren't looking where you were going, were you?"

    menu:
        adrastea_known "So, where were you off to?"

        "Downtown, want to come with me?":
            if mm_award_once("walk_downtown_trust", lambda: mm_give_trust("char_1", 5)):
                pause 2.8
            adrastea_known "Hm. You're bold, I'll give you that."
            adrastea_known "Fine. But you're buying the first drink."

        "Nowhere special, just walking.":
            adrastea_known "Same. I came here to think."
            adrastea_known "...Walk with me, then. Quietly."

    # | NEXT SCENE | #
    # scene bg_Downtown with fade
    "To be continued..."

    return