# ---------------------------------------------------------------
#  sole_mates_choice.rpy  -  themed choice menu + "+FP" popup
#
#  Put in game/ next to sole_mates_ui.rpy, then Force Recompile.
#  Replaces the default `screen choice` and adds `screen fp_popup`.
#  (If your screens.rpy also has `screen choice`, this one wins because
#   it loads later / at a higher init offset.)
# ---------------------------------------------------------------

init offset = 3

# ---------- Animations ----------
# Each choice slides in from the right, one after the other
transform mm_choice_in(delay=0.0):
    on show, appear:
        alpha 0.0
        xoffset 120
        pause delay
        parallel:
            ease 0.35 alpha 1.0
        parallel:
            easeout_back 0.45 xoffset 0
    on hover:
        ease 0.15 xoffset -14
    on idle:
        ease 0.2 xoffset 0

# The "+1" popup pops in, floats up a little, and fades out
transform fp_pop:
    alpha 0.0
    zoom 0.6
    yoffset 30
    parallel:
        ease 0.25 alpha 1.0
    parallel:
        easeout_back 0.4 zoom 1.0
    parallel:
        ease 0.4 yoffset 0
    pause 1.6
    parallel:
        ease 0.5 alpha 0.0
    parallel:
        ease 0.5 yoffset -40


# ---------- Styles ----------
style mm_choice_menu_button is empty:
    xsize 1000
    ysize 92
    xpadding 40
    background Solid("#fff3e8ee")
    hover_background Solid("#ffd9e6")
    insensitive_background Solid("#e6e6e6cc")

style mm_choice_menu_text:
    font mm_title_font
    size 38
    idle_color mm_color_dark
    hover_color "#c8567f"
    insensitive_color "#9a9a9a"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    yalign 0.5

style mm_choice_menu_vbox:
    xalign 0.5
    yalign 0.42
    spacing 22

style mm_fp_popup_text:
    font mm_title_font
    size 44
    bold True
    color mm_color_dark
    outlines [(3, "#ffffff", 0, 0)]


# ---------- Choice menu ----------
screen choice(items):

    # soft dim so the choices stand out from the background
    add Solid("#6b2d4a44")

    vbox:
        style "mm_choice_menu_vbox"

        for i, item in enumerate(items):

            button:
                style "mm_choice_menu_button"
                action item.action
                at mm_choice_in(i * 0.12)
                hover_sound None

                # pink accent bar on the left edge
                add Solid("#e0407f") xsize 8 ysize 92 xpos -40 ypos 0

                hbox:
                    spacing 22
                    yalign 0.5

                    text "✿" size 34 color "#e0407f" yalign 0.5
                    text item.caption style "mm_choice_menu_text"


# ---------- "+1 Feet Point" popup ----------
# Use from the script:   show screen fp_popup(1)
screen fp_popup(amount=1):

    zorder 150

    frame:
        xalign 0.5
        ypos 120
        padding (36, 18)
        background Solid("#fff3e8f2")
        at fp_pop

        hbox:
            spacing 18
            yalign 0.5

            add Fp_icon yalign 0.5
            text "+[amount] Feet Point" style "mm_fp_popup_text" yalign 0.5

    timer 2.8 action Hide("fp_popup")

# ---------- "Status changed" popup ----------
# Use from the script:   $ mm_show_status("ADRASTEA", "Mad")
# or:                    $ mm_show_status("ADRASTEA", "good")  # lowercase ok
screen mm_status_popup(name, status):

    $ key = (status or "").strip().lower()
    if key == "good":
        $ col  = "#3aa66b"
        $ txt  = _("Good")
        $ icon = u"✿"
    elif key in ("bad", "mad", "angry"):
        $ col  = "#c43a5b"
        $ txt  = _("Mad")
        $ icon = u"✖"
    else:
        $ col  = "#8a4b6a"
        $ txt  = _("Neutral")
        $ icon = u"●"

    zorder 150

    frame:
        xalign 0.5
        ypos 200
        padding (36, 18)
        background Solid("#fff3e8f2")
        at fp_pop

        hbox:
            spacing 18
            yalign 0.5

            text icon size 46 color col bold True yalign 0.5
            text "[name] — [txt]" style "mm_fp_popup_text" color col yalign 0.5

    timer 2.8 action Hide("mm_status_popup")


init python:
    def mm_show_status(name, status):
        """Convenience: call mm_show_status('ADRASTEA', 'mad') from script."""
        renpy.show_screen("mm_status_popup", name=name, status=status)

# ---------- "Status changed" popup ----------
# Use from the script:   $ mm_show_status("ADRASTEA", "Mad")
# or:                    $ mm_show_status("ADRASTEA", "good")  # lowercase ok
screen mm_status_popup(name, status):

    $ key = (status or "").strip().lower()
    if key == "good":
        $ col  = "#3aa66b"
        $ txt  = _("Good")
        $ icon = u"✿"
    elif key in ("bad", "mad", "angry"):
        $ col  = "#c43a5b"
        $ txt  = _("Mad")
        $ icon = u"✖"
    else:
        $ col  = "#8a4b6a"
        $ txt  = _("Neutral")
        $ icon = u"●"

    zorder 150

    frame:
        xalign 0.5
        ypos 200
        padding (36, 18)
        background Solid("#fff3e8f2")
        at fp_pop

        hbox:
            spacing 18
            yalign 0.5

            text icon size 46 color col bold True yalign 0.5
            text "[name] — [txt]" style "mm_fp_popup_text" color col yalign 0.5

    timer 2.8 action Hide("mm_status_popup")


init python:
    def mm_show_status(name, status):
        """Convenience: call mm_show_status('ADRASTEA', 'mad') from script."""
        renpy.show_screen("mm_status_popup", name=name, status=status)

# ---------- "Character Unlocked" popup ----------
screen mm_unlock_popup(cname):
    zorder 160

    # NEW: Wait 0.8 seconds before showing the popup so it doesn't feel rushed
    timer 0.8 action Show("mm_unlock_popup_actual", cname=cname)

screen mm_unlock_popup(cname):
    zorder 160

    frame:
        xalign 0.5
        ypos 100
        padding (40, 20)
        background Solid("#fff3e8f2")
        at fp_pop

        hbox:
            spacing 18
            yalign 0.5

            text "✦" size 44 color "#e6b800" bold True yalign 0.5
            text "Unlocked: [cname]!" style "mm_fp_popup_text" color "#c8567f" yalign 0.5

    timer 2.8 action Hide("mm_unlock_popup")

init python:
    def mm_show_unlock(name):
        """Show the character unlocked popup."""
        renpy.show_screen("mm_unlock_popup", cname=name)
