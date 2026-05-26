class Matiere:
    def __init__(self, id_matiere: int, nom: str, coefficient: float = 1.0):
        self.id = id_matiere
        self.nom = nom
        self.coefficient = coefficient

    def __str__(self):
        return f"Matière : {self.nom} (Coeff: {self.coefficient})"
