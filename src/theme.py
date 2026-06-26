import pygame

# iPod Classic 6th gen light theme
BG         = (255, 255, 255)   # white
HEADER_BG  = (214, 214, 214)   # silver grey
HIGHLIGHT  = (59,  130, 246)   # iPod blue (gradient top)
HIGHLIGHT2 = (23,  83,  184)   # iPod blue (gradient bottom)
TEXT       = (0,   0,   0)     # black
TEXT_DIM   = (110, 110, 110)   # medium grey
TEXT_HI    = (255, 255, 255)   # white text on highlight
DIVIDER    = (195, 195, 195)   # light grey dividers
PANEL_BG   = (255, 255, 255)   # white panel

# Layout
SCREEN_W   = 320
SCREEN_H   = 240
HEADER_H   = 28
LIST_W     = 175
PANEL_X    = LIST_W
PANEL_W    = SCREEN_W - LIST_W


def draw_highlight(surface, rect, radius=0):
    """Draw the iPod-style blue gradient selection bar."""
    r = pygame.Rect(rect)
    mid = r.top + r.height // 2

    top_surf = pygame.Surface((r.width, r.height // 2), pygame.SRCALPHA)
    top_surf.fill(HIGHLIGHT)
    surface.blit(top_surf, (r.left, r.top))

    bot_surf = pygame.Surface((r.width, r.height - r.height // 2), pygame.SRCALPHA)
    bot_surf.fill(HIGHLIGHT2)
    surface.blit(bot_surf, (r.left, mid))


def draw_battery(surface, fonts, level=1.0):
    """Battery icon top-right of header. level: 0.0–1.0."""
    bw, bh = 20, 10
    x = SCREEN_W - bw - 6
    y = HEADER_H // 2 - bh // 2
    nub_w, nub_h = 2, 4
    pygame.draw.rect(surface, TEXT_DIM, (x, y, bw, bh), 1, border_radius=2)
    pygame.draw.rect(surface, TEXT_DIM, (x + bw, y + (bh - nub_h) // 2, nub_w, nub_h))
    fill_w = max(0, int((bw - 4) * level))
    if fill_w:
        col = (60, 170, 60) if level > 0.2 else (200, 40, 40)
        pygame.draw.rect(surface, col, (x + 2, y + 2, fill_w, bh - 4), border_radius=1)


def draw_art_placeholder(surface, rect):
    """iPod-style dark grey art placeholder with a drawn music note."""
    r = pygame.Rect(rect)
    pygame.draw.rect(surface, (80, 80, 80), r, border_radius=4)
    col = (160, 160, 160)
    # Scale note to ~40% of the rect
    unit = max(4, r.height // 5)
    cx = r.centerx
    cy = r.centery + unit // 2
    # Filled note head (ellipse)
    head_w, head_h = int(unit * 1.1), int(unit * 0.8)
    pygame.draw.ellipse(surface, col,
                        (cx - head_w // 2, cy - head_h // 2, head_w, head_h))
    # Stem
    stem_h = int(unit * 1.6)
    pygame.draw.line(surface, col,
                     (cx + head_w // 2 - 1, cy),
                     (cx + head_w // 2 - 1, cy - stem_h), max(1, unit // 5))


def load_fonts():
    fonts = {}
    # Try fonts in order of preference — closest to iPod Classic appearance
    candidates = ["lucidagrande", "geneva", "helveticaneue", "arial"]
    chosen = None
    for name in candidates:
        f = pygame.font.SysFont(name, 13)
        if f is not None:
            chosen = name
            break
    if not chosen:
        chosen = None  # fallback to pygame default

    fonts["header"] = pygame.font.SysFont(chosen, 14, bold=True)
    fonts["item"]   = pygame.font.SysFont(chosen, 13)
    fonts["small"]  = pygame.font.SysFont(chosen, 12)
    return fonts
