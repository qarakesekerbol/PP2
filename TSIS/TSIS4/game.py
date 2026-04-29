"""
game.py — жыланның логикасы, тамақтар, улы тамақ,
          кедергілер, power-up-тар және деңгейлер.
"""
import pygame
import random
import time
from config import WIDTH, HEIGHT, CELL, SNAKE_COLORS

# ── Түстер ───────────────────────────────────────────────────────
colorBLACK  = (  0,   0,   0)
colorWHITE  = (255, 255, 255)
colorGRAY   = ( 40,  40,  40)
colorRED    = (255,   0,   0)
colorGREEN  = (  0, 255,   0)
colorBLUE   = (  0, 100, 255)
colorYELLOW = (255, 215,   0)
colorPURPLE = (128,   0, 128)
colorORANGE = (255, 165,   0)
colorPOISON = ( 80,   0, 140)   # улы тамақ түсі

COLS = WIDTH  // CELL
ROWS = HEIGHT // CELL


# ════════════════════════════════════════════════════════════════
# POINT
# ════════════════════════════════════════════════════════════════

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# ════════════════════════════════════════════════════════════════
# SNAKE
# ════════════════════════════════════════════════════════════════

class Snake:
    def __init__(self, color_name='red'):
        self.body    = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx      = 1
        self.dy      = 0
        self.score   = 0
        self.level   = 1
        self.alive   = True
        self.color   = SNAKE_COLORS.get(color_name, SNAKE_COLORS['red'])

        # Power-up күйлері
        self.shield        = False
        self.speed_boost   = False
        self.slow_motion   = False
        self.boost_end     = 0   # ms
        self.slow_end      = 0
        self.shield_used   = False

    # ── Қозғалыс ──────────────────────────────────────────────────
    def move(self, obstacles):
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        head = self.body[0]

        # Шекара
        if head.x >= COLS or head.x < 0 or head.y >= ROWS or head.y < 1:
            self._die()
            return

        # Өз денесіне соғылу
        for seg in self.body[1:]:
            if head == seg:
                self._die()
                return

        # Кедергіге соғылу
        for obs in obstacles:
            if head == obs:
                self._die()
                return

    def _die(self):
        if self.shield and not self.shield_used:
            self.shield      = False
            self.shield_used = True   # бір рет сақтайды
        else:
            self.alive = False

    # ── Тамақпен соқтығысу ────────────────────────────────────────
    def check_food(self, food, obstacles):
        if self.body[0] == food.pos:
            self.score += food.weight
            for _ in range(food.weight):
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
            food.generate(self.body, obstacles)
            self.level = 1 + self.score // 10
            return True
        return False

    def check_poison(self, poison):
        if poison.active and self.body[0] == poison.pos:
            # Ұзындықты 2-ге қысқарту
            for _ in range(2):
                if len(self.body) > 1:
                    self.body.pop()
                else:
                    self.alive = False
                    return True
            poison.respawn()
            return True
        return False

    def check_powerup(self, powerups):
        head = self.body[0]
        now  = pygame.time.get_ticks()
        for pu in powerups:
            if pu.active and head == pu.pos:
                if pu.kind == 'speed':
                    self.speed_boost = True
                    self.boost_end   = now + 5000
                elif pu.kind == 'slow':
                    self.slow_motion = True
                    self.slow_end    = now + 5000
                elif pu.kind == 'shield':
                    self.shield      = True
                    self.shield_used = False
                pu.collect()

    def update_powerups(self):
        now = pygame.time.get_ticks()
        if self.speed_boost and now > self.boost_end:
            self.speed_boost = False
        if self.slow_motion and now > self.slow_end:
            self.slow_motion = False

    def current_fps(self, base_fps):
        from config import BASE_FPS
        fps = base_fps + self.level
        if self.speed_boost:  fps += 4
        if self.slow_motion:  fps = max(2, fps - 4)
        return fps

    # ── Сызу ──────────────────────────────────────────────────────
    def draw(self, screen):
        for i, seg in enumerate(self.body):
            col = self.color if i == 0 else tuple(max(0, c-60) for c in self.color)
            pygame.draw.rect(screen, col,
                             (seg.x*CELL, seg.y*CELL, CELL-1, CELL-1))
        if self.shield:
            head = self.body[0]
            pygame.draw.rect(screen, (100, 200, 255),
                             (head.x*CELL-2, head.y*CELL-2, CELL+3, CELL+3), 2)


# ════════════════════════════════════════════════════════════════
# FOOD
# ════════════════════════════════════════════════════════════════

class Food:
    def __init__(self):
        self.pos      = Point(9, 9)
        self.weight   = 1
        self.color    = colorGREEN
        self.lifetime = 7
        self.born     = time.time()

    def generate(self, snake_body, obstacles):
        occupied = [(s.x, s.y) for s in snake_body] + [(o.x, o.y) for o in obstacles]
        while True:
            x = random.randint(0, COLS-1)
            y = random.randint(1, ROWS-1)
            if (x, y) not in occupied:
                self.pos = Point(x, y)
                break
        chance = random.randint(1, 100)
        if   chance <= 40: self.weight, self.color, self.lifetime = 1, colorGREEN,  8
        elif chance <= 70: self.weight, self.color, self.lifetime = 2, colorBLUE,   6
        elif chance <= 85: self.weight, self.color, self.lifetime = 3, colorORANGE, 5
        elif chance <= 95: self.weight, self.color, self.lifetime = 4, colorPURPLE, 4
        else:              self.weight, self.color, self.lifetime = 5, colorYELLOW, 3
        self.born = time.time()

    def update(self, snake_body, obstacles):
        if time.time() - self.born > self.lifetime:
            self.generate(snake_body, obstacles)

    def draw(self, screen, small_font):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL))
        lbl = small_font.render(str(self.weight), True,
                                colorBLACK if self.weight == 5 else colorWHITE)
        screen.blit(lbl, (self.pos.x*CELL+10, self.pos.y*CELL+5))


