import pygame


MAPPING_PLAYER1 = {
    pygame.K_z:     "accelerate",
    pygame.K_w:     "accelerate",
    pygame.K_s:     "freinage",
    pygame.K_q:     "tourner_gauche",
    pygame.K_a:     "tourner_gauche",
    pygame.K_d:     "tourner_droite",
}


MAPPING_PLAYER2 = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:     "freinage",
    pygame.K_LEFT:     "tourner_gauche",
    pygame.K_RIGHT:     "tourner_droite",
}



class InputHandler:
    """Gère les touches du clavier et les transforme en commandes pour la voiture"""
    def __init__(self):
        """Prépare le dictionnaire qui associe les touches du clavier aux actions"""
        self.mapping1 = MAPPING_PLAYER1
        self.mapping2 = MAPPING_PLAYER1

    def get_inputs(self) -> dict:
        """Vérifie les touches maintenues et renvoie les actions correspondantes
        pour le joueur 1"""
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping1.values()}

        for key, action in self.mapping1.items():
            if keys[key]:
                p[action] = True


    def get_inputs2(self) -> dict:
        """Vérifie les touches maintenues et renvoie les actions correspondantes
        pour le joueur 2"""
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping2.values()}

        for key, action in self.mapping2.items():
            if keys[key]:
                p[action] = True

        return p
