# models/evaluation.py

class Evaluation:
    def __init__(self, id_eleve, id_matiere, note, semestre, date_eval=None, id=None):
        self.id = id
        self.id_eleve = id_eleve
        self.id_matiere = id_matiere
        self.note = float(note)
        self.semestre = int(semestre)
        self.date_eval = date_eval

    @staticmethod
    def calculer_mention(moyenne):
        """Attribue automatiquement une mention selon la moyenne obtenue."""
        if moyenne >= 16:
            return "Très Bien"
        elif moyenne >= 14:
            return "Bien"
        elif moyenne >= 12:
            return "Assez Bien"
        elif moyenne >= 10:
            return "Passable"
        else:
            return "Insuffisant"

    @staticmethod
    def calculer_moyenne_generale(liste_moyennes_matieres):
        """
        Calcule la moyenne générale en tenant compte des coefficients.
        liste_moyennes_matieres doit être une liste de dictionnaires :
        [{'moyenne': 14, 'coefficient': 2}, {'moyenne': 11, 'coefficient': 3}]
        """
        if not liste_moyennes_matieres:
            return 0.0

        total_points = 0.0
        total_coefficients = 0.0

        for item in liste_moyennes_matieres:
            total_points += item['moyenne'] * item['coefficient']
            total_coefficients += item['coefficient']

        if total_coefficients == 0:
            return 0.0
            
        return round(total_points / total_coefficients, 2)