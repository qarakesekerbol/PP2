import pygame
from pygame.locals import *
from persistence import load_leaderboard, save_settings

# ── Colour palette ──────────────────────────────────────────────
BG        = (15,  15,  25)
PANEL     = (25,  25,  45)
ACCENT    = (0,  220, 180)
ACCENT2   = (255, 80,  80)
WHITE     = (255, 255, 255)
GRAY      = (140, 140, 160)
DARK_GRAY = (60,  60,  80)
GOLD      = (255, 215,   0)
SILVER    = (192, 192, 192)
GREEN     = (60,  200,  80)
RED       = (220,  50,  50)
YELLOW    = (255, 220,   0)

CAR_COLORS = {
    'default': (220, 60, 60),
    'blue':    (60, 120, 220),
    'green':   (60, 200, 80),
    'yellow':  (255, 220, 0),
    'purple':  (160, 60, 220),
}

DIFFICULTIES = ['easy', 'normal', 'hard']

# ── Helpers ──────────────────────────────────────────────────────

def _font(size):
    return pygame.font.Font(pygame.font.get_default_font(), size)

def draw_panel(surf, rect, radius=12, alpha=210):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*PANEL, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))

def draw_button(surf, text, rect, hover=False, color=ACCENT):
    col = tuple(min(255, c + 40) for c in color) if hover else color
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*col, 230), (0, 0, rect[2], rect[3]), border_radius=8)
    surf.blit(s, (rect[0], rect[1]))
    label = _font(22).render(text, True, BG if hover else WHITE)
    surf.blit(label, label.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2)))
    return pygame.Rect(rect)

