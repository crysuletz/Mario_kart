"""constantes du jeu"""

# fenêtre et vitesse du jeu
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# taille des cases et du circuit
TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# voiture
CAR_ACCELERATION = 0.05
CAR_WIDTH = 30
CAR_HEIGHT = 50

CAR_ORIENTATION = 3

"""
FROTTEMENT_BETON = 0.9
FROTTEMENT_HERBE = 1.5
FROTTEMENT_PLUIE = 0.5
FROTTEMENT_NEIGE = 0.2
"""


class GameState:
    """les états possibles du jeu"""
    MENU = "menu"
    CIRCUIT_SELECTION = "circuit_selection"
    RACING = "racing"
    VICTORY = "victory"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
