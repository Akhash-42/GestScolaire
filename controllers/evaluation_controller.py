# controllers/evaluation_controller.py

from database.db import get_connection
from models.evaluation import Evaluation

class EvaluationController:
    
    @staticmethod
    def saisir_note(id_eleve, id_matiere, note, semestre, date_eval):
        """Insère une nouvelle note dans la base de données."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO evaluation (id_eleve, id_matiere, note, semestre, date_eval)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (id_eleve, id_matiere, note, semestre, date_eval))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la saisie de la note : {e}")
            return False

    @staticmethod
    def obtenir_moyennes_par_matiere(id_eleve, semestre):
        """
        Calcule la moyenne d'un élève pour chaque matière pour un semestre donné,
        en incluant le coefficient de la matière.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Cette requête récupère la moyenne des notes par matière ainsi que son coefficient
        query = """
            SELECT m.id AS id_matiere, m.nom AS nom_matiere, m.coefficient, AVG(e.note) AS moyenne_matiere
            FROM evaluation e
            JOIN matiere m ON e.id_matiere = m.id
            WHERE e.id_eleve = ? AND e.semestre = ?
            GROUP BY m.id
        """
        cursor.execute(query, (id_eleve, semestre))
        rows = cursor.fetchall()
        conn.close()
        
        resultat = []
        for row in rows:
            moyenne_arrondie = round(row['moyenne_matiere'], 2)
            resultat.append({
                "id_matiere": row['id_matiere'],
                "nom_matiere": row['nom_matiere'],
                "coefficient": row['coefficient'],
                "moyenne": moyenne_arrondie,
                "mention": Evaluation.calculer_mention(moyenne_arrondie)  # Appel au modèle
            })
            
        return resultat

    @staticmethod
    def obtenir_bulletin_general(id_eleve, semestre):
        """
        Génère le résumé global pour l'élève : moyennes par matière, 
        moyenne générale et mention globale.
        """
        # 1. Récupérer les moyennes par matière
        moyennes_matieres = EvaluationController.obtenir_moyennes_par_matiere(id_eleve, semestre)
        
        if not moyennes_matieres:
            return {
                "moyennes_matieres": [],
                "moyenne_generale": 0.0,
                "mention_generale": "Aucune note"
            }
            
        # 2. Calculer la moyenne générale via le Modèle
        moyenne_generale = Evaluation.calculer_moyenne_generale(moyennes_matieres)
        
        # 3. Attribuer la mention globale via le Modèle
        mention_generale = Evaluation.calculer_mention(moyenne_generale)
        
        return {
            "id_eleve": id_eleve,
            "semestre": semestre,
            "moyennes_matieres": moyennes_matieres,
            "moyenne_generale": moyenne_generale,
            "mention_generale": mention_generale
        }