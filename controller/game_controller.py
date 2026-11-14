import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Gère le jeu et fait le lien entre le modèle (données du jeu), la vue (lffichage) et les touches du clavier"""
    def __init__(self):
        """Prépare la fenêtre Pygame, le modèle, la vue et la gestion des touches du clavier"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """Fait tourner le jeu en vérifiant les touches, en mettant à jour les voitures et en affichant le jeu à chaque image"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Gère les événements (actions du joueur), comme appuyer sur une touche ou fermer la fenêtre"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Vérifie l'état du jeu (menu, choix du circuit ou course) pour savoir quoi faire avec la touche appuyée"""
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECTION:
            self.handle_selection_key(key)
        elif state == GameState.RACING:
            if key == pygame.K_ESCAPE:
                self.model.state = GameState.MENU

    def handle_menu_key(self, key: int) -> None:
        """Permet d'aller au choix des circuits avec Entrée ou de quitter le jeu avec Échap"""
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECTION
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_selection_key(self, key: int) -> None:
        """Permet de choisir un circuit avec les flèches, de lancer la course avec Entrée ou de revenir au menu avec Échap"""
        if key == pygame.K_UP:
            self.model.change_circuit(-1)
        elif key == pygame.K_DOWN:
            self.model.change_circuit(1)
        elif key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU
            
    def update(self) -> None:
        """Récupère les commandes du joueur (accélérer, freiner, tourner) et met à jour le jeu pendant la course"""
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car
        self.apply_input(car, p1_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """Applique les commandes du joueur à la voiture (accélération, freinage et direction) selon les touches maintenues"""
        if player_input['accelerate']:
            car.accelerate()
        elif player_input['brake']:
            car.brake_or_reverse()
            
        if player_input['turn_left']:
            car.turn_left()
        elif player_input['turn_right']:
            car.turn_right()

    def render(self) -> None:
        """Demande à la vue (partie qui gère l'affichage) de dessiner le jeu à l'écran"""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Arrête la boucle du jeu, ferme Pygame et quitte le programme"""
        self.running = False
        pygame.quit()
        sys.exit()
