import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
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

        self.speed += CAR_ACCELERATION

    def update_position(self) -> None:

        """Definition de la position de la voiture en y"""

        self.y += self.speed

    def build_sprite(self) -> pygame.Surface:

        """Construit les éléments qui apparaissent à l'écran, 
        lorsque la voiture se déplace"""

        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    def freinage(self) -> None :
        self.speed -= CAR_ACCELERATION
        
    def marche_arriere(self) -> None :
        self.y -= self.speed


