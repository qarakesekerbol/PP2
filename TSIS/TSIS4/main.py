"""
main.py — негізгі файл: экрандар, settings.json, ойын циклі.
"""
import pygame
import json
import os
import random
import time
from pygame.locals import *

from config  import (WIDTH, HEIGHT, CELL, BASE_FPS,
                     SETTINGS_FILE, DEFAULT_SETTINGS,
                     SNAKE_COLORS, BG_COLORS)
from game    import (Snake, Food, PoisonFood, Obstacles,
                     PowerUp, draw_grid,
                     colorWHITE, colorBLACK, colorRED,
                     colorGREEN, colorYELLOW, colorGRAY)
from db      import init_db, save_score, get_top10, get_personal_best

# ════════════════════════════════════════════════════════════════
# SETTINGS  JSON
# ════════════════════════════════════════════════════════════════

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
                for k, v in DEFAULT_SETTINGS.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(cfg):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

# ════════════════════════════════════════════════════════════════
# PYGAME INIT
# ════════════════════════════════════════════════════════════════

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake — KBTU Edition")
clock = pygame.time.Clock()

font       = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24)
big_font   = pygame.font.SysFont(None, 48)

settings = load_settings()
init_db()

# ════════════════════════════════════════════════════════════════
# UI HELPERS
# ════════════════════════════════════════════════════════════════

def draw_button(text, cx, cy, w=200, h=44, hover=False):
    col  = (80, 160, 80) if hover else (50, 120, 50)
    rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
    pygame.draw.rect(screen, col, rect, border_radius=8)
    pygame.draw.rect(screen, colorWHITE, rect, 2, border_radius=8)
    lbl = font.render(text, True, colorWHITE)
    screen.blit(lbl, lbl.get_rect(center=(cx, cy)))
    return rect

def draw_bg():
    screen.fill(BG_COLORS.get(settings['bg_color'], colorBLACK))

# ════════════════════════════════════════════════════════════════
# USERNAME ENTRY SCREEN
# ════════════════════════════════════════════════════════════════

