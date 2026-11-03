init offset = 3

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

screen choice(items):
    key "mod_menu" action Show("mod_menu")
    add Solid("#6b2d4a44")

    vbox:
        style "mm_choice_menu_vbox"
        for i, item in enumerate(items):
            button:
                style "mm_choice_menu_button"
                action item.action
                at mm_choice_in(i * 0.12)
                hover_sound None
                add Solid("#e0407f") xsize 8 ysize 92 xpos -40 ypos 0
                hbox:
                    spacing 22
                    yalign 0.5
                    text "✿" size 34 color "#e0407f" yalign 0.5
                    text item.caption style "mm_choice_menu_text"

screen fp_popup(amount=1):
    modal True
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

screen mm_unlock_popup(cname):
    modal True
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
    def mm_show_status(name, status):
        renpy.show_screen("mm_status_popup", name=name, status=status)

    def mm_show_unlock(name):
        renpy.show_screen("mm_unlock_popup", cname=name)