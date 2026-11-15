import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:
    """gère l'affichage du jeu: le menu, le choix du circuit et la course"""

    def __init__(self, screen: pygame.Surface):
        """garde l'écran et choisit la police pour écrire le texte"""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        """efface l'écran puis dessine le menu ou la course selon l'état du jeu"""
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.CIRCUIT_SELECTION:
            self._draw_selection(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()
    
    def _draw_selection(self, model: GameModel) -> None:
        """dessine la liste des circuits avec celui qui est choisi en jaune"""
        cx = WINDOW_WIDTH // 2

        # titre en haut de l'écran
        title = self.font.render("Choisir un circuit", True, COLOR_ACCENT)
        self.screen.blit(title, title.get_rect(center=(cx, 160)))

        # un bouton par circuit
        for i in range(len(model.circuit_names)):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            # le circuit choisi en jaune, les autres en blanc
            if i == model.selected_circuit:
                color = COLOR_ACCENT
            else:
                color = COLOR_TEXT

            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)
            text = self.font.render(model.circuit_names[i], True, color)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_menu(self, model: GameModel) -> None:
        """dessine le menu avec le titre et les boutons jouer et quitter"""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """dessine les cases du circuit puis la voiture"""

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return
        surf, rect = model.car.get_rotated_sprite1()
        surf2, rect2 = model.car2.get_rotated_sprite2()
        self.screen.blit(surf, rect)
        self.screen.blit(surf2, rect2)
