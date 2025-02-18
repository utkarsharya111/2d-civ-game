"""
main.py

Entry point for the 2D Civ-Style Info-Theoretic game.
Initialize pygame, create a GameState, run the main loop.
"""

import pygame
import sys
from game import GameState, draw_game

def main():
    pygame.init()
    
    # Calculate window size
    from map_data import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
    window_width = MAP_WIDTH * TILE_SIZE + 250  # + side panel
    window_height = MAP_HEIGHT * TILE_SIZE
    
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("2D Civ-Style Info-Econ Game")
    
    clock = pygame.time.Clock()
    
    # Create the game state
    game_state = GameState()
    
    running = True
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    # cycle unit
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        game_state.select_next_unit(direction=-1)
                    else:
                        game_state.select_next_unit(direction=1)
                
                # Movement
                elif event.key == pygame.K_UP:
                    game_state.move_unit(0, -1)
                elif event.key == pygame.K_DOWN:
                    game_state.move_unit(0, 1)
                elif event.key == pygame.K_LEFT:
                    game_state.move_unit(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game_state.move_unit(1, 0)
                
                # Research
                elif event.key == pygame.K_r:
                    game_state.research_action()
                
                # Produce
                elif event.key == pygame.K_p:
                    game_state.produce_action()
        
        # Draw everything
        draw_game(screen, game_state)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
