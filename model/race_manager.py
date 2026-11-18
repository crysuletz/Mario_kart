class RaceManager:
    """gère la course : les tours, les checkpoints et le gagnant"""

    def __init__(self, total_checkpoints: int, total_laps: int):
        """initialise la course pour les 2 joueurs"""
        self.total_checkpoints = total_checkpoints
        self.total_laps = total_laps
        # tours faits par le joueur 1 et le joueur 2
        self.laps = {1: 0, 2: 0}
        # checkpoints passés pendant le tour en cours
        self.passed_checkpoints = {1: [], 2: []}
        # personne n'a gagné au début
        self.winner = None

    def pass_checkpoint(self, player: int, col: int, row: int) -> None:
        """retient qu'un joueur est passé sur un checkpoint"""
        position = (col, row)
        # on l'ajoute si le joueur est pas déjà passé dessus
        if position not in self.passed_checkpoints[player]:
            self.passed_checkpoints[player].append(position)
    