def draw_title(surf, text, y, size=54, color=ACCENT):
    f = _font(size)
    lbl = f.render(text, True, color)
    surf.blit(lbl, lbl.get_rect(centerx=surf.get_width()//2, top=y))

def draw_stars(surf, n=60):
    """Simple static starfield drawn each frame using a seeded list."""
    pass  # stars generated externally for performance

# ── Star background ──────────────────────────────────────────────

import random as _rnd
_rnd.seed(42)
STARS = [(_rnd.randint(0,1000), _rnd.randint(0,1000), _rnd.randint(1,3)) for _ in range(80)]

def draw_bg(surf, tick):
    surf.fill(BG)
    for sx, sy, sr in STARS:
        alpha = 120 + int(60 * abs((tick % 120) / 60 - 1))
        pygame.draw.circle(surf, (alpha, alpha, alpha), (sx, sy), sr)

# ════════════════════════════════════════════════════════════════
# USERNAME ENTRY
# ════════════════════════════════════════════════════════════════

def username_screen(screen, clock):
    name = ''
    tick = 0
    while True:
        tick += 1
        draw_bg(screen, tick)
        W, H = screen.get_size()
        draw_panel(screen, (W//2-220, H//2-100, 440, 200))
        draw_title(screen, 'RACER', H//2-200, color=ACCENT)

        prompt = _font(26).render('Enter your name:', True, GRAY)
        screen.blit(prompt, prompt.get_rect(centerx=W//2, top=H//2-80))

        # Input box
        box_rect = (W//2-150, H//2-30, 300, 50)
        pygame.draw.rect(screen, DARK_GRAY, box_rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT, box_rect, 2, border_radius=6)
        txt_surf = _font(28).render(name + ('|' if tick % 60 < 30 else ''), True, WHITE)
        screen.blit(txt_surf, txt_surf.get_rect(center=(W//2, H//2-5)))

        hint = _font(18).render('Press ENTER to start', True, GRAY)
        screen.blit(hint, hint.get_rect(centerx=W//2, top=H//2+40))

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                return None
            if ev.type == KEYDOWN:
                if ev.key == K_RETURN and name.strip():
                    return name.strip()
                elif ev.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and ev.unicode.isprintable():
                    name += ev.unicode

# ════════════════════════════════════════════════════════════════
# MAIN MENU
# ════════════════════════════════════════════════════════════════

def main_menu(screen, clock):
    """Returns: 'play', 'leaderboard', 'settings', 'quit'"""
    buttons = [
        ('PLAY',        'play'),
        ('LEADERBOARD', 'leaderboard'),
        ('SETTINGS',    'settings'),
        ('QUIT',        'quit'),
    ]
    tick = 0
    while True:
        tick += 1
        W, H = screen.get_size()
        draw_bg(screen, tick)

        draw_title(screen, '🏎  RACER', 80, size=64, color=ACCENT)
        sub = _font(20).render('KBTU Edition', True, GRAY)
        screen.blit(sub, sub.get_rect(centerx=W//2, top=155))

        bw, bh, gap = 280, 52, 16
        start_y = H//2 - (len(buttons)*(bh+gap))//2

        mx, my = pygame.mouse.get_pos()
        action = None

        for i, (label, key) in enumerate(buttons):
            bx = W//2 - bw//2
            by = start_y + i*(bh+gap)
            col = ACCENT2 if key == 'quit' else ACCENT
            hover = pygame.Rect(bx, by, bw, bh).collidepoint(mx, my)
            r = draw_button(screen, label, (bx, by, bw, bh), hover, col)
            if hover and pygame.mouse.get_pressed()[0]:
                action = key

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                return 'quit'
            if ev.type == MOUSEBUTTONDOWN:
                mx, my = ev.pos
                for i, (label, key) in enumerate(buttons):
                    bx = W//2 - bw//2
                    by = start_y + i*(bh+gap)
                    if pygame.Rect(bx, by, bw, bh).collidepoint(mx, my):
                        return key

# ════════════════════════════════════════════════════════════════
# SETTINGS SCREEN
# ════════════════════════════════════════════════════════════════

def settings_screen(screen, clock, settings):
    """Mutates settings dict in-place, saves on Back."""
    tick = 0
    while True:
        tick += 1
        W, H = screen.get_size()
        draw_bg(screen, tick)
        draw_panel(screen, (W//2-260, 80, 520, H-160))
        draw_title(screen, 'SETTINGS', 100, size=42)

        mx, my = pygame.mouse.get_pos()
        clicked = False
        for ev in pygame.event.get():
            if ev.type == QUIT:
                save_settings(settings)
                return
            if ev.type == MOUSEBUTTONDOWN:
                clicked = True

        # ── Sound toggle ──────────────────────────────────────
        sy = 190
        lbl = _font(24).render('Sound:', True, WHITE)
        screen.blit(lbl, (W//2-220, sy))
        s_col = GREEN if settings['sound'] else RED
        s_text = 'ON' if settings['sound'] else 'OFF'
        s_rect = (W//2+60, sy-4, 100, 36)
        h = pygame.Rect(s_rect).collidepoint(mx, my)
        draw_button(screen, s_text, s_rect, h, s_col)
        if h and clicked:
            settings['sound'] = not settings['sound']

        # ── Car colour ────────────────────────────────────────
        sy = 270
        lbl = _font(24).render('Car colour:', True, WHITE)
        screen.blit(lbl, (W//2-220, sy))
        cx0 = W//2+20
        for i, (cname, cval) in enumerate(CAR_COLORS.items()):
            cr = pygame.Rect(cx0+i*44, sy-4, 36, 36)
            pygame.draw.rect(screen, cval, cr, border_radius=6)
            if settings['car_color'] == cname:
                pygame.draw.rect(screen, WHITE, cr, 3, border_radius=6)
            if cr.collidepoint(mx, my) and clicked:
                settings['car_color'] = cname

        # ── Difficulty ────────────────────────────────────────
        sy = 360
        lbl = _font(24).render('Difficulty:', True, WHITE)
        screen.blit(lbl, (W//2-220, sy))
        dw = 100
        for i, diff in enumerate(DIFFICULTIES):
            dr = (W//2-160+i*(dw+10), sy-4, dw, 36)
            active = settings['difficulty'] == diff
            col = ACCENT if active else DARK_GRAY
            h = pygame.Rect(dr).collidepoint(mx, my)
            draw_button(screen, diff.upper(), dr, h, col)
            if h and clicked:
                settings['difficulty'] = diff

        # ── Back ──────────────────────────────────────────────
        br = (W//2-80, H-180, 160, 48)
        h = pygame.Rect(br).collidepoint(mx, my)
        draw_button(screen, 'BACK', br, h, GRAY)
        if h and clicked:
            save_settings(settings)
            return

        pygame.display.flip()
        clock.tick(60)

# ════════════════════════════════════════════════════════════════
# LEADERBOARD SCREEN
# ════════════════════════════════════════════════════════════════

def leaderboard_screen(screen, clock):
    tick = 0
    board = load_leaderboard()
    medals = {0: GOLD, 1: SILVER, 2: (205,127,50)}
    while True:
        tick += 1
        W, H = screen.get_size()
        draw_bg(screen, tick)
        draw_panel(screen, (W//2-280, 70, 560, H-160))
        draw_title(screen, 'LEADERBOARD', 90, size=40, color=GOLD)

        # Header
        hf = _font(18)
        cols = [(W//2-240,'#'), (W//2-200,'Name'), (W//2+20,'Score'), (W//2+130,'Dist'), (W//2+230,'Coins')]
        for cx, ch in cols:
            screen.blit(hf.render(ch, True, GRAY), (cx, 148))
        pygame.draw.line(screen, DARK_GRAY, (W//2-250, 172), (W//2+260, 172), 1)

        rf = _font(20)
        for i, entry in enumerate(board[:10]):
            ry = 182 + i*44
            col = medals.get(i, WHITE)
            rank_txt = f'{i+1}.'
            screen.blit(rf.render(rank_txt, True, col), (W//2-240, ry))
            screen.blit(rf.render(entry.get('name','?')[:14], True, WHITE), (W//2-200, ry))
            screen.blit(rf.render(str(entry.get('score',0)), True, ACCENT), (W//2+20, ry))
            screen.blit(rf.render(f"{entry.get('distance',0)}m", True, GRAY), (W//2+130, ry))
            screen.blit(rf.render(str(entry.get('coins',0)), True, GOLD), (W//2+230, ry))

        mx, my = pygame.mouse.get_pos()
        br = (W//2-80, H-150, 160, 46)
        h = pygame.Rect(br).collidepoint(mx, my)
        draw_button(screen, 'BACK', br, h, GRAY)

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                return
            if ev.type == MOUSEBUTTONDOWN:
                if pygame.Rect(br).collidepoint(ev.pos):
                    return
            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                return

# ════════════════════════════════════════════════════════════════
# GAME OVER SCREEN
# ════════════════════════════════════════════════════════════════

def game_over_screen(screen, clock, score, distance, coins):
    """Returns 'retry' or 'menu'."""
    tick = 0
    while True:
        tick += 1
        W, H = screen.get_size()
        draw_bg(screen, tick)
        draw_panel(screen, (W//2-240, H//2-200, 480, 400))

        draw_title(screen, 'GAME OVER', H//2-185, size=46, color=ACCENT2)

        stats = [
            ('Score',    str(score),           ACCENT),
            ('Distance', f'{int(distance)} m', WHITE),
            ('Coins',    str(coins),            GOLD),
        ]
        sf = _font(26)
        for i, (k, v, c) in enumerate(stats):
            ky = H//2-100+i*54
            screen.blit(sf.render(k+':', True, GRAY), (W//2-200, ky))
            screen.blit(sf.render(v,     True, c),    (W//2+30,  ky))

        mx, my = pygame.mouse.get_pos()
        btns = [('RETRY', 'retry', ACCENT), ('MAIN MENU', 'menu', GRAY)]
        bw, bh = 180, 48
        for i, (txt, key, col) in enumerate(btns):
            bx = W//2 - bw - 10 + i*(bw+20)
            by = H//2 + 130
            h = pygame.Rect(bx, by, bw, bh).collidepoint(mx, my)
            draw_button(screen, txt, (bx, by, bw, bh), h, col)

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                return 'menu'
            if ev.type == MOUSEBUTTONDOWN:
                mx, my = ev.pos
                for i, (txt, key, col) in enumerate(btns):
                    bx = W//2 - bw - 10 + i*(bw+20)
                    by = H//2 + 130
                    if pygame.Rect(bx, by, bw, bh).collidepoint(mx, my):
                        return key
            if ev.type == KEYDOWN:
                if ev.key == K_r:
                    return 'retry'
                if ev.key == K_ESCAPE:
                    return 'menu'