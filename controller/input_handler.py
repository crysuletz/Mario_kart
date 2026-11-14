import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:     "brake",
    pygame.K_LEFT:     "turn_left",
    pygame.K_RIGHT:     "turn_right",
}


class InputHandler:
    """Gère les touches du clavier et les transforme en commandes pour la voiture"""
    def __init__(self):
        """Prépare le dictionnaire qui associe les touches du clavier aux actions"""
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        """Vérifie les touches maintenues et renvoie les actions correspondantes"""
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
