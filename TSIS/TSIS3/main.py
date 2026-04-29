import pygame
import sys
from persistence import load_settings, save_settings, save_score
from ui import (main_menu, settings_screen, leaderboard_screen,
                game_over_screen, username_screen)
from racer import run_game

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Racer - KBTU Edition')
    clock  = pygame.time.Clock()

    settings    = load_settings()
    player_name = None

    while True:
        choice = main_menu(screen, clock)

        if choice == 'quit':
            break

        elif choice == 'leaderboard':
            leaderboard_screen(screen, clock)

        elif choice == 'settings':
            settings_screen(screen, clock, settings)

        elif choice == 'play':
            # Ask for name if not set yet
            if player_name is None:
                name = username_screen(screen, clock)
                if name is None:      # window closed
                    break
                player_name = name

            # Game / retry loop
            while True:
                score, distance, coins = run_game(screen, clock, settings, player_name)
                save_score(player_name, score, distance, coins)

                result = game_over_screen(screen, clock, score, distance, coins)
                if result == 'retry':
                    continue
                else:
                    player_name = None   # reset so next play asks again
                    break

    save_settings(settings)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()