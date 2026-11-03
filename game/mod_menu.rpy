default mod_rollback_amount = "1"
default mod_rollback_remaining = 0
default mod_trust_idx = 0

init python:
    config.keymap['mod_menu'] = ['K_F2']

    def mod_add_fp(n):
        persistent.Fp = (persistent.Fp or 0) + n
        renpy.restart_interaction()

    def mod_set_fp(n):
        persistent.Fp = n
        renpy.restart_interaction()

    def mod_unlock_all():
        persistent.mm_unlocked = set([c[0] for c in mm_characters])
        renpy.notify("Unlocked all characters")

    def mod_lock_all():
        persistent.mm_unlocked = set()
        renpy.notify("Locked all characters")

    def mod_clear_shop():
        persistent.mm_owned = set()
        renpy.notify("Cleared owned shop items")

    def mod_wipe_all():
        persistent.Fp = 0
        persistent.mm_unlocked = set()
        persistent.mm_owned = set()
        persistent.game_started = False
        renpy.notify("Wiped all persistent data!")
        renpy.restart_interaction()

    def mod_do_rollback():
        try:
            n = int(store.mod_rollback_amount)
        except (ValueError, TypeError):
            n = 1
        n = max(1, min(n, 100))   # keep it between 1 and 100
        renpy.hide_screen("mod_menu")
        renpy.rollback(checkpoints=n, force=True, greedy=True)

    def mod_reset_trust():
        persistent.mm_trust = {}
        renpy.notify("Reset all trust")

    def mod_trust_cycle(step):
        store.mod_trust_idx = (store.mod_trust_idx + step) % len(mm_characters)
        renpy.restart_interaction()

    def mod_add_trust(n):
        cid = mm_characters[store.mod_trust_idx][0]
        mm_set_trust(cid, mm_get_trust(cid) + n)   # clamps between 0 and 100
        renpy.restart_interaction()

    def mod_set_trust(n):
        cid = mm_characters[store.mod_trust_idx][0]
        mm_set_trust(cid, n)
        renpy.restart_interaction()


# ---------- Animations ----------
transform mod_pop:
    on show, appear:
        alpha 0.0
        yoffset 40
        parallel:
            ease 0.35 alpha 1.0
        parallel:
            easeout_back 0.45 yoffset 0
    on hide:
        ease 0.2 alpha 0.0

transform mod_fade:
    on show, appear:
        alpha 0.0
        ease 0.3 alpha 1.0
    on hide:
        ease 0.2 alpha 0.0

transform mod_hover:
    on hover:
        ease 0.12 yoffset -3
    on idle:
        ease 0.18 yoffset 0

transform mod_twinkle(delay, dur):
    alpha 0.0
    pause delay
    block:
        ease dur alpha 1.0
        ease dur alpha 0.15
        repeat


# ---------- Styles (same look as the main menu) ----------
style mod_title:
    font gui.text_font
    size 64
    bold True
    color "#6b2d4a"
    outlines [(4, "#ffffff", 0, 0), (9, "#c8567f55", 0, 5)]

style mod_tagline:
    font gui.text_font
    size 20
    color "#b5688a"
    kerning 2

style mod_section:
    font gui.text_font
    size 26
    bold True
    color "#c8567f"
    outlines [(3, "#ffffffaa", 0, 1)]

style mod_label:
    font gui.text_font
    size 22
    color "#6b2d4a"

style mod_fp_caption:
    font gui.text_font
    size 16
    color "#b5688a"
    kerning 2

style mod_fp_amount:
    font gui.text_font
    size 44
    bold True
    color "#6b2d4a"
    outlines [(2, "#ffffff", 0, 0)]

style mod_pill_text:
    font gui.text_font
    size 22
    bold True
    color "#ffffff"
    xalign 0.5

style mod_input:
    font gui.text_font
    size 28
    bold True
    color "#6b2d4a"

style mod_credit:
    font gui.text_font
    size 18
    kerning 3
    outlines [(2, "#ffffff", 0, 0)]

style mod_hint:
    font gui.text_font
    size 16
    color "#8a4b6a99"


# ---------- Reusable pill button ----------
screen mod_pill(label, act, col="#e0407f", hov="#c8567f"):
    button:
        action act
        background Solid(col)
        hover_background Solid(hov)
        padding (22, 10)
        at mod_hover
        hover_sound None
        text label style "mod_pill_text"


