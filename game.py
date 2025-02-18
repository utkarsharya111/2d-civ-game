"""
game.py

Implements the main game objects:
 - Tile
 - Unit (Scholar, Worker)
 - GameState (manages map, units, econ model, etc.)
 - Rendering logic for the map and UI
 - Input handling
"""

import pygame
from map_data import TILE_MAP, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
import econ_model

# Tile types for reference
TILE_GRASS = 0
TILE_RESEARCH = 1
TILE_PRODUCTION = 2

# Colors
COLOR_GRASS = (160, 160, 160)      # Gray for grass
COLOR_RESEARCH = (100, 100, 255)   # Blue for research station
COLOR_PRODUCTION = (100, 255, 100) # Green for production site
COLOR_SELECTED = (255, 255, 0)     # Yellow highlight for selection

# A simple tile class (optional, but we can just store map as 2D array)
class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type

class Unit:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        # Could store stats here if you want

class GameState:
    def __init__(self):
        # Probability distribution
        self.prob_dist = econ_model.initialize_prob_dist()
        
        # Keep track of player's money/score
        self.money = 0.0
        
        # Create tile objects from map data
        self.tiles = [
            [Tile(TILE_MAP[row][col]) for col in range(MAP_WIDTH)]
            for row in range(MAP_HEIGHT)
        ]
        
        # Create two units: Scholar and Worker
        self.units = []
        # We'll place them at arbitrary positions
        self.units.append(Unit("Scholar", 0, 0))
        self.units.append(Unit("Worker", 1, 0))
        
        # Index of currently selected unit
        self.selected_unit_idx = 0
    
    def select_next_unit(self, direction=1):
        """
        Cycle through units with Tab / Shift+Tab
        direction=1 for next, -1 for previous
        """
        self.selected_unit_idx = (self.selected_unit_idx + direction) % len(self.units)
    
    def move_unit(self, dx, dy):
        """
        Moves the currently selected unit by (dx, dy) if in bounds
        """
        unit = self.units[self.selected_unit_idx]
        new_x = unit.x + dx
        new_y = unit.y + dy
        
        # Check map boundaries
        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            unit.x = new_x
            unit.y = new_y
    
    def research_action(self):
        """
        Called when player presses 'R' if Scholar is on a research tile
        """
        unit = self.units[self.selected_unit_idx]
        tile_type = self.tiles[unit.y][unit.x].tile_type
        
        if unit.name == "Scholar" and tile_type == TILE_RESEARCH:
            self.prob_dist = econ_model.research(self.prob_dist)
    
    def produce_action(self):
        """
        Called when player presses 'P' if Worker is on a production tile
        """
        unit = self.units[self.selected_unit_idx]
        tile_type = self.tiles[unit.y][unit.x].tile_type
        
        if unit.name == "Worker" and tile_type == TILE_PRODUCTION:
            # produce
            Y = econ_model.produce(self.prob_dist)
            self.money += Y

    def get_entropy(self):
        return econ_model.shannon_entropy(self.prob_dist)

    def get_knowledge(self):
        return econ_model.knowledge_stock(self.prob_dist)

    def get_tfp(self):
        return econ_model.tfp(self.prob_dist)

def draw_game(screen, game_state):
    """
    Renders the tile map, units, and UI on the screen.
    """
    # 1) Draw tile map
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            tile_type = game_state.tiles[row][col].tile_type
            
            if tile_type == TILE_GRASS:
                color = COLOR_GRASS
            elif tile_type == TILE_RESEARCH:
                color = COLOR_RESEARCH
            elif tile_type == TILE_PRODUCTION:
                color = COLOR_PRODUCTION
            
            rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

    # 2) Draw units
    for idx, unit in enumerate(game_state.units):
        # We'll represent them with text: 'S' for Scholar, 'W' for Worker
        if unit.name == "Scholar":
            text_str = "S"
            text_color = (255, 255, 255)  # white
        else:
            text_str = "W"
            text_color = (255, 255, 255)  # white
        
        # Is this the selected unit?
        if idx == game_state.selected_unit_idx:
            # draw a highlight box
            highlight_rect = pygame.Rect(unit.x*TILE_SIZE, unit.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLOR_SELECTED, highlight_rect, width=3)
        
        # Render the text in the center of the tile
        font = pygame.font.SysFont("Arial", 24)
        text_surf = font.render(text_str, True, text_color)
        # center it
        text_rect = text_surf.get_rect(center=(unit.x*TILE_SIZE + TILE_SIZE//2,
                                               unit.y*TILE_SIZE + TILE_SIZE//2))
        screen.blit(text_surf, text_rect)
    
    # 3) Draw UI panel with Entropy, Knowledge, TFP, money, p(ω) distribution, etc.
    # We'll place this on the right side of the screen
    panel_x = MAP_WIDTH * TILE_SIZE
    panel_width = 250
    panel_rect = pygame.Rect(panel_x, 0, panel_width, MAP_HEIGHT * TILE_SIZE)
    pygame.draw.rect(screen, (50, 50, 50), panel_rect)
    
    # Text Info
    font_small = pygame.font.SysFont("Arial", 18)
    lines = []
    lines.append(f"Entropy: {game_state.get_entropy():.3f}")
    lines.append(f"Knowledge: {game_state.get_knowledge():.3f}")
    lines.append(f"TFP: {game_state.get_tfp():.3f}")
    lines.append(f"Money: {game_state.money:.2f}")
    lines.append("")  # blank
    
    # Probability distribution lines
    lines.append("p(ω):")
    for i, pval in enumerate(game_state.prob_dist):
        lines.append(f" Method {i}: {pval:.3f}")
    
    # Render each line
    text_y = 20
    for line in lines:
        tsurf = font_small.render(line, True, (255, 255, 255))
        screen.blit(tsurf, (panel_x+10, text_y))
        text_y += 22
