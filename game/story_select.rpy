# story_select.rpy  (redesigned)
# Story selection screen: "Main Story" (starts the game) and "Locked" (for a later story).
#
# Needs these files in game/images/ :
#   story_bg.png, story_divider.png, petal_a.png, petal_b.png,
#   story_card_main.png, story_card_main_hover.png,
#   story_card_locked.png, story_card_locked_hover.png
#
# Flow: Start on the main menu -> label start (bottom of this file) -> this screen.
# Main Story jumps to label main_story (rename your old "label start:" in script.rpy to that).

define story_main_label = "main_story"
define story_font = "fonts/PatrickHand-Regular.ttf"

# ---------------------------------------------------------------
# Animations
# ---------------------------------------------------------------
# Cards slide up and fade in one after the other.
transform story_card_in(delay=0.0):
    alpha 0.0 yoffset 50
    pause delay
    parallel:
        ease 0.55 alpha 1.0
    parallel:
        easein_back 0.55 yoffset 0

# Gentle floating, so the screen never feels static.
transform story_float(delay=0.0, amp=7, dur=3.0):
    yoffset 0
    pause delay
    block:
        ease dur/2.0 yoffset -amp
        ease dur/2.0 yoffset 0
        repeat

# Title drops in.
transform story_title_in:
    alpha 0.0 yoffset -30
    ease 0.6 alpha 1.0 yoffset 0

# Main card: grows a little on hover and "pops" on press.
transform story_main_fx:
    anchor (0.5, 0.5)
    zoom 1.0
    on idle:
        ease 0.2 zoom 1.0
    on hover:
        ease 0.2 zoom 1.06
    on selected_idle:
        ease 0.2 zoom 1.0

# Locked card: tiny shake on hover ("nope, not yet").
transform story_locked_fx:
    anchor (0.5, 0.5)
    zoom 1.0
    on idle:
        ease 0.15 zoom 1.0 xoffset 0
    on hover:
        ease 0.15 zoom 1.02
        linear 0.05 xoffset 7
        linear 0.05 xoffset -7
        linear 0.05 xoffset 5
        linear 0.05 xoffset -5
        linear 0.05 xoffset 0

# ---------------------------------------------------------------
# Screen
# ---------------------------------------------------------------
screen story_select():
    modal True

    # Background + falling petals
    add "story_bg"
    add SnowBlossom("petal_a", count=12, border=60, xspeed=(15, 55), yspeed=(60, 120), start=0, fast=True)
    add SnowBlossom("petal_b", count=14, border=60, xspeed=(-25, 40), yspeed=(45, 95), start=0, fast=True)

    # Title block
    fixed:
        at story_title_in
        text "Choose your story":
            font story_font
            size 96
            color "#ff5f9a"
            xalign 0.5
            ypos 40
            outlines [(7, "#ffffff", 0, 0), (0, "#f7a6c4", 4, 5)]
        text "Pick where your journey begins":
            font story_font
            size 38
            color "#c0557f"
            xalign 0.5
            ypos 150
            outlines [(3, "#ffffff", 0, 0)]
        add "story_divider":
            xalign 0.5
            ypos 205

    hbox:
        xalign 0.5
        yalign 0.66
        spacing 50

        # ---------------- MAIN STORY ----------------
        fixed:
            xysize (500, 640)
            at story_card_in(0.2)
            fixed:
                xysize (500, 640)
                at story_float(0.0)
                button:
                    xysize (500, 640)
                    xpos 250
                    ypos 320
                    padding (0, 0, 0, 0)
                    background "story_card_main"
                    hover_background "story_card_main_hover"
                    at story_main_fx
                    action Jump(story_main_label)
                    fixed:
                        xysize (500, 640)
                        text "Main Story":
                            font story_font
                            size 62
                            color "#ff4f8b"
                            xalign 0.5
                            ypos 428
                            outlines [(5, "#ffffff", 0, 0)]
                        text "Begin the journey":
                            font story_font
                            size 34
                            color "#b24a73"
                            xalign 0.5
                            ypos 497
                            outlines [(3, "#ffffff", 0, 0)]

        # ---------------- LOCKED ----------------
        fixed:
            xysize (500, 640)
            at story_card_in(0.4)
            fixed:
                xysize (500, 640)
                at story_float(1.2)
                button:
                    xysize (500, 640)
                    xpos 250
                    ypos 320
                    padding (0, 0, 0, 0)
                    background "story_card_locked"
                    hover_background "story_card_locked_hover"
                    at story_locked_fx
                    action Notify("This story is locked for now. Coming soon!")
                    fixed:
                        xysize (500, 640)
                        text "Locked":
                            font story_font
                            size 62
                            color "#6a6088"
                            xalign 0.5
                            ypos 428
                            outlines [(5, "#ffffff", 0, 0)]
                        text "Coming soon":
                            font story_font
                            size 34
                            color "#7d749a"
                            xalign 0.5
                            ypos 497
                            outlines [(3, "#ffffff", 0, 0)]

    # Back button (text only, no dark bar; white outline gets thicker on hover)
    textbutton "< Back":
        xpos 60
        yalign 0.96
        text_font story_font
        text_size 52
        text_color "#ff6fa0"
        text_hover_color "#ff4f8b"
        text_outlines [(4, "#ffffff", 0, 0)]
        text_hover_outlines [(7, "#ffffff", 0, 0)]
        background None
        hover_background None
        action MainMenu(confirm=False)

    key "game_menu" action MainMenu(confirm=False)

# ---------------------------------------------------------------
# New "start" label: Start on the main menu lands here.
# Main Story jumps to label main_story, Back returns to the main menu.
# ---------------------------------------------------------------
label start:
    scene black
    call screen story_select
    return
