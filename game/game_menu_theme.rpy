# ---------------------------------------------------------------
#  game_menu_theme.rpy  -  gives Load / Save / Settings / Characters /
#  Shop / Help / History / Confirm the same soft pink style as main_menu.rpy
#
#  SETUP:
#   1. Put this file in the game/ folder next to main_menu.rpy.
#   2. That's it. It re-defines the screens `game_menu`, `navigation`,
#      `file_slots`, `preferences` and `confirm` with a higher init
#      priority, so you do NOT have to edit screens.rpy.
#      (If Ren'Py ever complains about a duplicate screen, comment out
#       those screens in screens.rpy.)
#
#  It uses the colours / fonts / bubbles / animations from main_menu.rpy
#  (mm_color_dark, mm_color_soft, mm_title_font, mm_bg, ...).
# ---------------------------------------------------------------

init offset = 1

# Placeholder picture for empty save slots
define mm_empty_slot = Fixed(
    Solid("#ffffff55"),
    Text(u"✿", size=80, color="#ffffffcc", xalign=0.5, yalign=0.5),
    xysize=(config.thumbnail_width, config.thumbnail_height))


# ---------- Characters: data + unlocking ----------
# One entry per character:  (id, name, image or None, short description)
# Locked characters show as a gray card with a lock. Unlock one from your
# script with:   $ mm_unlock("char_1")
define mm_characters = [
    ("char_1", "Character 1", None, "Add a description here."),
    ("char_2", "Character 2", None, "Add a description here."),
    ("char_3", "Character 3", None, "Add a description here."),
    ("char_4", "Character 4", None, "Add a description here."),
    ("char_5", "Character 5", None, "Add a description here."),
    ("char_6", "Character 6", None, "Add a description here."),
    ("char_7", "Character 7", None, "Add a description here."),
    ("char_8", "Character 8", None, "Add a description here."),
]

default persistent.mm_unlocked = set()

init python:
    def mm_unlock(cid):
        persistent.mm_unlocked = set(persistent.mm_unlocked or []) | set([cid])

    def mm_is_unlocked(cid):
        return cid in (persistent.mm_unlocked or [])

# A simple padlock drawn from rectangles (no image needed)
define mm_lock = Fixed(
    Solid("#6d6d6d", xsize=10, ysize=36, xpos=14, ypos=0),
    Solid("#6d6d6d", xsize=10, ysize=36, xpos=46, ypos=0),
    Solid("#6d6d6d", xsize=42, ysize=10, xpos=14, ypos=0),
    Solid("#575757", xsize=70, ysize=54, xpos=0, ypos=32),
    Solid("#c9c9c9", xsize=10, ysize=22, xpos=30, ypos=46),
    xysize=(70, 86))

# ---------- Shop: placeholder items (name, price) ----------
define mm_shop_items = [
    ("Coming soon", "-"),
    ("Coming soon", "-"),
    ("Coming soon", "-"),
    ("Coming soon", "-"),
    ("Coming soon", "-"),
    ("Coming soon", "-"),
]

transform mm_card_hover:
    on hover:
        ease 0.15 yoffset -8
    on idle:
        ease 0.2 yoffset 0

style mm_card_name:
    font mm_title_font
    size 32
    color "#ffffff"
    outlines [(0, "#00000000", 0, 0)]

# ---------- Animation for the navigation buttons ----------
transform mm_nav_btn:
    on hover, selected_hover:
        ease 0.15 xoffset 14
    on idle, selected_idle:
        ease 0.2 xoffset 0


# ---------- Styles ----------
style mm_gm_title:
    font mm_title_font
    size 80
    bold True
    color mm_color_dark
    outlines [(4, "#ffffff", 0, 0), (9, "#c8567f55", 0, 5)]

style mm_nav_text:
    font mm_title_font
    size 38
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(5, "#ffffff", 0, 0)]

style mm_content_frame is empty:
    xpos 450
    ypos 160
    xsize 1440
    ysize 880
    xpadding 30
    ypadding 20
    background Solid("#ffffff33")

# --- save / load slots ---
style slot_button:
    background Solid("#ffffff55")
    hover_background Solid("#ffffffb0")

style slot_button_text:
    font mm_title_font
    size 22
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color mm_color_dark
    selected_hover_color "#c8567f"

style slot_time_text:
    xalign 0.5

style slot_name_text:
    xalign 0.5
    idle_color mm_color_soft

style page_label_text:
    font mm_title_font
    size 40
    color "#c8567f"
    hover_color "#e0407f"
    outlines [(3, "#ffffffaa", 0, 1)]

style page_button:
    background None
    hover_background None
    selected_background None

style page_button_text:
    font mm_title_font
    size 32
    idle_color mm_color_soft
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    insensitive_color "#b5688a66"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(4, "#ffffff", 0, 0)]

# --- preferences ---
style mm_pref_label:
    top_margin 10
    bottom_margin 4

style mm_pref_label_text:
    font mm_title_font
    size 40
    color "#c8567f"
    outlines [(3, "#ffffffaa", 0, 1)]

