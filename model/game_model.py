from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.race_manager import RaceManager


class GameModel:

    def __init__(self):

        """ Définit l'état initial du jeu comme étant le menu principal,
        et permet de savoir quel est le circuit et la voiture choisit """
        
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.car2: Car | None = None
        self.race: RaceManager | None = None
        # noms des circuits et numéro du circuit choisi
        self.circuit_names = ["Campagne", "Canyon", "Glace"]
        self.selected_circuit = 0
            
    def change_circuit(self, direction: int) -> None:
        """passe au circuit suivant ou précédent"""
        self.selected_circuit = self.selected_circuit + direction
        # si on dépasse le dernier circuit, on revient au premier
        if self.selected_circuit >= len(self.circuit_names):
            self.selected_circuit = 0
        # si on passe avant le premier, on va au dernier
        if self.selected_circuit < 0:
            self.selected_circuit = len(self.circuit_names) - 1

    def load_circuit(self) -> None:
        
        """ Met à jour le circuit et fais apparaître les voitures """
        """Charge le circuit choisi parmi Campagne, Canyon et Glace"""
        nom = self.circuit_names[self.selected_circuit]
        self.circuit = Circuit.creer(nom)
        
        # 4 checkpoints et 3 tours pour l'instant va falloir adapter apres pour chaque circuit
        self.race = RaceManager(4, 3)
        self.spawn_car()

    def spawn_car(self) -> None:
        
        """ Initialisation de la position des voitures au début de la course"""
        
        self.car = Car(4, 10)
        self.car2 = Car(3, 10)

    def update(self) -> None:

        """ Mis à jour de la position des voitures pendant la course """

        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
        self.car2.update_position()
        # si un joueur a gagne on passe à l'écran de victoire
        if self.race.winner is not None:
            self.state = GameState.VICTORY
