class Block:
    """bloc posé sur une case du circuit"""

    def __init__(self, name: str, color: tuple[int, int, int]):
        """crée un bloc avec un nom et une couleur"""
        # nom du bloc par exemple boost
        self.name = name
        # couleur du bloc en rouge, vert, bleu
        self.color = color

class Boost(Block):
    """case du circuit qui fait accélérer la voiture"""

    def __init__(self):
        """crée un bloc boost orange"""
        # on appelle le constructeur de Block pour donner le nom et la couleur
        super().__init__("boost", (255, 140, 0))

class Checkpoint(Block):
    """point de passage -> la voiture doit passer sur tous les checkpoints avant la ligne d'arrivée"""

    def __init__(self):
        """crée un checkpoint affiché en bleu clair"""
        # on appelle le constructeur de Block avec le nom et la couleur du checkpoint
        super().__init__("checkpoint", (0, 200, 255))