style mm_choice_button is empty:
    ysize 56
    xminimum 300

style mm_choice_text:
    font mm_title_font
    size 36
    idle_color mm_color_dark
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(5, "#ffffff", 0, 0)]
    yalign 0.5

style mm_small_button is empty:
    left_margin 20
    yalign 0.5

style mm_small_button_text:
    font mm_title_font
    size 30
    idle_color mm_color_soft
    hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]

style mm_slider:
    xsize 520
    ysize 34
    left_bar Fixed(Solid("#c8567f", ysize=10, yalign=0.5))
    right_bar Fixed(Solid("#ffffff99", ysize=10, yalign=0.5))
    thumb Solid("#6b2d4a", xsize=22, ysize=34)
    hover_thumb Solid("#e0407f", xsize=22, ysize=34)

# --- scrollbars (several names so every Ren'Py version picks it up) ---
style vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style gui_vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style game_menu_scrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

style game_menu_vscrollbar:
    xsize 18
    base_bar Solid("#ffffff66")
    thumb Solid("#c8567f")
    unscrollable "hide"

# --- about / help / history text colours (default theme is light-on-dark) ---
style about_text:
    color mm_color_dark

style about_label_text:
    color "#c8567f"

style help_text:
    color mm_color_dark

style help_label_text:
    color "#c8567f"

style help_button:
    background None
    hover_background None
    selected_background None

style help_button_text:
    idle_color mm_color_soft
    hover_color "#c8567f"
    selected_idle_color "#e0407f"
    selected_hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(4, "#ffffff", 0, 0)]
    selected_idle_outlines [(3, "#ffffff", 0, 0)]
    selected_hover_outlines [(4, "#ffffff", 0, 0)]

style history_text:
    color mm_color_dark

style history_name_text:
    color "#c8567f"

style history_label_text:
    color "#c8567f"

# --- confirm popup ---
style mm_confirm_frame:
    xalign 0.5
    yalign 0.5
    xminimum 900
    xpadding 60
    ypadding 50
    background Solid("#fff3e8f2")

style mm_confirm_prompt:
    xalign 0.5

style mm_confirm_button is empty:
    xminimum 120

style mm_confirm_prompt_text:
    font mm_title_font
    size 40
    color mm_color_dark
    text_align 0.5

style mm_confirm_button_text:
    font mm_title_font
    size 46
    idle_color mm_color_dark
    hover_color "#c8567f"
    outlines [(0, "#00000000", 0, 0)]
    hover_outlines [(5, "#ffffff", 0, 0)]


# ---------- One navigation button (just the label) ----------
screen mm_nav_button(label, act):
    button:
        action act
        style "mm_plain_button"
        xsize 380
        ysize 72
        at mm_nav_btn
        hover_sound None

        text label style "mm_nav_text" yalign 0.5


# ---------- Radio / check choice (rose + white outline when selected) ----------
screen mm_choice(lbl, act):
    button:
        action act
        style "mm_choice_button"

        text lbl style "mm_choice_text"


# ---------- Navigation (left column of every menu page) ----------
screen navigation():

    vbox:
        xpos 50
        yalign 0.5
        spacing 6

        if main_menu:

            use mm_nav_button(_("Start"), Start())

        else:

            use mm_nav_button(_("History"), ShowMenu("history"))

            use mm_nav_button(_("Save"), ShowMenu("save"))

        use mm_nav_button(_("Load"), ShowMenu("load"))

        use mm_nav_button(_("Characters"), ShowMenu("characters"))

        use mm_nav_button(_("Shop"), ShowMenu("shop"))

        use mm_nav_button(_("Settings"), ShowMenu("preferences"))

        if _in_replay:

            use mm_nav_button(_("End Replay"), EndReplay(confirm=True))

        elif not main_menu:

            use mm_nav_button(_("Main Menu"), MainMenu())

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            use mm_nav_button(_("Help"), ShowMenu("help"))

        if renpy.variant("pc"):

            use mm_nav_button(_("Quit"), Quit(confirm=not main_menu))


# ---------- The frame every menu page lives in ----------
screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    # backdrop (same as the main menu)
    add mm_bg
    text "●" size 760 color "#ffffff2a" at mm_glow(0.85, 0.20, 7.0)
    text "●" size 520 color "#ffd2b633" at mm_glow(0.55, 0.98, 9.0)

    for (bx, bsize, bdelay, bdur, bcol) in mm_bubbles[:10]:
        text "●" size bsize color bcol at mm_float(bx, bdelay, bdur)

    # frosted navigation panel
    add Solid("#ffffff3c") xsize 420 ysize config.screen_height
    add Solid("#ffffffaa") xsize 3 ysize config.screen_height xpos 420

    # content area
    frame:
        style "mm_content_frame"

        if scroll == "viewport":

            viewport:
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                vbox:
                    spacing spacing

                    transclude

        elif scroll == "vpgrid":

            vpgrid:
                cols 1
                yinitial yinitial

                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                spacing spacing

                transclude

        else:

            transclude

    use navigation

    vbox:
        xpos 50
        yalign 0.97
        use mm_nav_button(_("Return"), Return())

    text title style "mm_gm_title" xpos 60 ypos 30

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