def username_screen():
    name  = ''
    tick  = 0
    while True:
        tick += 1
        draw_bg()
        title = big_font.render('SNAKE', True, colorGREEN)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, top=120))

        prompt = font.render('Enter your name:', True, colorWHITE)
        screen.blit(prompt, prompt.get_rect(centerx=WIDTH//2, top=220))

        # Input box
        box = pygame.Rect(WIDTH//2-120, 260, 240, 44)
        pygame.draw.rect(screen, (40, 40, 60), box, border_radius=6)
        pygame.draw.rect(screen, colorGREEN, box, 2, border_radius=6)
        cursor = '|' if tick % 60 < 30 else ''
        inp = font.render(name + cursor, True, colorWHITE)
        screen.blit(inp, inp.get_rect(center=box.center))

        hint = small_font.render('Press ENTER to start', True, colorGRAY)
        screen.blit(hint, hint.get_rect(centerx=WIDTH//2, top=320))

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

def main_menu():
    buttons = [('PLAY', 'play'), ('LEADERBOARD', 'lb'),
               ('SETTINGS', 'settings'), ('QUIT', 'quit')]
    while True:
        draw_bg()
        title = big_font.render('SNAKE', True, colorGREEN)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, top=80))

        mx, my = pygame.mouse.get_pos()
        rects  = {}
        for i, (txt, key) in enumerate(buttons):
            cy = 220 + i * 70
            hover = pygame.Rect(WIDTH//2-100, cy-22, 200, 44).collidepoint(mx, my)
            r = draw_button(txt, WIDTH//2, cy, hover=hover)
            rects[key] = r

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                return 'quit'
            if ev.type == MOUSEBUTTONDOWN:
                for key, r in rects.items():
                    if r.collidepoint(ev.pos):
                        return key

# ════════════════════════════════════════════════════════════════
# SETTINGS SCREEN
# ════════════════════════════════════════════════════════════════

def settings_screen():
    while True:
        draw_bg()
        title = font.render('SETTINGS', True, colorGREEN)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, top=40))

        mx, my = pygame.mouse.get_pos()
        clicked = False
        for ev in pygame.event.get():
            if ev.type == QUIT:
                save_settings(settings)
                return
            if ev.type == MOUSEBUTTONDOWN:
                clicked = True
            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                save_settings(settings)
                return

        # ── Дыбыс ──────────────────────────────────────────────
        sy = 110
        screen.blit(font.render('Sound:', True, colorWHITE), (80, sy))
        s_txt = 'ON' if settings['sound'] else 'OFF'
        s_col = (50,200,50) if settings['sound'] else (200,50,50)
        sr = pygame.Rect(280, sy-4, 80, 32)
        pygame.draw.rect(screen, s_col, sr, border_radius=6)
        screen.blit(font.render(s_txt, True, colorWHITE),
                    font.render(s_txt, True, colorWHITE).get_rect(center=sr.center))
        if sr.collidepoint(mx, my) and clicked:
            settings['sound'] = not settings['sound']

        # ── Жылан түсі ──────────────────────────────────────────
        sy = 170
        screen.blit(font.render('Snake color:', True, colorWHITE), (80, sy))
        for i, (cname, cval) in enumerate(SNAKE_COLORS.items()):
            cr = pygame.Rect(80 + i*60, sy+30, 48, 28)
            pygame.draw.rect(screen, cval, cr, border_radius=4)
            if settings['snake_color'] == cname:
                pygame.draw.rect(screen, colorWHITE, cr, 3, border_radius=4)
            if cr.collidepoint(mx, my) and clicked:
                settings['snake_color'] = cname

        # ── Фон түсі ────────────────────────────────────────────
        sy = 260
        screen.blit(font.render('Background:', True, colorWHITE), (80, sy))
        bg_opts = list(BG_COLORS.items())
        for i, (bname, bval) in enumerate(bg_opts):
            br = pygame.Rect(80 + i*80, sy+30, 68, 28)
            pygame.draw.rect(screen, bval if bval != (0,0,0) else (30,30,30), br, border_radius=4)
            pygame.draw.rect(screen, colorWHITE, br, 1, border_radius=4)
            if settings['bg_color'] == bname:
                pygame.draw.rect(screen, colorGREEN, br, 3, border_radius=4)
            lbl = small_font.render(bname, True, colorWHITE)
            screen.blit(lbl, (br.x+2, br.y+7))
            if br.collidepoint(mx, my) and clicked:
                settings['bg_color'] = bname

        # ── Back ────────────────────────────────────────────────
        br2 = draw_button('BACK', WIDTH//2, 480,
                          hover=pygame.Rect(WIDTH//2-100, 458, 200, 44).collidepoint(mx, my))
        if br2.collidepoint(mx, my) and clicked:
            save_settings(settings)
            return

        pygame.display.flip()
        clock.tick(60)

# ════════════════════════════════════════════════════════════════
# LEADERBOARD SCREEN
# ════════════════════════════════════════════════════════════════

def leaderboard_screen():
    board = get_top10()
    while True:
        draw_bg()
        title = font.render('TOP 10', True, colorYELLOW)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, top=20))

        hdr = small_font.render('#   Name              Score  Lvl', True, colorGRAY)
        screen.blit(hdr, (40, 55))
        pygame.draw.line(screen, colorGRAY, (40, 72), (WIDTH-40, 72))

        medals = {0:(255,215,0), 1:(192,192,192), 2:(205,127,50)}
        for i, e in enumerate(board):
            col = medals.get(i, colorWHITE)
            row = small_font.render(
                f"{i+1:<3} {e['name'][:16]:<17} {e['score']:<7} {e.get('level','-')}",
                True, col)
            screen.blit(row, (40, 80 + i*38))

        mx, my = pygame.mouse.get_pos()
        br = draw_button('BACK', WIDTH//2, 530,
                         hover=pygame.Rect(WIDTH//2-100, 508, 200, 44).collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT: return
            if ev.type == MOUSEBUTTONDOWN:
                if br.collidepoint(ev.pos): return
            if ev.type == KEYDOWN and ev.key == K_ESCAPE: return

# ════════════════════════════════════════════════════════════════
# GAME OVER SCREEN
# ════════════════════════════════════════════════════════════════

def gameover_screen(score, level, personal_best):
    while True:
        draw_bg()
        go = big_font.render('GAME OVER', True, colorRED)
        screen.blit(go, go.get_rect(centerx=WIDTH//2, top=140))

        lines = [
            (f'Score: {score}',          colorWHITE),
            (f'Level: {level}',          colorWHITE),
            (f'Personal Best: {personal_best}', colorYELLOW),
        ]
        for i, (txt, col) in enumerate(lines):
            lbl = font.render(txt, True, col)
            screen.blit(lbl, lbl.get_rect(centerx=WIDTH//2, top=240+i*42))

        mx, my = pygame.mouse.get_pos()
        btns = [('RETRY', 'retry'), ('MAIN MENU', 'menu')]
        rects = {}
        for i, (txt, key) in enumerate(btns):
            cx = WIDTH//2 - 110 + i*220
            hover = pygame.Rect(cx-90, 398, 180, 44).collidepoint(mx, my)
            rects[key] = draw_button(txt, cx, 420, w=180, hover=hover)

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT: return 'menu'
            if ev.type == MOUSEBUTTONDOWN:
                for key, r in rects.items():
                    if r.collidepoint(ev.pos): return key
            if ev.type == KEYDOWN:
                if ev.key == K_r: return 'retry'
                if ev.key == K_ESCAPE: return 'menu'

# ════════════════════════════════════════════════════════════════
# PLAY  —  негізгі ойын
# ════════════════════════════════════════════════════════════════

def play(player_name):
    snake     = Snake(settings['snake_color'])
    food      = Food()
    poison    = PoisonFood()
    obstacles = Obstacles()
    powerups  = [PowerUp('speed'), PowerUp('slow'), PowerUp('shield')]

    food.generate(snake.body, [])

    frame        = 0
    poison_timer = 0
    pu_timer     = 0

    while True:
        fps = snake.current_fps(BASE_FPS)
        clock.tick(fps)
        frame += 1

        for ev in pygame.event.get():
            if ev.type == QUIT:
                save_score(player_name, snake.score, snake.level)
                return 'quit'
            if ev.type == KEYDOWN:
                if ev.key == K_RIGHT and snake.dx != -1: snake.dx, snake.dy =  1,  0
                elif ev.key == K_LEFT  and snake.dx !=  1: snake.dx, snake.dy = -1,  0
                elif ev.key == K_UP    and snake.dy !=  1: snake.dx, snake.dy =  0, -1
                elif ev.key == K_DOWN  and snake.dy != -1: snake.dx, snake.dy =  0,  1
                elif ev.key == K_ESCAPE:
                    save_score(player_name, snake.score, snake.level)
                    return 'menu'

        # ── Жаңарту ──────────────────────────────────────────────
        snake.update_powerups()
        food.update(snake.body, obstacles.blocks)
        poison.update(snake.body, obstacles.blocks)
        for pu in powerups:
            pu.update(snake.body, obstacles.blocks, food.pos)

        snake.move(obstacles.blocks)
        if not snake.alive:
            break

        snake.check_food(food, obstacles.blocks)
        snake.check_poison(poison)
        if not snake.alive:
            break
        snake.check_powerup(powerups)

        # Кедергі спавны (Level 3+)
        obstacles.update(snake.level, snake.body, food.pos)

        # Улы тамақ спавны (әр 15 секунд)
        if not poison.active and time.time() - poison_timer > 15:
            poison.spawn(snake.body, obstacles.blocks)
            poison_timer = time.time()

        # Power-up спавны (әр 20 секунд, кездейсоқ бірі)
        if time.time() - pu_timer > 20:
            inactive = [p for p in powerups if not p.active]
            if inactive:
                random.choice(inactive).spawn(snake.body, obstacles.blocks, food.pos)
            pu_timer = time.time()

        # ── Сызу ─────────────────────────────────────────────────
        draw_bg()
        draw_grid(screen)
        obstacles.draw(screen)
        food.draw(screen, small_font)
        poison.draw(screen)
        for pu in powerups:
            pu.draw(screen, small_font)
        snake.draw(screen)

        # ── HUD ──────────────────────────────────────────────────
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, CELL))
        screen.blit(font.render(f'Score: {snake.score}', True, colorWHITE), (10, 2))
        screen.blit(font.render(f'Level: {snake.level}', True, colorWHITE), (180, 2))
        screen.blit(font.render(player_name, True, colorGREEN),
                    font.render(player_name, True, colorGREEN).get_rect(right=WIDTH-10, top=2))

        # Power-up таймерлері
        now = pygame.time.get_ticks()
        pu_y = CELL + 4
        if snake.speed_boost:
            sec = max(0, (snake.boost_end - now) // 1000)
            screen.blit(small_font.render(f'SPEED +{sec}s', True, (255,200,0)), (10, pu_y))
            pu_y += 20
        if snake.slow_motion:
            sec = max(0, (snake.slow_end - now) // 1000)
            screen.blit(small_font.render(f'SLOW  {sec}s', True, (80,180,255)), (10, pu_y))
            pu_y += 20
        if snake.shield:
            screen.blit(small_font.render('SHIELD ✓', True, (100,255,100)), (10, pu_y))

        pygame.display.flip()

    # ── Ойын аяқталды ────────────────────────────────────────────
    save_score(player_name, snake.score, snake.level)
    pb = get_personal_best(player_name)
    return gameover_screen(snake.score, snake.level, pb)

# ════════════════════════════════════════════════════════════════
# MAIN LOOP
# ════════════════════════════════════════════════════════════════

def main():
    player_name = None

    while True:
        choice = main_menu()

        if choice == 'quit':
            break
        elif choice == 'lb':
            leaderboard_screen()
        elif choice == 'settings':
            settings_screen()
        elif choice == 'play':
            if player_name is None:
                name = username_screen()
                if name is None:
                    break
                player_name = name

            result = play(player_name)
            if result == 'quit':
                break
            elif result == 'menu':
                player_name = None  # келесі ойында атты қайта сұрайды

    save_settings(settings)
    pygame.quit()


if __name__ == '__main__':
    main()