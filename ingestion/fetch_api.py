"""
fetch_api.py
Récupère toutes les données de l'API FastAPI avec pagination.
Retourne une liste de dicts prête à être sérialisée en JSONL.
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

# Endpoints paginés et non paginés
ENDPOINTS = {
    "clients":  {"path": "/clients",  "paginated": True},
    "produits": {"path": "/produits", "paginated": False},
    "contrats": {"path": "/contrats", "paginated": True},
}


def fetch_paginated(path: str, page_size: int = 100) -> list[dict]:
    """
    Parcourt toutes les pages d'un endpoint paginé
    Utilise limit/offset jusqu'à avoir tout récupérer
    """
    all_records = []
    offset = 0

    while True:
        params = {"limit": page_size, "offset": offset}
        response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
        response.raise_for_status()  # lève une exception si erreur HTTP

        data = response.json()
        records = data.get("data", [])
        total = data.get("total", 0)

        all_records.extend(records)
        logger.info(f"  [{path}] récupéré {len(all_records)}/{total} enregistrements")

        # Condition d'arrêt : on a tout récupéré
        if offset + page_size >= total:
            break

        offset += page_size

    return all_records


def fetch_simple(path: str) -> list[dict]:
    """
    Récupère un endpoint non paginé (ex: /produits).
    """
    response = requests.get(f"{BASE_URL}{path}", timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


def fetch_all_entities() -> dict[str, list[dict]]:
    """
    Point d'entrée principal : récupère toutes les entités.
    Retourne un dict  { "clients": [...], "produits": [...], "contrats": [...] }
    """
    result = {}

    for entity, config in ENDPOINTS.items():
        logger.info(f"Récupération de : {entity}")
        try:
            if config["paginated"]:
                records = fetch_paginated(config["path"])
            else:
                records = fetch_simple(config["path"])

            result[entity] = records
            logger.info(f"  OK {entity} : {len(records)} enregistrements récupérés")

        except requests.exceptions.ConnectionError:
            logger.error(f"  FAIL Impossible de joindre l'API sur {BASE_URL}. Est-elle lancée ?")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"  FAIL Erreur HTTP sur {entity} : {e}")
            raise

    return result