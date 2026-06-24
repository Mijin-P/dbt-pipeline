from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.data.generator import CLIENTS

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", summary="Liste tous les clients")
def liste_clients(
    segment: Optional[str] = Query(None, description="Filtrer par segment : particulier, premium, professionnel"),
    ville:   Optional[str] = Query(None, description="Filtrer par ville"),
    limit:   int           = Query(10,  ge=1, le=100, description="Nombre de résultats"),
    offset:  int           = Query(0,   ge=0,         description="Décalage pour la pagination"),
):
    resultats = CLIENTS

    if segment:
        resultats = [c for c in resultats if c["segment"] == segment]
    if ville:
        resultats = [c for c in resultats if ville.lower() in c["ville"].lower()]

    total = len(resultats)
    resultats = resultats[offset: offset + limit]

    return {
        "total":   total,
        "limit":   limit,
        "offset":  offset,
        "data":    resultats,
    }


@router.get("/{client_id}", summary="Récupère un client par son ID")
def get_client(client_id: str):
    client = next((c for c in CLIENTS if c["client_id"] == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return client