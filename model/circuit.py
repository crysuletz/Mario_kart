from model.road_tile import RoadTile
from constants import TILE_SIZE

# chaque lettre correspond à un type de terrain dans la grille
TERRAINS = {
    "R": "road",
    "G": "grass",
    "D": "dirt",
    "I": "ice",
    "V": "void",
}


# grilles des trois circuits, chaque lettre représente une case
CARTES = {
    "Campagne": (
        "GGGGGGGGGGGGGGGG",
        "GGGRRRRRRRRRRGGG",
        "GGRRRRRRRRRRRRGG",
        "GRRRGGGGGGGGRRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRRGGGGGGGGRRRG",
        "GGRRRRRRRRRRRRGG",
        "GGGRRRRRRRRRRGGG",
        "GGGGGGGGGGGGGGGG",
    ),

    "Canyon": (
        "GGGGGGGGGGGGGGGG",
        "GRRRRRRGGGRRRRRG",
        "GRRRRRRGGGRRRRRG",
        "GRRGGRRRDDRRGRRG",
        "GRRGGRRRDDRRGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRRRRRRRRRRRRRG",
        "GRRRRRRRRRRRRRRG",
        "GGGGGGGGGGGGGGGG",
    ),

    "Glace": (
        "GGGGGGGGGGGGGGGG",
        "GGGGGRRRRIIRRRRG",
        "GGGGGRRRRIIRRRRG",
        "GGGGGRRGGGGGGRRG",
        "GGGGGRRGGRRIIRRG",
        "GRRDDRRGGRRIIRRG",
        "GRRDDRRGGRRGGGGG",
        "GRRGGGGVVRRIIRRG",
        "GRRGGGGVVRRIIRRG",
        "GRRGGGGGGGGGGRRG",
        "GRRRRRRRRRRRRRRG",
        "GRRRRRRRRRRRRRRG",
    ),
}

# positions des quatre checkpoints de chaque circuit
CHECKPOINTS = {
    "Campagne": [(10, 10), (13, 6), (7, 1), (1, 6)],
    "Canyon": [(10, 10), (13, 6), (3, 1), (1, 6)],
    "Glace": [(10, 10), (13, 9), (9, 1), (1, 8)],
}

# positions des boosts sur chaque circuit
BOOSTS = {
    "Campagne": [(9, 1), (5, 10)],
    "Canyon": [(12, 9), (7, 4)],
    "Glace": [(12, 10), (10, 5)],
}

# les cases de chaque checkpoint dans l'ordre du circuit
CHECKPOINT_BANDS = {
    "Campagne": [[(10, 9), (10, 10)], [(13, 6), (14, 6)], [(7, 1), (7, 2)], [(1, 6), (2, 6)]],
    "Canyon": [[(10, 9), (10, 10)], [(13, 6), (14, 6)], [(3, 1), (3, 2)], [(1, 6), (2, 6)]],
    "Glace": [[(10, 10), (10, 11)], [(13, 9), (14, 9)], [(9, 1), (9, 2)], [(1, 8), (2, 8)]],
}

# les cases de la ligne d'arrivée
FINISH_BANDS = {
    "Campagne": [(8, 9), (8, 10)],
    "Canyon": [(8, 9), (8, 10)],
    "Glace": [(8, 10), (8, 11)],
}

# sens dans lequel on doit traverser chaque checkpoint
CHECKPOINT_DIRECTIONS = ["right", "up", "left", "down"]

# sens dans lequel on doit traverser la ligne d'arrivée
FINISH_DIRECTION = "right"


class Circuit:
    """Représente un circuit composé de plusieurs cases organisées en lignes et en colonnes"""

    def __init__(self, grid: list[list[RoadTile]], nom: str | None = None):
        """Enregistre la grille, le nom et les informations du circuit"""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

        # nom du circuit et positions de ses checkpoints et boosts
        self.nom = nom
        self.checkpoints = CHECKPOINTS.get(nom, [])
        self.boosts = BOOSTS.get(nom, [])
        self.checkpoint_bands = CHECKPOINT_BANDS.get(nom, [])
        self.finish_band = FINISH_BANDS.get(nom, [])
        self.checkpoint_directions = CHECKPOINT_DIRECTIONS
        self.finish_direction = FINISH_DIRECTION

        # position du départ, de l'arrivée et nombre de tours
        self.depart = (4, 10)
        self.arrivee = (8, 10)
        self.nombre_tours = 3

    @classmethod
    def creer(cls, nom: str):
        """Crée le circuit choisi à partir de sa grille: chaque lettre est transformée en une case avec son terrain et ses couleurs"""
        lignes = CARTES[nom]
        grille = []
        for ligne_idx, ligne in enumerate(lignes):
            rangee = []
            for colonne_idx, caractere in enumerate(ligne):
                terrain = TERRAINS[caractere]
                case = RoadTile(colonne_idx, ligne_idx, terrain, nom)
                rangee.append(case)
            grille.append(rangee)
        return cls(grille, nom)

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """Renvoie la case située à la ligne et à la colonne indiquées, ou None si elle n'existe pas"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Retrouve la case du circuit à partir d'une position en pixels (coordonnées à l'écran)"""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """Calcule la largeur totale du circuit en pixels à partir du nombre de colonnes"""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Calcule la hauteur totale du circuit en pixels à partir du nombre de lignes"""
        return self.rows * TILE_SIZE