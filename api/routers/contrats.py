from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.data.generator import CONTRATS

router = APIRouter(prefix="/contrats", tags=["Contrats"])


@router.get("/", summary="Liste tous les contrats")
def liste_contrats(
    statut:     Optional[str] = Query(None, description="Filtrer par statut : actif, résilié, suspendu, en_attente"),
    produit_id: Optional[str] = Query(None, description="Filtrer par produit"),
    limit:      int           = Query(10, ge=1, le=100), # greater or equal, less or equal
    offset:     int           = Query(0,  ge=0),
):
    resultats = CONTRATS

    if statut:
        resultats = [c for c in resultats if c["statut"] == statut]
    if produit_id:
        resultats = [c for c in resultats if c["produit_id"] == produit_id]

    total = len(resultats)
    resultats = resultats[offset: offset + limit]

    return {"total": total, "limit": limit, "offset": offset, "data": resultats}


@router.get("/{contrat_id}", summary="Récupère un contrat par son ID")
def get_contrat(contrat_id: str):
    contrat = next((c for c in CONTRATS if c["contrat_id"] == contrat_id), None)
    if not contrat:
        raise HTTPException(status_code=404, detail="Contrat introuvable")
    return contrat


@router.get("/client/{client_id}", summary="Tous les contrats d'un client")
def contrats_par_client(client_id: str):
    resultats = [c for c in CONTRATS if c["client_id"] == client_id]
    if not resultats:
        raise HTTPException(status_code=404, detail="Aucun contrat pour ce client")
    return {"total": len(resultats), "data": resultats}