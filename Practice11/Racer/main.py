import pygame
from pygame.locals import *
import random

# Инициализация
pygame.init()

# Экран параметрлері
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Racer - KBTU Edition')

# Түстер
gray = (100, 100, 100)
green = (76, 209, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
gold_color = (255, 215, 0)
silver_color = (192, 192, 192)
bronze_color = (205, 127, 50)

# Жол параметрлері
marker_w, marker_h = 10, 50
road = (200, 0, 600, height)
left_m, right_m = (190, 0, 10, height), (790, 0, 10, height)

left_line, center_line, right_line = 300, 500, 700
lines = [left_line, center_line, right_line]

# --- КЛАСТАР ---

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 150 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('C:/Users/user/Downloads/Car.png')
        super().__init__(image, x, y)

# EXTRA TASK 1: Түрлі салмағы бар монеталар (Random weights)
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        chance = random.randint(1, 100)
        if chance <= 10: # 10% - Алтын (5 ұпай)
            self.weight = 5
            self.color = gold_color
        elif chance <= 40: # 30% - Күміс (3 ұпай)
            self.weight = 3
            self.color = silver_color
        else: # 60% - Қола (1 ұпай)
            self.weight = 1
            self.color = bronze_color
            
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (20, 20), 18)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 20), 18, 2) 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# --- ОБЪЕКТІЛЕРДІ БАПТАУ ---

player_group = pygame.sprite.Group()
player = PlayerVehicle(500, 800)
player_group.add(player)

image_filenames = ['mini_truck.png', 'mini_van.png', 'police.png', 'truck.png', 'taxi.png', 'ambulance.png', 'audi.png', 'black_viper.png']
transport = [pygame.image.load(f'Practice10/Racer/image/Topdown_vehicle_sprites_pack/{name}') for name in image_filenames]

vehicle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

crash_img = pygame.image.load('C:/Users/user/Downloads/crash.png')
bg_music = pygame.mixer.Sound('Practice10/Racer/A_BOO_Senen_basqa_Yeski_Taspa.mp3')
crash_sound = pygame.mixer.Sound('Practice10/Racer/craaash.mp3')

# Ойын айнымалылары
clock = pygame.time.Clock()
fps = 120
running = True
gameover = False
speed = 2
score = 0
coins_collected = 0
last_speed_milestone = 0 
y_move = 0

bg_music.play(-1)

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT: running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_line: player.rect.x -= 200
            elif event.key == K_RIGHT and player.rect.center[0] < right_line: player.rect.x += 200

    # Фон
    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, right_m)
    pygame.draw.rect(screen, yellow, left_m)

    # Жол сызықтары
    y_move += speed * 2
    if y_move >= marker_h * 2: y_move = 0
    for y in range(marker_h * -2, height, marker_h * 2):
        pygame.draw.rect(screen, white, (left_line + 90, y + y_move, marker_w, marker_h))
        pygame.draw.rect(screen, white, (center_line + 90, y + y_move, marker_w, marker_h))

    player_group.draw(screen)

    # Жаңа көліктер мен монеталар генерациясы
    if len(vehicle_group) < 2:
        add_v = True
        for v in vehicle_group:
            if v.rect.top < v.rect.height * 1.5: add_v = False
        if add_v:
            vehicle_group.add(Vehicle(random.choice(transport), random.choice(lines), height / -2))

    if random.randint(1, 100) == 1 and len(coin_group) < 3:
        coin_group.add(Coin(random.choice(lines), -50))

    # Қозғалыс логикасы
    for v in vehicle_group:
        v.rect.y += speed
        if v.rect.top >= height:
            v.kill()
            score += 1

    for c in coin_group:
        c.rect.y += speed
        if c.rect.top >= height: c.kill()

    vehicle_group.draw(screen)
    coin_group.draw(screen)

    # Монета жинау және EXTRA TASK 2: Жылдамдықты арттыру (N монета сайын)
    collected = pygame.sprite.spritecollide(player, coin_group, True)
    for coin in collected:
        coins_collected += coin.weight
        
    # Әр 5 монета (ұпай) сайын жылдамдықты 1-ге арттыру
    if coins_collected // 5 > last_speed_milestone:
        speed += 1
        last_speed_milestone = coins_collected // 5

    # --- Есептегіштерді шығару ---
    font = pygame.font.Font(pygame.font.get_default_font(), 30)

    # SPEED - СОЛ жақ жоғарыда
    speed_txt = font.render(f'Speed: {speed}', True, white)
    screen.blit(speed_txt, (20, 80)) 

    # SCORE мен COINS - ОҢ жақ жоғарыда
    score_txt = font.render(f'Score: {score}', True, white)
    screen.blit(score_txt, score_txt.get_rect(topright=(width - 20, 80)))

    coin_txt = font.render(f'Coins: {coins_collected}', True, gold_color)
    screen.blit(coin_txt, coin_txt.get_rect(topright=(width - 20, 120)))

    # Соқтығысуды тексеру
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        bg_music.stop()
        crash_sound.play()

    if gameover:
        screen.blit(crash_img, (player.rect.x, player.rect.y - 50))
        pygame.draw.rect(screen, red, (0, 100, width, 300))
        msg = font.render(f"GAME OVER! Coins: {coins_collected}", True, white)
        screen.blit(msg, msg.get_rect(center=(width/2, 200)))
        retry = font.render("Press Y to Restart or N to Quit", True, white)
        screen.blit(retry, retry.get_rect(center=(width/2, 260)))

    pygame.display.update()

    while gameover:
        for event in pygame.event.get():
            if event.type == QUIT: running = False; gameover = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False; speed = 2; score = 0; coins_collected = 0; last_speed_milestone = 0
                    vehicle_group.empty(); coin_group.empty(); player.rect.center = [500, 800]
                    bg_music.play(-1)
                elif event.key == K_n: running = False; gameover = False

pygame.quit()