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

def draw_battery(surface, fonts, level=1.0):
    """Draw battery icon top-right of header. level: 0.0–1.0 (placeholder until Pi GPIO)."""
    import pygame
    bw, bh = 20, 10
    x = SCREEN_W - bw - 6
    y = HEADER_H // 2 - bh // 2
    nub_w, nub_h = 2, 4
    pygame.draw.rect(surface, TEXT_DIM, (x, y, bw, bh), 1, border_radius=2)
    pygame.draw.rect(surface, TEXT_DIM, (x + bw, y + (bh - nub_h) // 2, nub_w, nub_h))
    fill_w = max(0, int((bw - 4) * level))
    if fill_w:
        col = (80, 200, 80) if level > 0.2 else (220, 60, 60)
        pygame.draw.rect(surface, col, (x + 2, y + 2, fill_w, bh - 4), border_radius=1)


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
