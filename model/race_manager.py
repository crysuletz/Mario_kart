class RaceManager:
    """gère la course : les tours, les checkpoints et le gagnant"""

    def __init__(self, total_checkpoints: int, total_laps: int):
        """initialise la course pour les 2 joueurs"""
        self.total_checkpoints = total_checkpoints
        self.total_laps = total_laps
        # tours faits par le joueur 1 et le joueur 2
        self.laps = {1: 0, 2: 0}
        # numéros des checkpoints passés pendant le tour en cours
        self.passed_checkpoints = {1: [], 2: []}
        # personne n'a gagné au début
        self.winner = None

    def pass_checkpoint(self, player: int, number: int) -> None:
        """retient le checkpoint seulement si c'est le suivant dans l'ordre du circuit"""
        # le prochain checkpoint attendu, c'est le nombre de checkpoints déjà passés + 1
        prochain = len(self.passed_checkpoints[player]) + 1
        if number == prochain:
            self.passed_checkpoints[player].append(number)

    def pass_finish_line(self, player: int) -> None:
        """ajoute un tour si tous les checkpoints sont passés et vérifie si le joueur a gagné"""
        if len(self.passed_checkpoints[player]) == self.total_checkpoints:
            self.laps[player] = self.laps[player] + 1
            # on vide la liste pour recommencer au tour suivant
            self.passed_checkpoints[player] = []
            # le premier qui fait tous les tours gagne
            if self.laps[player] == self.total_laps and self.winner is None:
                self.winner = player