import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's clock")
clock = pygame.time.Clock()

# Суреттерді жүктеу (Жолдарын өзіңе ыңғайлап тексер)
path = 'Practice9/mickeys_clock/images/'
clc_image = pygame.image.load(path + 'mickeyclocks.png') # Егер .jpeg болса, солай жаз
clc_image = pygame.transform.scale(clc_image, (1100, 700))

# Қолдарды жүктеу
right_hand_img = pygame.image.load(path + 'hand_rights.png') # Минуттық
right_hand_img = pygame.transform.scale(right_hand_img, (400, 400)) # Өлшемін үлкейттім

left_hand_img = pygame.image.load(path + 'hand_lefts.png')   # Секундтық
left_hand_img = pygame.transform.scale(left_hand_img, (400, 400))

# Орталық нүкте
center_x, center_y = WIDTH // 2, HEIGHT // 2

def rotate(image, angle, x, y):
    # -angle сағат тілімен айналдыру үшін. 
    # Егер қолдар 12-ден бастамаса, (angle + 90) деп көру керек
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=(x, y))
    return rotated_image, new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    
    # Градустарды есептеу
    m_angle = minutes * 6 # 360 / 60
    s_angle = seconds * 6
    
    # Айналдыру (Орталық нүктеге қатысты)
    rotated_right, right_rect = rotate(right_hand_img, m_angle, center_x, center_y)
    rotated_left, left_rect = rotate(left_hand_img, s_angle, center_x, center_y)
    
    screen.fill((255, 255, 255))
    
    # 1. Циферблатты ортаға қою
    clock_rect = clc_image.get_rect(center=(center_x, center_y))
    screen.blit(clc_image, clock_rect)
    
    # 2. Қолдарды шығару (rect-тің өзін беру жеткілікті)
    screen.blit(rotated_right, right_rect)
    screen.blit(rotated_left, left_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()