# ════════════════════════════════════════════════════════════════
# POISON FOOD  — жесе ұзындық -2
# ════════════════════════════════════════════════════════════════

class PoisonFood:
    def __init__(self):
        self.pos    = Point(-1, -1)
        self.active = False
        self.born   = 0

    def spawn(self, snake_body, obstacles):
        occupied = [(s.x, s.y) for s in snake_body] + [(o.x, o.y) for o in obstacles]
        for _ in range(100):
            x = random.randint(0, COLS-1)
            y = random.randint(1, ROWS-1)
            if (x, y) not in occupied:
                self.pos    = Point(x, y)
                self.active = True
                self.born   = time.time()
                return

    def respawn(self):
        self.active = False

    def update(self, snake_body, obstacles):
        if self.active and time.time() - self.born > 6:
            self.respawn()

    def draw(self, screen):
        if not self.active:
            return
        pygame.draw.rect(screen, colorPOISON,
                         (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL))
        pygame.draw.rect(screen, colorWHITE,
                         (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL), 2)
        f = pygame.font.Font(pygame.font.get_default_font(), 14)
        lbl = f.render('☠', True, colorWHITE)
        screen.blit(lbl, (self.pos.x*CELL+6, self.pos.y*CELL+5))


# ════════════════════════════════════════════════════════════════
# OBSTACLES  — Level 3-тен бастап пайда болады
# ════════════════════════════════════════════════════════════════

class Obstacles:
    def __init__(self):
        self.blocks = []   # Point тізімі
        self._last_level = 0

    def update(self, level, snake_body, food_pos):
        """Деңгей өскен сайын жаңа блок қосады."""
        if level < 3 or level <= self._last_level:
            return
        self._last_level = level
        occupied = ([(s.x, s.y) for s in snake_body]
                    + [(b.x, b.y) for b in self.blocks]
                    + [(food_pos.x, food_pos.y)])
        # Жыланды қамап тастамайтындай — тек бос орынға
        attempts = 0
        while attempts < 200:
            x = random.randint(0, COLS-1)
            y = random.randint(1, ROWS-1)
            if (x, y) not in occupied:
                # Жыланның басынан кем дегенде 5 ұяшық алыс болсын
                head = snake_body[0]
                if abs(x - head.x) + abs(y - head.y) > 4:
                    self.blocks.append(Point(x, y))
                    return
            attempts += 1

    def draw(self, screen):
        for b in self.blocks:
            pygame.draw.rect(screen, (120, 80, 40),
                             (b.x*CELL, b.y*CELL, CELL-1, CELL-1), border_radius=3)
            pygame.draw.rect(screen, (80, 50, 20),
                             (b.x*CELL, b.y*CELL, CELL-1, CELL-1), 2, border_radius=3)


# ════════════════════════════════════════════════════════════════
# POWER-UPS
# ════════════════════════════════════════════════════════════════

PU_COLORS = {
    'speed':  (255, 200,   0),
    'slow':   ( 80, 180, 255),
    'shield': (100, 255, 100),
}
PU_LABELS = {
    'speed': 'S+', 'slow': 'S-', 'shield': 'SH'
}

class PowerUp:
    LIFETIME = 8   # секунд

    def __init__(self, kind):
        self.kind   = kind
        self.pos    = Point(-1, -1)
        self.active = False
        self.born   = 0

    def spawn(self, snake_body, obstacles, food_pos):
        occupied = ([(s.x, s.y) for s in snake_body]
                    + [(o.x, o.y) for o in obstacles]
                    + [(food_pos.x, food_pos.y)])
        for _ in range(200):
            x = random.randint(0, COLS-1)
            y = random.randint(1, ROWS-1)
            if (x, y) not in occupied:
                self.pos    = Point(x, y)
                self.active = True
                self.born   = time.time()
                return

    def collect(self):
        self.active = False

    def update(self, snake_body, obstacles, food_pos):
        if self.active and time.time() - self.born > self.LIFETIME:
            self.active = False

    def draw(self, screen, small_font):
        if not self.active:
            return
        col = PU_COLORS[self.kind]
        pygame.draw.rect(screen, col,
                         (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL),
                         border_radius=6)
        lbl = small_font.render(PU_LABELS[self.kind], True, colorBLACK)
        screen.blit(lbl, (self.pos.x*CELL+4, self.pos.y*CELL+6))


# ════════════════════════════════════════════════════════════════
# GRID
# ════════════════════════════════════════════════════════════════

def draw_grid(screen):
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(screen, colorGRAY, (i, CELL), (i, HEIGHT))
    for i in range(CELL, HEIGHT, CELL):
        pygame.draw.line(screen, colorGRAY, (0, i), (WIDTH, i))