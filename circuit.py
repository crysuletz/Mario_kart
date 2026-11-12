from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    """Représente un circuit composé de plusieurs cases organisées en lignes et en colonnes"""
    def __init__(self,  grid: list[list[RoadTile]]):
        """Prépare le circuit en enregistrant ses cases et son nombre de lignes et de colonnes"""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

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
