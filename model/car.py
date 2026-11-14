import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_ORIENTATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Definition des comportements de la voiture"""

    def __init__(self, start_col: int, start_row: int):

        """Construction des caractéristiques qui definissent 
        la voiture à un temps donné t"""

        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        
        """Définition de l'accélération de la voiture"""

        self.speed += CAR_ACCELERATION #*math.exp(-frottement)

    def freinage(self) -> None :

        """Définition de la décéleration de la voiture"""
    
        self.speed -= CAR_ACCELERATION #*math.exp(-frottement)

    def tourner_gauche(self) -> None:

        """ Permet de mettre à jour l'orientation de la voiture à gauche"""

        self.angle -= CAR_ORIENTATION

    def tourner_droite(self) -> None:
    
        """ Permet de mettre à jour l'orientation de la voiture à droite"""
            
        self.angle += CAR_ORIENTATION

    def update_position(self) -> None:

        """Definition de la position de la voiture en y"""

        angle_rad = math.radians(self.angle)

        self.x += self.speed * math.sin(angle_rad)
        self.y += self.speed * math.cos(angle_rad)

    def build_sprite(self) -> pygame.Surface:

        """Construit les éléments qui apparaissent à l'écran, 
        lorsque la voiture se déplace"""

        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 255, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5, border_top_left_radius=20, border_top_right_radius = 20)

        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:

        """Affiche correctement la voiture lorsqu'elle tourne à gauche ou à droite."""
        
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect



