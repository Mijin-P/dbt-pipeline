"""
load_postgres.py
Charge les données extraites de l'API FastAPI dans PostgreSQL.

Pattern ELT : on dépose les données BRUTES dans un schéma `raw` au format
JSONB. dbt se chargera ensuite de typer / nettoyer / modéliser à partir de là.

Prérequis :
  - psycopg2-binary (déjà installé via dbt-postgres)
  - requests (utilisé par fetch_api.py)
  - une base PostgreSQL déjà créée (voir variable PG_DATABASE ci-dessous)

Lancement (depuis le dossier contenant ce fichier ET fetch_api.py) :
    python load_postgres.py
"""

import os
import json
import logging
from datetime import datetime, timezone

import psycopg2
from psycopg2.extras import execute_values

from fetch_api import fetch_all_entities
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration de la connexion.
# Par défaut : valeurs locales classiques. Tu peux les surcharger sans toucher
# au code via des variables d'environnement (PG_HOST, PG_PASSWORD, etc.),
# ce qui évite d'écrire ton mot de passe en dur dans le fichier.
# ---------------------------------------------------------------------------
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("PG_HOST", "localhost"),
    "port":     os.getenv("PG_PORT", "5432"),
    "dbname":   os.getenv("PG_DATABASE", "banque"),
    "user":     os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD"),  # plus de défaut → force à le définir
}

RAW_SCHEMA = "raw"


def get_connection():
    """Ouvre une connexion PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def create_schema_and_tables(conn, entities):
    """
    Crée le schéma `raw` et une table par entité si elles n'existent pas.
    Chaque table stocke : un id auto, la donnée brute en JSONB, un horodatage.
    """
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA};")
        for entity in entities:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {RAW_SCHEMA}.{entity} (
                    id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    data      JSONB NOT NULL,
                    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )
    conn.commit()
    logger.info(f"Schéma '{RAW_SCHEMA}' et tables prêts : {', '.join(entities)}")


def load_entity(conn, entity, records):
    """
    Charge une entité en mode FULL REFRESH : on vide la table puis on réinsère
    tout. Insertion par lot avec execute_values (rapide, une seule requête).
    """
    if not records:
        logger.warning(f"  [{entity}] aucun enregistrement — table laissée vide")
        return

    loaded_at = datetime.now(timezone.utc)
    rows = [(json.dumps(record), loaded_at) for record in records]

    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {RAW_SCHEMA}.{entity};")
        execute_values(
            cur,
            f"INSERT INTO {RAW_SCHEMA}.{entity} (data, loaded_at) VALUES %s",
            rows,
        )
    conn.commit()
    logger.info(f"  [{entity}] {len(rows)} enregistrements chargés "
                f"dans {RAW_SCHEMA}.{entity}")


def main():
    logger.info("=== 1/2 Extraction depuis l'API ===")
    data = fetch_all_entities()  # { "clients": [...], "produits": [...], ... }

    logger.info("=== 2/2 Chargement dans PostgreSQL ===")
    conn = get_connection()
    try:
        create_schema_and_tables(conn, list(data.keys()))
        for entity, records in data.items():
            load_entity(conn, entity, records)
        logger.info("=== Pipeline terminé avec succès ===")
    except Exception:
        conn.rollback()
        logger.exception("Erreur pendant le chargement — rollback effectué")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()