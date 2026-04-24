import pygame
import random
import time
from pygame.locals import *

# Түстер
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorGRAY = (40, 40, 40)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 100, 255)
colorYELLOW = (255, 215, 0)
colorPURPLE = (128, 0, 128)
colorORANGE = (255, 165, 0)

pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 600, 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: 5 Types of Food")

font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24) # Фрукты үстіндегі сан үшін

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx, self.dy = 1, 0
        self.score = 0
        self.level = 1 
        self.alive = True

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Шекараны тексеру
        if self.body[0].x >= WIDTH // CELL or self.body[0].x < 0 or \
           self.body[0].y >= HEIGHT // CELL or self.body[0].y < 1:
            self.alive = False
            
        # Өз денесіне соғылу
        for segment in self.body[1:]:
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                self.alive = False

    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL - 1, CELL - 1))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.score += food.weight
            # Салмағына қарай өсу
            for _ in range(food.weight):
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
            
            food.generate_random_pos(self.body)
            self.level = 1 + self.score // 10 # Әр 10 ұпай сайын деңгей артады

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        self.color = colorGREEN
        self.spawn_time = time.time()
        self.lifetime = 7

    def generate_random_pos(self, snake_body):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(1, HEIGHT // CELL - 1)
            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body):
                break
        
        # 5 түрлі фрукты: салмақ, түс және өмір сүру уақыты
        chance = random.randint(1, 100)
        if chance <= 40: # 40% - 1 ұпай (Жасыл)
            self.weight, self.color, self.lifetime = 1, colorGREEN, 8
        elif chance <= 70: # 30% - 2 ұпай (Көк)
            self.weight, self.color, self.lifetime = 2, colorBLUE, 6
        elif chance <= 85: # 15% - 3 ұпай (Қызғылт сары)
            self.weight, self.color, self.lifetime = 3, colorORANGE, 5
        elif chance <= 95: # 10% - 4 ұпай (Күлгін)
            self.weight, self.color, self.lifetime = 4, colorPURPLE, 4
        else: # 5% - 5 ұпай (Алтын)
            self.weight, self.color, self.lifetime = 5, colorYELLOW, 3
            
        self.spawn_time = time.time()

    def update(self, snake_body):
        if time.time() - self.spawn_time > self.lifetime:
            self.generate_random_pos(snake_body)

    def draw(self):
        # Фруктыны сызу
        rect = (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        pygame.draw.rect(screen, self.color, rect)
        # Ұпайын үстіне жазу
        weight_text = small_font.render(str(self.weight), True, colorWHITE if self.weight != 5 else colorBLACK)
        screen.blit(weight_text, (self.pos.x * CELL + 10, self.pos.y * CELL + 5))

def draw_grid():
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(screen, colorGRAY, (i, CELL), (i, HEIGHT))
    for i in range(CELL, HEIGHT, CELL):
        pygame.draw.line(screen, colorGRAY, (0, i), (WIDTH, i))

# Ойын циклі
FPS = 5
clock = pygame.time.Clock()
snake = Snake()
food = Food()
food.generate_random_pos(snake.body)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and snake.dx != -1: snake.dx, snake.dy = 1, 0
            elif event.key == K_LEFT and snake.dx != 1: snake.dx, snake.dy = -1, 0
            elif event.key == K_UP and snake.dy != 1: snake.dx, snake.dy = 0, -1
            elif event.key == K_DOWN and snake.dy != -1: snake.dx, snake.dy = 0, 1

    if snake.alive:
        food.update(snake.body)
        snake.move()
        snake.check_collision(food)

        screen.fill(colorBLACK)
        draw_grid()
        snake.draw()
        food.draw()

        # Статистика
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, CELL))
        screen.blit(font.render(f"Score: {snake.score}", True, colorWHITE), (10, 2))
        screen.blit(font.render(f"Level: {snake.level}", True, colorWHITE), (200, 2))
    else:
        screen.fill(colorBLACK)
        screen.blit(font.render("GAME OVER", True, colorRED), (WIDTH//2 - 70, HEIGHT//2 - 20))
        screen.blit(font.render(f"Final Score: {snake.score}", True, colorWHITE), (WIDTH//2 - 75, HEIGHT//2 + 20))
        pygame.display.flip()
        time.sleep(3)
        running = False

    pygame.display.flip()
    clock.tick(FPS + snake.level)

pygame.quit()