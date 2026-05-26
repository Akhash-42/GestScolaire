class Enseignant:
    def __init__(self, id_enseignant: int, nom: str, prenom: str, email: str = None):
        self.id = id_enseignant
        self.nom = nom
        self.prenom = prenom
        self.email = email

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def __str__(self):
        return f"Enseignant : {self.nom_complet} ({self.email if self.email else 'Pas d\'email'})"
