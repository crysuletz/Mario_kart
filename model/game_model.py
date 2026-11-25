from constants import GameState, TILE_SIZE
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
        """charge le circuit choisi parmi Campagne, Canyon et Glace et fait apparaître les voitures"""
        nom = self.circuit_names[self.selected_circuit]
        self.circuit = Circuit.creer(nom)
        # le nombre de checkpoints et de tours vient du circuit choisi
        self.race = RaceManager(len(self.circuit.checkpoint_bands), self.circuit.nombre_tours)
        # bande où était chaque voiture à l'image d'avant
        self.previous_band = {1: None, 2: None}
        self.spawn_car()

    def spawn_car(self) -> None:
        
        """ Initialisation de la position des voitures au début de la course"""
        
        self.car = Car(4, 10)
        self.car2 = Car(3, 10)

    def good_side(self, tile_pos: tuple[int, int], band: list, direction: str) -> bool:
        """vrai si la case est du bon côté de la bande, dans le sens du circuit"""
        col, row = tile_pos
        # une bande est sur une seule colonne (verticale) ou une seule ligne (horizontale)
        band_col, band_row = band[0]
        if direction == "right":
            return col > band_col
        if direction == "left":
            return col < band_col
        if direction == "up":
            return row < band_row
        return row > band_row

    def check_car(self, player: int, car: Car) -> None:
        """compte un checkpoint ou l'arrivée quand la voiture sort de la bande dans le sens du circuit"""
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)
        # la voiture est sortie de l'écran
        if tile is None:
            return
        tile_pos = (tile.col, tile.row)

        # sur quelle bande est la voiture maintenant : numéro du checkpoint, "finish" ou None
        band = None
        for i in range(len(self.circuit.checkpoint_bands)):
            if tile_pos in self.circuit.checkpoint_bands[i]:
                band = i + 1
        if tile_pos in self.circuit.finish_band:
            band = "finish"

        # bande où était la voiture à l'image d'avant
        old_band = self.previous_band[player]

        # la voiture vient de sortir de la ligne d'arrivée
        if old_band == "finish" and band != "finish":
            if self.good_side(tile_pos, self.circuit.finish_band, self.circuit.finish_direction):
                self.race.pass_finish_line(player)

        # la voiture vient de sortir d'un checkpoint
        elif old_band is not None and old_band != band:
            checkpoint_band = self.circuit.checkpoint_bands[old_band - 1]
            direction = self.circuit.checkpoint_directions[old_band - 1]
            if self.good_side(tile_pos, checkpoint_band, direction):
                self.race.pass_checkpoint(player, old_band)

        self.previous_band[player] = band

    def check_blocks(self) -> None:
        """regarde les checkpoints et l'arrivée pour les deux voitures"""
        self.check_car(1, self.car)
        self.check_car(2, self.car2)

    def update(self) -> None:

        """ Mis à jour de la position des voitures pendant la course """

        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
        self.car2.update_position()
        # on regarde si les voitures passent sur des checkpoints ou sur l'arrivée
        self.check_blocks()
        # si un joueur a gagne on passe à l'écran de victoire
        if self.race.winner is not None:
            self.state = GameState.VICTORY
