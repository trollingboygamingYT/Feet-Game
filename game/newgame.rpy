init offset = 4

init python:

    def mm_reset_progress():
        persistent.Fp = mm_start_fp
        persistent.mm_unlocked = set()
        persistent.mm_owned = set()
        persistent.mm_status = {}
        persistent.mm_trust = {}
        persistent.mm_awarded_saves = {}   # <-- add
        renpy.save_persistent()

# The "are you sure?" popup. Uses your existing pink confirm screen.
define mm_confirm_new_game = Show(
    "confirm",
    message="Are you sure you want to start a new game?\nAll characters, Feet Points and trust will be reset.",
    yes_action=[Hide("confirm"), Start()],
    no_action=Hide("confirm"),
)