
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "scolarite.db")


def get_connection():
    """Retourne une connexion à la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    conn.execute("PRAGMA foreign_keys = ON") 
    return conn


def initialiser_base():
    """Crée toutes les tables si elles n'existent pas encore."""
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Table : annee_scolaire
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS annee_scolaire (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            libelle     TEXT NOT NULL UNIQUE  -- ex: "2025-2026"
        )
    """)

    # -------------------------
    # Table : classe
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classe (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nom             TEXT NOT NULL,        -- ex: "Seconde A", "Terminale C"
            id_annee        INTEGER NOT NULL,
            FOREIGN KEY (id_annee) REFERENCES annee_scolaire(id)
        )
    """)

    # -------------------------
    # Table : enseignant
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enseignant (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom         TEXT NOT NULL,
            prenom      TEXT NOT NULL,
            email       TEXT
        )
    """)

    # -------------------------
    # Table : matiere
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matiere (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nom             TEXT NOT NULL,       -- ex: "Mathématiques"
            coefficient     REAL NOT NULL DEFAULT 1.0
        )
    """)

    # -------------------------
    # Table : classe_matiere
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classe_matiere (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            id_classe       INTEGER NOT NULL,
            id_matiere      INTEGER NOT NULL,
            id_enseignant   INTEGER,
            FOREIGN KEY (id_classe)     REFERENCES classe(id),
            FOREIGN KEY (id_matiere)    REFERENCES matiere(id),
            FOREIGN KEY (id_enseignant) REFERENCES enseignant(id),
            UNIQUE (id_classe, id_matiere)  -- Une matière une seule fois par classe
        )
    """)

    # -------------------------
    # Table : eleve
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eleve (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nom             TEXT NOT NULL,
            prenom          TEXT NOT NULL,
            date_naissance  TEXT,               -- Format: "YYYY-MM-DD"
            id_classe       INTEGER,
            id_annee        INTEGER,
            FOREIGN KEY (id_classe) REFERENCES classe(id),
            FOREIGN KEY (id_annee)  REFERENCES annee_scolaire(id)
        )
    """)

    # -------------------------
    # Table : evaluation
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eleve    INTEGER NOT NULL,
            id_matiere  INTEGER NOT NULL,
            note        REAL NOT NULL CHECK(note >= 0 AND note <= 20),
            semestre    INTEGER NOT NULL CHECK(semestre IN (1, 2)),  -- 1 ou 2
            date_eval   TEXT,                   -- Format: "YYYY-MM-DD"
            FOREIGN KEY (id_eleve)   REFERENCES eleve(id),
            FOREIGN KEY (id_matiere) REFERENCES matiere(id)
        )
    """)

    # -------------------------
    # Table : utilisateur
    # Gestion de l'authentification (admin ou élève)
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateur (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            login       TEXT NOT NULL UNIQUE,
            mot_de_passe TEXT NOT NULL,         -- À hasher en production
            role        TEXT NOT NULL CHECK(role IN ('admin', 'eleve')),
            id_eleve    INTEGER,                -- NULL si c'est un admin
            FOREIGN KEY (id_eleve) REFERENCES eleve(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès!!!!")


def reinitialiser_base():
    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        "utilisateur",
        "evaluation",
        "eleve",
        "classe_matiere",
        "matiere",
        "enseignant",
        "classe",
        "annee_scolaire"
    ]

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()
    conn.close()
    initialiser_base()
    print("Base de données réinitialisée.")


if __name__ == "__main__":
    initialiser_base()
