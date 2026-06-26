import pygame

# iPod classic 6th gen colour palette
BG          = (30,  30,  30)
HEADER_BG   = (20,  20,  20)
HIGHLIGHT   = (59, 130, 246)   # iPod blue
TEXT        = (255, 255, 255)
TEXT_DIM    = (160, 160, 160)
DIVIDER     = (60,  60,  60)
PANEL_BG    = (18,  18,  18)

# Layout
SCREEN_W    = 320
SCREEN_H    = 240
HEADER_H    = 28
LIST_W      = 175   # left panel width
PANEL_X     = LIST_W
PANEL_W     = SCREEN_W - LIST_W

# Typography
def load_fonts():
    fonts = {}
    try:
        fonts["header"] = pygame.font.SysFont("helveticaneue", 13, bold=True)
        fonts["item"]   = pygame.font.SysFont("helveticaneue", 13)
        fonts["small"]  = pygame.font.SysFont("helveticaneue", 11)
    except Exception:
        fonts["header"] = pygame.font.SysFont("arial", 13, bold=True)
        fonts["item"]   = pygame.font.SysFont("arial", 13)
        fonts["small"]  = pygame.font.SysFont("arial", 11)
    return fonts
