import pygame
import random
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

        self._draw_decorations(model.circuit)
        
        """Dessine les 4 checkpoints"""
        for numero, (col, row) in enumerate(model.circuit.checkpoints, start=1):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            """Les checkpoints 1 et 3 sont verticaux"""
            vertical = numero == 1 or numero == 3
            if vertical:
                """Cherche les deux cases à traverser en hauteur"""
                case_bas = model.circuit.get_tile(col, row + 1)
                if case_bas and case_bas.terrain in ("road", "dirt", "ice"):
                    debut = row
                else:
                    debut = row - 1
                zone = pygame.Rect(x + 16, debut * TILE_SIZE, 32, TILE_SIZE * 2)
            else:
                """Les checkpoints 2 et 4 sont horizontaux"""
                case_droite = model.circuit.get_tile(col + 1, row)
                if case_droite and case_droite.terrain in ("road", "dirt", "ice"):
                    debut = col
                else:
                    debut = col - 1
                zone = pygame.Rect(debut * TILE_SIZE, y + 16, TILE_SIZE * 2, 32)
            
            """Dessine une bande bleue avec une bordure foncée"""
            pygame.draw.rect(self.screen, (85, 186, 219), zone)
            pygame.draw.rect(self.screen, (26, 84, 110), zone, 2)

            """Écrit le numéro du checkpoint au milieu de la bande"""
            police_checkpoint = pygame.font.SysFont("Arial", 15, bold=True)
            texte = police_checkpoint.render("CHECKPOINT " + str(numero), True, (15, 52, 74))
            """Tourne le texte pour les bandes verticales"""
            if vertical:
                if numero == 1:
                    texte = pygame.transform.rotate(texte, -90)
                else:
                    texte = pygame.transform.rotate(texte, 90)
            """Place le texte au centre de la bande"""
            self.screen.blit(texte, texte.get_rect(center=zone.center))
            
        """Dessine 2 boosts jaunes"""
        for col, row in model.circuit.boosts:
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            """Dessine un carré jaune sur la route"""
            pygame.draw.rect(self.screen, (245, 197, 50), (x + 13, y + 13, 38, 38))
            """Ajoute la lettre B au centre du boost"""
            texte = self.font.render("B", True, (60, 42, 15))
            self.screen.blit(texte, texte.get_rect(center=(x + 32, y + 32)))
            
        """Dessine la ligne d'arrivée en damier noir et blanc"""
        col, row = model.circuit.arrivee
        """Cherche les deux cases de route à traverser"""
        case_bas = model.circuit.get_tile(col, row + 1)
        if case_bas and case_bas.terrain in ("road", "dirt", "ice"):
            debut = row
        else:
            debut = row - 1
        """Position de la ligne d'arrivée"""
        x = col * TILE_SIZE + 20
        y = debut * TILE_SIZE
        """Dessine les petits carrés noirs et blancs"""
        for ligne in range(16):
            for colonne in range(4):
                if (ligne + colonne) % 2 == 0:
                    couleur = (245, 245, 245)
                else:
                    couleur = (30, 30, 35)
                pygame.draw.rect(self.screen, couleur, (x + colonne * 6, y + ligne * 8, 6, 8))

        surf, rect = model.car.get_rotated_sprite1()
        surf2, rect2 = model.car2.get_rotated_sprite2()
        self.screen.blit(surf, rect)
        self.screen.blit(surf2, rect2)
        self.screen.blit(surf, rect)
        self.screen.blit(surf2, rect2)
        self._draw_laps(model)

    def _draw_decorations(self, circuit) -> None:
        """Dessine les décorations du circuit choisi"""
        if circuit.nom == "Campagne":

            """Dessine une grange rouge"""
            """Murs de la grange"""
            pygame.draw.rect(self.screen, (170, 60, 48), (330, 355, 112, 88))
            """Toit"""
            pygame.draw.polygon(self.screen, (115, 40, 38),[(318, 355), (386, 315), (454, 355)])
            """Porte"""
            pygame.draw.rect(self.screen, (95, 60, 45),(372, 397, 28, 46))
            """Deux fenêtres"""
            pygame.draw.rect(self.screen, (235, 205, 125), (345, 370, 18, 18))
            pygame.draw.rect(self.screen, (235, 205, 125), (410, 370, 18, 18))
          
            """Dessine un étang"""
            pygame.draw.ellipse(self.screen, (65, 130, 85),(531, 452, 151, 93))
            pygame.draw.ellipse(self.screen, (91, 170, 210),(539, 460, 135, 77))
            """Ajoute un reflet sur l'eau"""
            pygame.draw.ellipse(self.screen, (170, 220, 235),(558, 476, 50, 10))

            """Ajoute des fleurs dans l'herbe"""
            fleurs = [(286, 270), (314, 474), (355, 535), (463, 310), (485, 458), (508, 389), (691, 305), (716, 466), (720, 542), (582, 559)]

            for x, y in fleurs:
                """Dessine la tige verte et le centre jaune de chaque fleur"""
                pygame.draw.line(self.screen, (50, 120, 55), (x, y + 2), (x, y + 9), 2)
                pygame.draw.circle(self.screen, (250, 225, 110), (x, y), 4)
            
            """Place des arbres sur l'herbe"""
            hasard = random.Random(5)
            for row_idx, row in enumerate(circuit.grid):
                for col_idx, tile in enumerate(row):
                    if tile.terrain != "grass":
                        continue
                    if hasard.randrange(11) != 0:
                        continue
                    x = col_idx * TILE_SIZE + hasard.randint(-8, 8)
                    y = row_idx * TILE_SIZE + hasard.randint(-8, 8)

                    """Évite de placer des arbres sur la grange"""
                    if 300 < x + 32 < 470 and 290 < y + 32 < 465:
                        continue
                    """Évite de placer des arbres sur l'étang"""
                    if 505 < x + 32 < 710 and 425 < y + 32 < 560:
                        continue
                    """Dessine le tronc marron et les feuilles vertes"""
                    pygame.draw.rect(self.screen, (118, 78, 45), (x + 27, y + 33, 10, 17))
                    pygame.draw.circle(self.screen, (47, 119, 59), (x + 32, y + 28), 17)

        elif circuit.nom == "Canyon":
            
            """Dessine des cactus sur le sable de Canyon"""
            for row_idx, row in enumerate(circuit.grid):
                for col_idx, tile in enumerate(row):
                    if tile.terrain != "grass":
                        continue
                    if (col_idx * 5 + row_idx * 7) % 17 != 0:
                        continue
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    
                    """Dessine le tronc et les deux bras du cactus"""
                    pygame.draw.rect(self.screen, (53, 120, 76), (x + 28, y + 15, 10, 38))
                    pygame.draw.rect(self.screen, (53, 120, 76), (x + 18, y + 29, 13, 9))
                    pygame.draw.rect(self.screen, (53, 120, 76), (x + 42, y + 23, 8, 15))

            """Dessine une petite tour de guet en bois au milieu de Canyon"""
            """Les deux pieds de la tour"""
            pygame.draw.rect(self.screen, (125, 77, 48), (393, 390, 10, 65))
            pygame.draw.rect(self.screen, (125, 77, 48), (433, 390, 10, 65))
            """Cabane en haut de la tour"""
            pygame.draw.rect(self.screen, (172, 105, 65), (385, 372, 66, 25))
            """Toit"""
            pygame.draw.polygon(self.screen, (115, 65, 45), [(380, 372), (418, 349), (456, 372)])
            """Supports en bois"""
            pygame.draw.line(self.screen, (90, 55, 38), (403, 416), (433, 441), 4)
            pygame.draw.line(self.screen, (90, 55, 38), (433, 416), (403, 441), 4)
            """Petite fenêtre"""
            pygame.draw.rect(self.screen, (65, 48, 37), (409, 378, 17, 12))

            """Dessine quelques rochers dans le sable"""
            rochers = [(280, 420, 18), (540, 475, 22), (635, 510, 16)]
            for x, y, taille in rochers:
                """Dessine chaque rocher avec une forme irrégulière"""
                pygame.draw.polygon(self.screen, (154, 97, 65), [(x, y + taille), (x + 5, y), (x + taille, y - 4), (x + taille + 8, y + taille)])
                """Ajoute un trait plus clair sur le rocher"""
                pygame.draw.line( self.screen, (205, 142, 91), (x + 5, y + 3), (x + taille, y), 3)

        elif circuit.nom == "Glace":
            
            """Dessine un petit chalet enneigé sur le circuit Glace"""
            """Murs"""
            pygame.draw.rect(self.screen, (145, 105, 80), (110, 228, 82, 62))
            """Toit"""
            pygame.draw.polygon(self.screen, (95, 65, 55), [(101, 228), (151, 197), (201, 228)])
            """Neige sur le toit"""
            pygame.draw.line(self.screen, (240, 247, 250), (101, 228), (151, 197), 5)
            pygame.draw.line(self.screen, (240, 247, 250), (151, 197), (201, 228), 5)
            """Porte"""
            pygame.draw.rect(self.screen, (82, 58, 48), (140, 255, 20, 35))
            """Fenêtre"""
            pygame.draw.rect(self.screen, (245, 211, 125), (118, 240, 15, 15))

            """Dessine le lac gelé avec une forme irrégulière"""
            pygame.draw.polygon(self.screen, (49, 117, 151),
                [
                    (463, 455), (495, 449),
                    (539, 455), (568, 477),
                    (573, 514), (558, 551),
                    (524, 567), (481, 562),
                    (454, 540), (449, 497)
                ]
            )

            """Ajoute une surface plus clair au milieu du lac"""
            pygame.draw.polygon(self.screen, (117, 193, 219),
                [
                    (474, 468), (498, 460),
                    (534, 468), (556, 486),
                    (560, 515), (545, 542),
                    (521, 553), (486, 547),
                    (466, 529), (462, 499)
                ]
            )
            
            """Ajoute quelques sapins"""
            sapins = [(300, 250), (245, 390), (350, 500), (610, 390), (650, 575),]
            for x, y in sapins:
                """Tronc du sapin"""
                pygame.draw.rect(self.screen, (99, 87, 77), (x + 13, y + 34, 6, 12))
                """Feuillage du sapin"""
                pygame.draw.polygon(self.screen, (45, 105, 112), [(x + 16, y), (x, y + 34), (x + 32, y + 34)])
                """Ajoute un petit trait clair pour la neige"""
                pygame.draw.line(self.screen, (228, 242, 245), (x + 9, y + 20), (x + 16, y + 6), 3)

            