# ---------- Save / Load slots ----------
screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot, empty=mm_empty_slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


# ---------- Preferences ----------
screen preferences():

    tag menu

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            spacing 30

            hbox:
                spacing 100
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        spacing 4
                        label _("Display") style "mm_pref_label"
                        use mm_choice(_("Window"), Preference("display", "window"))
                        use mm_choice(_("Fullscreen"), Preference("display", "fullscreen"))

                vbox:
                    spacing 4
                    label _("Skip") style "mm_pref_label"
                    use mm_choice(_("Unseen Text"), Preference("skip", "toggle"))
                    use mm_choice(_("After Choices"), Preference("after choices", "toggle"))
                    use mm_choice(_("Transitions"), InvertSelected(Preference("transitions", "toggle")))

            hbox:
                spacing 100
                box_wrap True

                vbox:
                    spacing 6
                    xsize 620

                    label _("Text Speed") style "mm_pref_label"
                    bar value Preference("text speed") style "mm_slider"

                    label _("Auto-Forward Time") style "mm_pref_label"
                    bar value Preference("auto-forward time") style "mm_slider"

                vbox:
                    spacing 6
                    xsize 620

                    if config.has_music:
                        label _("Music Volume") style "mm_pref_label"
                        bar value Preference("music volume") style "mm_slider"

                    if config.has_sound:
                        label _("Sound Volume") style "mm_pref_label"
                        hbox:
                            bar value Preference("sound volume") style "mm_slider"
                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound) style "mm_small_button"

                    if config.has_voice:
                        label _("Voice Volume") style "mm_pref_label"
                        hbox:
                            bar value Preference("voice volume") style "mm_slider"
                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice) style "mm_small_button"

                    if config.has_music or config.has_sound or config.has_voice:
                        null height 16
                        use mm_choice(_("Mute All"), Preference("all mute", "toggle"))


# ---------- Yes / No popup ----------
screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    add Solid("#6b2d4a77")

    ## Right-click and escape answer "no".
    key "game_menu" action no_action

    frame:
        style "mm_confirm_frame"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 40

            label _(message):
                style "mm_confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 120

                textbutton _("Yes") action yes_action style "mm_confirm_button"
                textbutton _("No") action no_action style "mm_confirm_button"


# ---------- Characters (locked cards) ----------
screen mm_char_card(cid, cname, cimg):

    $ unlocked = mm_is_unlocked(cid)

    button:
        style "mm_plain_button"
        xysize (290, 370)
        at mm_card_hover

        if unlocked:
            action NullAction()
        else:
            action Notify(_("This character is still locked."))

        fixed:
            clipping True

            if unlocked:

                add Solid("#fff3f8")

                if cimg:
                    add cimg xalign 0.5 yalign 0.0
                else:
                    text "✿" size 140 color "#ffc2d6" xalign 0.5 ypos 70

                add Solid("#c8567fdd") ysize 62 yalign 1.0
                text cname style "mm_card_name" xalign 0.5 yalign 0.96

            else:

                add Solid("#8f8f8f")
                add Solid("#b9b9b9") xpos 6 ypos 6 xsize 278 ysize 358

                # gray silhouette
                text "●" size 130 color "#a3a3a3" xalign 0.5 ypos 40
                text "●" size 380 color "#a3a3a3" xalign 0.5 ypos 150

                add mm_lock xalign 0.5 ypos 120

                add Solid("#00000033") ysize 62 yalign 1.0
                text _("Locked") style "mm_card_name" color "#6b6b6b" xalign 0.5 yalign 0.96


screen characters():

    tag menu

    use game_menu(_("Characters"), scroll="viewport"):

        hbox:
            xsize 1370
            spacing 30
            box_wrap True
            box_wrap_spacing 30

            for (cid, cname, cimg, cdesc) in mm_characters:
                use mm_char_card(cid, cname, cimg)


# ---------- Shop (placeholder cards) ----------
screen shop():

    tag menu

    use game_menu(_("Shop"), scroll="viewport"):

        hbox:
            xsize 1370
            spacing 30
            box_wrap True
            box_wrap_spacing 30

            for (iname, iprice) in mm_shop_items:

                button:
                    style "mm_plain_button"
                    xysize (290, 330)
                    at mm_card_hover
                    action Notify(_("Coming soon!"))

                    fixed:
                        clipping True
                        add Solid("#ffffff66")
                        text "✿" size 120 color "#ffffffdd" xalign 0.5 ypos 50
                        add Solid("#c8567fdd") ysize 62 yalign 1.0
                        text iname style "mm_card_name" xalign 0.5 yalign 0.96
                        text iprice style "mm_card_name" color "#6b2d4a" xalign 0.5 ypos 215
