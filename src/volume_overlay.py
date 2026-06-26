import pygame
import src.theme as t

SHOW_MS   = 1500
FADE_MS   = 300
OVERLAY_W = 160
OVERLAY_H = 10
_BAR_PAD  = 2
_BAR_H    = OVERLAY_H - _BAR_PAD * 2
RADIUS    = OVERLAY_H // 2   # full pill

_volume = 0.8
_start  = None


def set_volume(v):
    global _volume, _start
    _volume = max(0.0, min(1.0, v))
    _start  = pygame.time.get_ticks()
    try:
        import src.state as state
        state.player.set_volume(_volume)
    except Exception:
        pass


def bump(delta):
    set_volume(_volume + delta)


def _draw_speaker(surface, x, y, w, h, alpha):
    col = (0, 0, 0, alpha)
    bw = w // 3
    by = y + h // 4
    pygame.draw.rect(surface, col, (x, by, bw, h // 2))
    pygame.draw.polygon(surface, col, [
        (x + bw,           y),
        (x + bw + w // 2,  y + h // 2),
        (x + bw,           y + h),
    ])


def draw(surface, fonts):
    if _start is None:
        return

    elapsed = pygame.time.get_ticks() - _start
    if elapsed > SHOW_MS + FADE_MS:
        return

    a = 255 if elapsed <= SHOW_MS else max(0, 255 - int(255 * (elapsed - SHOW_MS) / FADE_MS))

    ox = t.SCREEN_W // 2 - OVERLAY_W // 2
    oy = t.SCREEN_H - OVERLAY_H - 14

    # White 75% pill background
    pill = pygame.Surface((OVERLAY_W, OVERLAY_H), pygame.SRCALPHA)
    pygame.draw.rect(pill, (255, 255, 255, int(191 * a / 255)),
                     pill.get_rect(), border_radius=RADIUS)
    surface.blit(pill, (ox, oy))

    # Speaker icon (left side, vertically centred)
    icon_margin = 5
    icon_w, icon_h = 9, 8
    icon_x = ox + RADIUS + icon_margin
    icon_y = oy + (OVERLAY_H - icon_h) // 2
    icon_surf = pygame.Surface((icon_w, icon_h), pygame.SRCALPHA)
    _draw_speaker(icon_surf, 0, 0, icon_w, icon_h, a)
    surface.blit(icon_surf, (icon_x, icon_y))

    # Fill bar (black, rounded, inside pill)
    bar_x = icon_x + icon_w + icon_margin
    bar_y = oy + _BAR_PAD
    bar_w = OVERLAY_W - (bar_x - ox) - RADIUS - icon_margin
    fill_w = max(0, int(bar_w * _volume))
    if fill_w:
        fill_surf = pygame.Surface((bar_w, _BAR_H), pygame.SRCALPHA)
        pygame.draw.rect(fill_surf, (0, 0, 0, int(60 * a / 255)),
                         fill_surf.get_rect(), border_radius=_BAR_H // 2)
        pygame.draw.rect(fill_surf, (0, 0, 0, a),
                         (0, 0, fill_w, _BAR_H), border_radius=_BAR_H // 2)
        surface.blit(fill_surf, (bar_x, bar_y))
