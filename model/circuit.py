from model.road_tile import RoadTile
from constants import TILE_SIZE

"""Chaque lettre correspond à un type de terrain dans la grille"""
TERRAINS = {
    "R": "road",
    "G": "grass",
    "D": "dirt",
    "I": "ice",
    "V": "void",
}


"""Grilles des trois circuits, chaque lettre représente une case"""
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


"""Positions des quatre checkpoints de chaque circuit"""
CHECKPOINTS = {
    "Campagne": [(10, 10), (13, 6), (7, 1), (1, 6)],
    "Canyon": [(10, 10), (13, 6), (3, 1), (1, 6)],
    "Glace": [(10, 10), (13, 9), (9, 1), (1, 8)],
}

"""Positions des boosts sur chaque circuit"""
BOOSTS = {
    "Campagne": [(9, 1), (5, 10)],
    "Canyon": [(12, 9), (7, 4)],
    "Glace": [(12, 10), (10, 5)],
}

class Circuit:
    """Représente un circuit composé de plusieurs cases organisées en lignes et en colonnes"""

    def __init__(self,  grid: list[list[RoadTile]], nom: str | None = None):
        """Enregistre la grille, le nom et les informations du circuit"""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
        """Nom du circuit et positions de ses checkpoints et boosts"""
        self.nom = nom
        self.checkpoints = CHECKPOINTS.get(nom, [])
        self.boosts = BOOSTS.get(nom, [])

        """Position du départ, de l'arrivée et nombre de tours"""
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

