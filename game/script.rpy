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

# Bigger, standing on the bottom edge, no extra downward push
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

# Her entrance: slides in a little from the side
transform adrastea_enter:
    left_side
    alpha 0.0
    xoffset -60
    parallel:
        ease 0.4 alpha 1.0
    parallel:
        easeout 0.4 xoffset 0


# The game starts here.
label start:

    scene bg_Park_Wo_A with fade

    "The sun is out, the park is quiet, and you've got nowhere to be until later."

    y "What a lovely day!"

    "You close your eyes for a second, smiling up at the sky and not looking where you're walking..."

    # --- The bump ---
    "*THUD*" with vpunch

    "You stumble backwards, heart racing."

    show Adrastea_Park_Annoyed at adrastea_enter with dissolve

    "You bumped into a girl!"

    a "Oh, watch where you're going!"

    menu:
        y "What should I reply?"

        "I'm so sorry, I didn't see you there!":
            
            # 1. Show Feet Points and WAIT for it to finish
            $ mm_add_fp(1)
            show screen fp_popup(1)
            pause 2.8
            
            # 2. Check if she was already unlocked. If not, unlock her and show popup!
            if not mm_is_unlocked("char_1"):
                $ mm_unlock("char_1")
                $ mm_show_unlock("ADRASTEA")
                pause 2.8
                
            a "...That's alright. Just be more careful next time."
            a "Where are you heading off to, anyway?"

        "Hey, never touch me again!":
            
            # 1. Check if she was already unlocked. If not, unlock her and show popup!
            if not mm_is_unlocked("char_1"):
                $ mm_unlock("char_1")
                $ mm_show_unlock("ADRASTEA")
                pause 2.8

            "You made her angry. No Feet Points this time."

            a "Wow, there's no need to be so aggressive!"
            y "Sorry... I'm just not in the mood right now."

    y "Well, I'm actually going downtown. Wanna come?"

    return

    return