# ---------- The mod menu ----------
screen mod_menu():
    modal True
    zorder 1000

    default wipe_armed = False

    # soft plum dim instead of plain black
    add Solid("#3f1c31b8") at mod_fade

    # twinkling sparkles around the card
    for (sx, sy, ssz, sdl, sdr) in [(0.12, 0.18, 36, 0.2, 1.4), (0.88, 0.14, 30, 0.8, 1.8),
                                    (0.08, 0.72, 26, 0.5, 1.6), (0.93, 0.68, 40, 1.1, 1.3),
                                    (0.20, 0.92, 28, 0.3, 2.0), (0.80, 0.90, 32, 0.9, 1.5)]:
        text "✦" size ssz color "#ffffff" xpos sx ypos sy xanchor 0.5 yanchor 0.5 at mod_twinkle(sdl, sdr)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        padding (6, 6)
        background Solid("#ffffff")
        at mod_pop

        frame:
            xfill True
            padding (50, 34, 50, 34)
            # cream background with a pink accent stripe down the left side
            background Fixed(Solid("#fff3e8"), Solid("#e0407f", xsize=8))

            vbox:
                spacing 18

                # ---- Header ----
                vbox:
                    xalign 0.5
                    spacing -2
                    text "✿  D E V  T O O L S  ✿" style "mod_tagline" xalign 0.5
                    text _("Mod Menu") style "mod_title" xalign 0.5

                    null height 10

                    # studio credit pill
                    frame:
                        xalign 0.5
                        padding (26, 6)
                        background Solid("#ffffffaa")

                        hbox:
                            spacing 14
                            yalign 0.5
                            text "✦" size 18 color "#e0407f" yalign 0.5 at mod_twinkle(0.3, 1.2)
                            text "{color=#b5688a}BY{/color}   {b}{color=#e0407f}ACTUALDYNAMIC STUDIO{/color}{/b}" style "mod_credit" yalign 0.5
                            text "✦" size 18 color "#e0407f" yalign 0.5 at mod_twinkle(0.9, 1.5)

                hbox:
                    xalign 0.5
                    spacing 14
                    add Solid("#c8567f99") xsize 260 ysize 3 yalign 0.5
                    text "✿" size 28 color "#e0407f" yalign 0.5
                    add Solid("#c8567f99") xsize 260 ysize 3 yalign 0.5

                # ---- Feet Points ----
                frame:
                    xfill True
                    padding (20, 12)
                    background Solid("#ffffffcc")

                    hbox:
                        spacing 20
                        yalign 0.5

                        add Fp_icon yalign 0.5

                        vbox:
                            yalign 0.5
                            spacing -4
                            text _("FEET POINTS") style "mod_fp_caption"
                            text str(persistent.Fp or 0) style "mod_fp_amount"

                        null width 10

                        hbox:
                            spacing 10
                            yalign 0.5
                            use mod_pill(_("+10"),  Function(mod_add_fp, 10))
                            use mod_pill(_("+100"), Function(mod_add_fp, 100))
                            use mod_pill(_("-10"),  Function(mod_add_fp, -10), "#b5688a", "#8a4b6a")
                            use mod_pill(_("Zero"), Function(mod_set_fp, 0),   "#b5688a", "#8a4b6a")

                # ---- Characters + Shop (side by side) ----
                hbox:
                    spacing 40

                    vbox:
                        spacing 10
                        text _("Characters") style "mod_section"
                        hbox:
                            spacing 10
                            use mod_pill(_("Unlock All"), Function(mod_unlock_all), "#e0407f", "#c8567f")
                            use mod_pill(_("Lock All"),   Function(mod_lock_all),   "#b5688a", "#8a4b6a")
                            use mod_pill(_("Reset Trust"), Function(mod_reset_trust), "#b5688a", "#8a4b6a")

                    vbox:
                        spacing 10
                        text _("Shop") style "mod_section"
                        use mod_pill(_("Reset Owned Items"), Function(mod_clear_shop), "#b5688a", "#8a4b6a")
                        
                # ---- Trust ----
                vbox:
                    spacing 10
                    text _("Trust") style "mod_section"

                    hbox:
                        spacing 10
                        yalign 0.5

                        $ t_cid = mm_characters[mod_trust_idx][0]
                        $ t_name = mm_characters[mod_trust_idx][1]

                        use mod_pill("◀", Function(mod_trust_cycle, -1), "#b5688a", "#8a4b6a")

                        frame:
                            background Solid("#ffffff")
                            padding (12, 8)
                            xsize 170
                            yalign 0.5
                            text t_name style "mod_label" xalign 0.5

                        use mod_pill("▶", Function(mod_trust_cycle, 1), "#b5688a", "#8a4b6a")

                        null width 6
                        text (str(mm_get_trust(t_cid)) + " / 100") style "mod_label" yalign 0.5
                        null width 6

                        use mod_pill("+10", Function(mod_add_trust, 10))
                        use mod_pill("-10", Function(mod_add_trust, -10), "#b5688a", "#8a4b6a")
                        use mod_pill("Max", Function(mod_set_trust, 100))
                        use mod_pill("Zero", Function(mod_set_trust, 0), "#b5688a", "#8a4b6a")

                # ---- Rewind ----
                vbox:
                    spacing 10
                    text _("Rewind") style "mod_section"

                    hbox:
                        spacing 14
                        yalign 0.5

                        frame:
                            background Solid("#ffffff")
                            padding (16, 6)
                            xsize 100
                            yalign 0.5
                            input value VariableInputValue("mod_rollback_amount") length 3 allow "0123456789" style "mod_input"

                        text _("lines") style "mod_label" yalign 0.5

                        use mod_pill("1",  SetVariable("mod_rollback_amount", "1"),  "#b5688a", "#8a4b6a")
                        use mod_pill("5",  SetVariable("mod_rollback_amount", "5"),  "#b5688a", "#8a4b6a")
                        use mod_pill("10", SetVariable("mod_rollback_amount", "10"), "#b5688a", "#8a4b6a")

                        null width 10

                        use mod_pill(_("◀◀  Rewind"), Function(mod_do_rollback))

                    text _("Click the box to type a number (max 100). Only works in-game.") style "mod_hint"

                # ---- Danger zone + close ----
                add Solid("#c8567f55") xsize 860 ysize 2

                hbox:
                    xfill True

                    if wipe_armed:
                        use mod_pill(_("⚠  Really wipe? Click again"), [Function(mod_wipe_all), SetScreenVariable("wipe_armed", False)], "#c01818", "#8f0f0f")
                    else:
                        use mod_pill(_("⚠  Wipe All Data"), SetScreenVariable("wipe_armed", True), "#d9667f", "#c01818")

                    hbox:
                        xalign 1.0
                        use mod_pill(_("Close  (F2)"), Hide("mod_menu"), "#6b2d4a", "#3f1c31")

    key "mod_menu" action Hide("mod_menu")
    key "game_menu" action Hide("mod_menu")
