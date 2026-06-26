import pygame

# Keyboard → DMG button mapping for Mac development
KEY_MAP = {
    pygame.K_UP:        "up",
    pygame.K_DOWN:      "down",
    pygame.K_LEFT:      "left",
    pygame.K_RIGHT:     "right",
    pygame.K_z:         "a",         # A / Select
    pygame.K_x:         "b",         # B / Back
    pygame.K_RETURN:    "a",
    pygame.K_BACKSPACE: "b",
    pygame.K_SPACE:     "start",     # Play / Pause
    pygame.K_s:         "select",    # Skip
    pygame.K_q:         "l",         # L trigger
    pygame.K_e:         "r",         # R trigger
}


def get_button(event):
    """Return button name string for a KEYDOWN event, or None."""
    if event.type == pygame.KEYDOWN:
        return KEY_MAP.get(event.key)
    return None
