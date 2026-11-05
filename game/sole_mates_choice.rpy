init offset = 3

# ---------- Transforms ----------
transform paper_choice_in(delay=0.0):
    on show, appear:
        alpha 0.0
        yoffset 20
        pause delay
        parallel:
            ease 0.3 alpha 1.0
        parallel:
            ease 0.3 yoffset 0
    on hover:
        ease 0.12 xoffset 10
    on idle:
        ease 0.15 xoffset 0

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
style mm_choice_menu_text:
    font mm_title_font
    size 38
    idle_color mm_color_dark
    hover_color "#c8567f"
    insensitive_color "#9a9a9a"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    yalign 0.5

style mm_fp_popup_text:
    font mm_title_font
    size 44
    bold True
    color mm_color_dark
    outlines [(3, "#ffffff", 0, 0)]


# ---------- Choice screen: one paper per option ----------
screen choice(items):
    key "mod_menu" action Show("mod_menu")

    vbox:
        xalign 0.5
        yanchor 1.0
        ypos 0.60                    # bottom of the options (0.0 = top, 1.0 = bottom)
        spacing 6                    # gap between the papers

        for i, item in enumerate(items):
            button:
                xysize (1100, 126)
                background "gui/choice_paper.png"
                hover_background "gui/choice_paper_hover.png"
                insensitive_background "gui/choice_paper.png"
                action item.action
                at paper_choice_in(i * 0.12)

                hbox:
                    xpos 80
                    yalign 0.5
                    spacing 22
                    text item.caption style "mm_choice_menu_text" xmaximum 840

# NOTE: the Feet Point / Unlocked / Trust popups now live in sole_mates_toasts.rpy
