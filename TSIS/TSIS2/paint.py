import pygame
import datetime
import os
from pygame.locals import *
from tools import flood_fill, draw_shape

# Папканы тексеру
if not os.path.exists("assets"):
    os.makedirs("assets")

pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 1000, 750
CANVAS_Y = 110
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2: Professional Paint")

# Түстер мен Қаріптер
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
# Палитра - барлық жерде осы тізім қолданылады
COLORS = [BLACK, (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (128,0,0), (0,128,0)]

font_ui = pygame.font.SysFont('Arial', 15)
font_canvas = pygame.font.SysFont('Arial', 24)

# Негізгі кенеп
canvas = pygame.Surface((WIDTH, HEIGHT - CANVAS_Y))
canvas.fill(WHITE)

# Құралдар тізімі
tools = ['Pencil', 'Line', 'Rect', 'Circle', 'Square', 'RightTri', 'EquiTri', 'Rhombus', 'Fill', 'Text', 'Eraser']

# Бастапқы күй
current_tool = 'Pencil'
current_color = BLACK
brush_size = 2
start_pos = None
prev_pos = None
is_typing = False
text_content = ""
text_pos = (0, 0)

running = True
clock = pygame.time.Clock()

while running:
    mx, my = pygame.mouse.get_pos()
    cx, cy = mx, my - CANVAS_Y

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_1: brush_size = 2
            if event.key == K_2: brush_size = 5
            if event.key == K_3: brush_size = 10
            
            if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas, f"assets/paint_{now}.png")
                print("Saved to assets folder")

            if is_typing:
                if event.key == K_RETURN:
                    txt_s = font_canvas.render(text_content, True, current_color)
                    canvas.blit(txt_s, text_pos)
                    is_typing = False
                elif event.key == K_ESCAPE:
                    is_typing = False
                elif event.key == K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode

        if event.type == MOUSEBUTTONDOWN:
            if my < CANVAS_Y: # Панельді басу
                # Құрал таңдау
                for i, t in enumerate(tools):
                    if 10 + i * 88 < mx < 93 + i * 88 and 10 < my < 45:
                        current_tool = t
                
                # Түс таңдау (Дәл осы жер түсті өзгертеді)
                for i, c in enumerate(COLORS):
                    if 10 + i * 45 < mx < 50 + i * 45 and 60 < my < 90:
                        current_color = c
            else: # Кенепті басу
                if current_tool == 'Fill':
                    flood_fill(canvas, (cx, cy), current_color)
                elif current_tool == 'Text':
                    is_typing, text_pos, text_content = True, (cx, cy), ""
                else:
                    start_pos, prev_pos = (cx, cy), (cx, cy)

        if event.type == MOUSEMOTION and start_pos:
            if current_tool == 'Pencil':
                pygame.draw.line(canvas, current_color, prev_pos, (cx, cy), brush_size)
                prev_pos = (cx, cy)
            elif current_tool == 'Eraser':
                pygame.draw.circle(canvas, WHITE, (cx, cy), brush_size * 5)

        if event.type == MOUSEBUTTONUP:
            if start_pos and current_tool not in ['Pencil', 'Eraser', 'Fill', 'Text']:
                draw_shape(canvas, current_tool, start_pos, (cx, cy), current_color, brush_size)
            start_pos = None

    # --- ЭКРАНҒА ШЫҒАРУ ---
    screen.fill(GRAY)
    screen.blit(canvas, (0, CANVAS_Y))

    # Панель (Toolbar)
    pygame.draw.rect(screen, (60, 60, 60), (0, 0, WIDTH, CANVAS_Y))
    
    # Батырмаларды салу
    for i, t in enumerate(tools):
        clr = (0, 120, 255) if current_tool == t else (130, 130, 130)
        pygame.draw.rect(screen, clr, (10 + i * 88, 10, 83, 35))
        screen.blit(font_ui.render(t, True, WHITE), (15 + i * 88, 18))

    # Түстерді салу
    for i, c in enumerate(COLORS):
        pygame.draw.rect(screen, c, (10 + i * 45, 60, 40, 30))
        if current_color == c:
            pygame.draw.rect(screen, WHITE, (10 + i * 45, 60, 40, 30), 2)

    # Ақпарат жолағы
    status = f"Size: {brush_size} | Tool: {current_tool} | Ctrl+S to Save"
    screen.blit(font_ui.render(status, True, WHITE), (450, 65))

    # Алдын ала көру (Preview)
    if start_pos and current_tool not in ['Pencil', 'Eraser', 'Fill', 'Text']:
        draw_shape(screen, current_tool, (start_pos[0], start_pos[1]+CANVAS_Y), (mx, my), current_color, brush_size)
    
    if is_typing:
        screen.blit(font_canvas.render(text_content + "|", True, current_color), (text_pos[0], text_pos[1]+CANVAS_Y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()