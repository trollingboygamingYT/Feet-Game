# ---------------------------------------------------------------
#  sole_mates_pause.rpy  -  in-game pause menu
#
#  SETUP:
#   1. Put this file in your game/ folder (next to sole_mates_ui.rpy).
#   2. Force Recompile from the Ren'Py launcher.
#
#  What it does:
#   - Removes the always-visible quick menu from the game screen.
#   - ESC / right-click in-game opens this pause menu instead of
#     jumping straight to the Save screen.
#   - Uses the same look as the main menu (needs sole_mates_ui.rpy).
# ---------------------------------------------------------------

init offset = 3

# ESC / right-click now opens the pause menu
default _game_menu_screen = "pause_menu"

# Replace the quick menu with an empty screen (hides it in-game)
screen quick_menu():
    pass


# ---------- Pause menu ----------
screen pause_menu():
    tag menu
    modal True

    # pause all audio channels while this menu is open, resume when closed
    on "show" action Function(mm_pause_all_audio, True)
    on "hide" action Function(mm_pause_all_audio, False)

    key "game_menu" action Return()

    add Solid("#6b2d4a88")
    # ... rest unchanged

    # a few petals drifting for atmosphere (remove these 2 lines if you want it plain)
    for (ptx, ptx2, pty, ptdelay, ptdur, ptspin, ptglyph, ptsize, ptcol) in mm_petals[:14]:
        text ptglyph size ptsize color ptcol at mm_petal(ptx, ptx2, pty, ptdelay, ptdur, ptspin)

    # centered frosted panel
    frame:
        xalign 0.5
        yalign 0.5
        xsize 620
        padding (40, 30)
        background Solid("#fff3e8ee")
        at mm_fade_in(0.0)

        vbox:
            xalign 0.5
            spacing 2

            text _("Paused") style "mm_gm_title" size 72 xalign 0.5

            null height 6

            # divider
            hbox:
                xalign 0.5
                spacing 14
                add Solid("#c8567f99") xsize 140 ysize 3 yalign 0.5
                text "✿" size 28 color "#e0407f" yalign 0.5
                add Solid("#c8567f99") xsize 140 ysize 3 yalign 0.5

            null height 14

            vbox:
                xalign 0.5
                spacing 2

                use mm_pause_button(_("Resume"), Return())
                use mm_pause_button(_("Save"), ShowMenu("save"))
                use mm_pause_button(_("Load"), ShowMenu("load"))
                use mm_pause_button(_("History"), ShowMenu("history"))
                use mm_pause_button(_("Skip"), [Return(), Skip()])
                use mm_pause_button(_("Auto"), [Preference("auto-forward", "enable"), Return()])
                use mm_pause_button(_("Settings"), ShowMenu("preferences"))
                use mm_pause_button(_("Main Menu"), MainMenu())

    # Feet Points badge, same as the other menus
    use Fp_hud

    # ESC / right-click again closes the pause menu
    key "game_menu" action Return()


# One centered button (same hover outline as the other menus)
screen mm_pause_button(label, act):
    button:
        action act
        style "mm_plain_button"
        xsize 540
        ysize 68
        xalign 0.5
        at mm_nav_btn
        hover_sound None

        text label style "mm_nav_text" xalign 0.5 yalign 0.5
        
init python:
    def mm_pause_all_audio(paused):
        """
        Pause or resume every audio channel that can be paused.
        Works for music, sound, voice, and any custom channels.
        """
        for channel in ("music", "sound", "voice", "audio"):
            try:
                renpy.music.set_pause(paused, channel=channel)
            except Exception:
                # channel doesn't exist in this project — skip it
                pass
