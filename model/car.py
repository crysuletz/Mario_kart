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
        self.sprite1 = self.build_sprite1()
        self.sprite2 = self.build_sprite2()

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
        self.y -= self.speed * math.cos(angle_rad)

    def build_sprite1(self) -> pygame.Surface:

        """Construit les éléments qui apparaissent à l'écran, 
        lorsque la voiture du joueur 1 se déplace"""

        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 105, 180), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5, border_top_left_radius=15, border_top_right_radius = 15)
        pygame.draw.rect(surf, (205, 55, 125), (0, 0, CAR_WIDTH,
                                         CAR_HEIGHT/3), border_radius=5, border_top_left_radius=5, border_top_right_radius = 5, 
                                         border_bottom_left_radius=5, border_bottom_right_radius = 5)
        pygame.draw.rect(surf, (0, 0, 0), (-2, 5, CAR_WIDTH/7,CAR_HEIGHT/4) )
        pygame.draw.rect(surf, (0, 0, 0), (-2, 35, CAR_WIDTH/7,CAR_HEIGHT/4) )
        pygame.draw.rect(surf, (0, 0, 0), (28, 5, CAR_WIDTH/5,CAR_HEIGHT/4) )
        pygame.draw.rect(surf, (0, 0, 0), (28, 35, CAR_WIDTH/5,CAR_HEIGHT/4) )
        
        return surf
        
    def build_sprite2(self) -> pygame.Surface:
    
        """Construit les éléments qui apparaissent à l'écran, 
        lorsque la voiture du joueur 2 se déplace"""
    
        surf2 = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf2, (0, 0, 255), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5, border_top_left_radius=5, border_top_right_radius = 5)
        pygame.draw.rect(surf2, (0, 0, 205), (0, 0, CAR_WIDTH,
                                 CAR_HEIGHT/3), border_radius=5, border_top_left_radius=5, border_top_right_radius = 5, 
                                 border_bottom_left_radius=5, border_bottom_right_radius = 5)

        pygame.draw.rect(surf2, (0, 0, 0), (-2, 5, CAR_WIDTH/7,CAR_HEIGHT/4) )
        pygame.draw.rect(surf2, (0, 0, 0), (-2, 35, CAR_WIDTH/7,CAR_HEIGHT/4) )
        pygame.draw.rect(surf2, (0, 0, 0), (28, 5, CAR_WIDTH/5,CAR_HEIGHT/4))
        pygame.draw.rect(surf2, (0, 0, 0), (28, 35, CAR_WIDTH/5,CAR_HEIGHT/4))
    
            
        return surf2

    
    def get_rotated_sprite1(self) -> tuple[pygame.Surface, pygame.Rect]:

        """Affiche correctement la voiture du joueur 1 lorsqu'elle tourne
        à gauche ou à droite."""
        
        rotated = pygame.transform.rotate(self.sprite1, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    def get_rotated_sprite2(self) -> tuple[pygame.Surface, pygame.Rect]:
        
        """Affiche correctement la voiture du joueur 2 lorsqu'elle tourne
        à gauche ou à droite."""
        
        rotated2 = pygame.transform.rotate(self.sprite2, -self.angle)
        rect2 = rotated2.get_rect(center=(int(self.x), int(self.y)))
        return rotated2, rect2

