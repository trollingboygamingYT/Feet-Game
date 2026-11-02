define y = Character("YOU")
define a = Character("ADRASTEA")

# | Backgrounds | #
image bg_Park_W_Ao = "images/Adrastea/Scenes/Park_without_Adrastea.png"
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

# The game starts here.
label start:

    scene bg_Park_W_Ao

    y "What a lovely day!"

    "YOU bump into a girl"
    "*THUD*" with vpunch # Changed to vpunch so it doesn't reveal the side edges of the screen

    # Show her with the updated lighting and position
    show Adrastea_Park_Annoyed at left_side

    a "Oh, watch where you're going!"
    
    menu:
        y "What should I reply?"
        
        "I'm sorry, I didn't see you there":
            # Assuming mm_add_fp and fp_popup are defined in your variables/screens files
            $ mm_add_fp(1)
            show screen fp_popup(1)
            "You received +1 Friendship Point!"

            a "That's alright, where are you heading off to?"
            y "Well, I'm actually going downtown, wanna come?"
            
        "Hey, never touch me again!":
            "You made her angry. You didn't receive any Friendship Points!"

            a "Wow, there's no need to be so aggressive!"
            y "Sorry, I'm not in the mood right now."
            y "Well, I'm actually going downtown, wanna come?"