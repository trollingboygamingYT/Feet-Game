define y = Character("YOU")
define a = Character("ADRASTEA")
image bg_Park_W_A = "scenes/Park_without_Adrastea.png"


# The game starts here.





label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg_Park_W_A

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show YOU

    # These display lines of dialogue.

    y "What a lovely day!"

    "YOU bump into another girl"

    show ADRASTEA

    a "Oh, watch where you're going!"

    show YOU

menu:
    y "What should i reply?"
    "I'm sorry, I didn't see you there":
        $ mm_add_fp(1)
        show screen fp_popup(1)
        "You received +1 Friendship Point!"

        a "That's alright, Where are you heading off to?"
        

    
    "Hey, never touch me again!":
        "You made her angry,You didn't receive any Friendship Point!"

        a "Wow, there's no need to be so aggresive!"
        y "Sorry, I'm not in the mood right now"
    
y "Well, i'm actually going downtown, wanna come?"


   
