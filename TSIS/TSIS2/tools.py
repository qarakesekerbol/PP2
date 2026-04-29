import pygame
import math
from collections import deque

def flood_fill(surface, start_pos, fill_color):
    """BFS алгоритмі арқылы аймақты толтырып бояу"""
    target_color = surface.get_at(start_pos)
    if target_color == fill_color:
        return
    
    queue = deque([start_pos])
    width, height = surface.get_size()
    
    while queue:
        x, y = queue.popleft()
        if surface.get_at((x, y)) != target_color:
            continue
        
        surface.set_at((x, y), fill_color)
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color:
                    queue.append((nx, ny))

def draw_shape(surf, tool, start, end, color, size):
    """Барлық фигураларды сызуға арналған ортақ функция"""
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    
    if tool == 'Line':
        pygame.draw.line(surf, color, start, end, size)
    elif tool == 'Rect':
        pygame.draw.rect(surf, color, (x1, y1, dx, dy), size)
    elif tool == 'Circle':
        radius = int(math.hypot(dx, dy))
        pygame.draw.circle(surf, color, start, radius, size)
    elif tool == 'Square':
        side = max(abs(dx), abs(dy))
        s_x = x1 if dx > 0 else x1 - side
        s_y = y1 if dy > 0 else y1 - side
        pygame.draw.rect(surf, color, (s_x, s_y, side, side), size)
    elif tool == 'RightTri':
        pygame.draw.polygon(surf, color, [(x1, y1), (x1, y2), (x2, y2)], size)
    elif tool == 'EquiTri':
        side = dx
        h = int(side * math.sqrt(3) / 2)
        pygame.draw.polygon(surf, color, [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - h)], size)
    elif tool == 'Rhombus':
        pts = [(x1 + dx//2, y1), (x1 + dx, y1 + dy//2), (x1 + dx//2, y1 + dy), (x1, y1 + dy//2)]
        pygame.draw.polygon(surf, color, pts, size)