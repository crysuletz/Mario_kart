import pygame
from constants import TILE_SIZE


class RoadTile:
    """Représente une case du circuit : route, herbe, terre, glace ou vide"""

    def __init__(self, col: int, row: int, terrain: str = "road", theme: str | None = None):
        """Enregistre la position, le terrain et le circuit de la case"""
        self.col = col
        self.row = row
        self.terrain = terrain
        self.theme = theme
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Dessine une case avec sa couleur et ses motifs selon le terrain"""
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        if self.theme is None: 
            surface.fill((80, 80, 90))
            pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)
            """Si aucun thème n'est indiqué, on garde des cases grises"""
        else:
            """Chaque circuit a ses propres couleurs: Campagne utilise surtout du vert, Canyon des couleurs orangées et Glace du blanc et du bleu"""
            couleurs = {
                "Campagne": {
                    "road": (67, 73, 78),
                    "grass": (114, 168, 96),
                    "dirt": (176, 128, 81),
                    "ice": (136, 208, 230),
                    "void": (35, 54, 68),
                },
                "Canyon": {
                    "road": (66, 69, 75),
                    "grass": (226, 164, 103),
                    "dirt": (174, 106, 66),
                    "ice": (136, 208, 230),
                    "void": (48, 47, 53),
                },
                "Glace": {
                    "road": (65, 77, 91),
                    "grass": (209, 230, 236),
                    "dirt": (160, 137, 122),
                    "ice": (122, 207, 231),
                    "void": (42, 110, 145),
                },
            }

            """Si le thème indiqué est inconnu, on utilise les couleurs de Campagne"""
            palette = couleurs.get(self.theme, couleurs["Campagne"])
            surface.fill(palette.get(self.terrain, palette["road"]))
        
            """Ajout de petits motifs selon le terrain choisi"""
            if self.terrain == "grass":
                """Grass représente l'herbe dans Campagne, le sable dans Canyon et la neige dans Glace"""
                if self.theme == "Campagne":
                    couleur = (90, 148, 75)
                elif self.theme == "Canyon":
                    couleur = (203, 139, 85)
                else:
                    couleur = (232, 243, 247)

                pygame.draw.rect(surface, couleur, (10, 16, 14, 4))
                pygame.draw.rect(surface, couleur, (39, 47, 12, 3))

            elif self.terrain == "dirt":
                """Dessine deux petites marques pour représenter la terre"""
                pygame.draw.rect(surface, (141, 98, 68), (9, 21, 18, 4))
                pygame.draw.rect(surface, (199, 151, 96), (36, 45, 14, 4))

            elif self.terrain == "ice":
                """Dessine des traits clairs pour representer la glace"""
                pygame.draw.line(surface, (218, 249, 251), (8, 13), (27, 28), 3)
                pygame.draw.line(surface, (78, 165, 201), (32, 47), (52, 34), 3)

            elif self.terrain == "void":
                """Dessine une marque sombre sur les cases de vide"""
                pygame.draw.rect(surface, (24, 75, 105), (13, 22, 31, 7))
        self.sprite = surface
        return self.sprite
