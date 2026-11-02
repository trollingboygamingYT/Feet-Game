default mod_rollback_amount = "1"

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
        renpy.notify("Wiped all persistent data!")

screen mod_menu():
    modal True
    zorder 1000

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        background Solid("#2a2a2a")
        padding (40, 40)

        vbox:
            spacing 20
            text _("MOD MENU") size 40 bold True color "#ff4444" xalign 0.5
            
            text _("Feet Points: [persistent.Fp]") size 24 color "#ffffff" bold True
            hbox:
                spacing 15
                textbutton _("+10 FP") action Function(mod_add_fp, 10) text_color "#ffffff" text_hover_color "#ff88bb"
                textbutton _("+100 FP") action Function(mod_add_fp, 100) text_color "#ffffff" text_hover_color "#ff88bb"
                textbutton _("-10 FP") action Function(mod_add_fp, -10) text_color "#ffffff" text_hover_color "#ff88bb"
                textbutton _("Set to 0") action Function(mod_set_fp, 0) text_color "#ffffff" text_hover_color "#ff88bb"

            text _("Characters:") size 24 color "#ffffff" bold True
            hbox:
                spacing 15
                textbutton _("Unlock All") action Function(mod_unlock_all) text_color "#ffffff" text_hover_color "#88ffbb"
                textbutton _("Lock All") action Function(mod_lock_all) text_color "#ffffff" text_hover_color "#ff8888"

            text _("Shop:") size 24 color "#ffffff" bold True
            hbox:
                spacing 15
                textbutton _("Reset Owned Items") action Function(mod_clear_shop) text_color "#ffffff" text_hover_color "#ff8888"

            text _("Gameplay:") size 24 color "#ffffff" bold True
            hbox:
                spacing 15
                yalign 0.5
                
                text _("Rewind lines:") size 20 color "#aaaaaa" yalign 0.5
                
                # The input box
                frame:
                    background Solid("#444444")
                    padding (10, 5)
                    input:
                        value VariableInputValue("mod_rollback_amount")
                        length 3
                        color "#ffffff"
                        
                # The button that triggers the rewind
                textbutton _("⏪ Go Back") action [Hide("mod_menu"), Rollback(int(mod_rollback_amount) if mod_rollback_amount.isdigit() else 1)] text_color "#ffffff" text_hover_color "#ff88bb"

            null height 20
            textbutton _("⚠ WIPE ALL DATA (Reset Game)") action Function(mod_wipe_all) text_color "#ff0000" xalign 0.5
            
            null height 20
            textbutton _("Close Mod Menu (F2)") action Hide("mod_menu") xalign 0.5 text_color "#ffffff"
            
    key "mod_menu" action Hide("mod_menu")
    key "game_menu" action Hide("mod_menu")