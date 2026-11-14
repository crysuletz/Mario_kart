from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):

        """ Définit l'état initial du jeu comme étant le menu principal,
        et permet de savoir quel est le circuit et la voiture choisit """
        
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        
        """ Met à jour le circuit et fais apparaître la voiture """
        
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        
        """ Initialisation de la position de la voiture au début de la course"""
        
        self.car = Car(7, 1)

    def update(self) -> None:

        """ Mis à jour de la position de la voiture pendant la course """

        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
