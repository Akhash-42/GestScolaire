class Classe:
    def __init__(self, id_classe: int, nom: str, id_annee: int):
        self.id = id_classe
        self.nom = nom
        self.id_annee = id_annee

    def __str__(self):
        return f"Classe N°{self.id} : {self.nom}"
