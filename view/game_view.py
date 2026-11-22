import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:
    """gère l'affichage du jeu : le menu, le choix du circuit, la course et la victoire"""

    def __init__(self, screen: pygame.Surface):
        """garde l'écran et choisit la police pour écrire le texte"""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        """efface l'écran puis le redessine selon l'état du jeu"""
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.CIRCUIT_SELECTION:
            self._draw_selection(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        elif model.state == GameState.VICTORY:
            self._draw_victory(model)
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
    
    def _draw_victory(self, model: GameModel) -> None:
        """affiche le joueur qui a gagné"""
        cx = WINDOW_WIDTH // 2
        text = self.font.render("Joueur " + str(model.race.winner) + " a gagné !", True, COLOR_ACCENT)
        self.screen.blit(text, text.get_rect(center=(cx, 300)))
        # aide en dessous pour le joueur
        aide = self.font.render("Entrée ou Échap : retour au menu", True, COLOR_TEXT)
        self.screen.blit(aide, aide.get_rect(center=(cx, 450)))
    
    def _draw_laps(self, model: GameModel) -> None:
        """affiche les tours et checkpoints du joueur 1 à gauche et du joueur 2 à droite"""
        race = model.race
        # bande noire en haut pour bien voir le texte
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, WINDOW_WIDTH, 40))

        # joueur 1 en rose à gauche
        tours1 = str(race.laps[1]) + "/" + str(race.total_laps)
        cp1 = str(len(race.passed_checkpoints[1])) + "/" + str(race.total_checkpoints)
        texte1 = "Joueur 1 : tour " + tours1 + "   checkpoints " + cp1
        ligne1 = self.font.render(texte1, True, (255, 105, 180))
        # on part du bord gauche
        self.screen.blit(ligne1, (10, 8))

        # joueur 2 en bleu à droite
        tours2 = str(race.laps[2]) + "/" + str(race.total_laps)
        cp2 = str(len(race.passed_checkpoints[2])) + "/" + str(race.total_checkpoints)
        texte2 = "Joueur 2 : tour " + tours2 + "   checkpoints " + cp2
        ligne2 = self.font.render(texte2, True, (100, 150, 255))
        # on enlève la largeur du texte pour qu'il finisse au bord droit
        self.screen.blit(ligne2, (WINDOW_WIDTH - ligne2.get_width() - 10, 8))

    def _draw_menu(self, model: GameModel) -> None:
        """dessine le menu avec le titre et les boutons jouer et quitter"""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Entrée)", GameState.RACING),
                   ("QUITTER (Échap)", None)]
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
        self.screen.blit(surf, rect)
        self.screen.blit(surf2, rect2)
        self._draw_laps(model)
