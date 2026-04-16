import pygame
import os

# Егер Player класы бөлек файлда болса:
from player import Player 

pygame.init()
pygame.mixer.init()

player = Player()
# Мұнда музыка папкасына баратын жолды COPY RELATIVE PATH арқылы тексер
music_path = "Practice9/music_player/music"
player.load(music_path)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Music Player')

clock = pygame.time.Clock()

# Шрифтің бар екеніне көз жеткіз немесе жүйелік шрифт қолдан:
try:
    font = pygame.font.Font("fonts/MinecraftItalic-R8Mo.otf", 30)
except:
    font = pygame.font.SysFont("Arial", 30) # Егер шрифт табылмаса қате бермейді

# Мәтіндерді дайындау
play_txt = font.render("P - Play / Pause", True, 'White')
next_txt = font.render("N - Next", True, 'White')
stop_txt = font.render("S - Stop", True, 'White')
pre_txt = font.render("B - Previous", True, 'White') # P-ның орнына B деп өзгерттік
quit_txt = font.render("Q - Quit", True, 'White')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b: # Бұрынғы P-previous орнына
                player.pre()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_q:
                running = False    
    
    screen.fill((30, 30, 30))
    
    # Мәтіндерді шығару
    screen.blit(play_txt, (30, 170))
    screen.blit(stop_txt, (30, 200))
    screen.blit(next_txt, (30, 230))
    screen.blit(pre_txt, (30, 260))
    screen.blit(quit_txt, (30, 290))
    
    # Қазіргі трек атын шығару (player.tracks бос емес екеніне көз жеткізу керек)
    if player.tracks:
        track_name = os.path.basename(player.tracks[player.cur])
        text = font.render(f"Now Playing: {track_name}", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        
        status = "Playing" if player.playing else "Stopped"
        status_text = font.render(f"Status: {status}", True, (0, 255, 0))
        screen.blit(status_text, (50, 100))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()