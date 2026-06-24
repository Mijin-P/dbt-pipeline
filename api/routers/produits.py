from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.data.generator import PRODUITS_DB

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.get("/", summary="Liste tous les produits bancaires")
def liste_produits(
    type: Optional[str] = Query(None, description="Filtrer par type : compte, epargne, assurance, carte, credit"),
):
    resultats = PRODUITS_DB
    if type:
        resultats = [p for p in resultats if p["type"] == type]
    return {"total": len(resultats), "data": resultats}


@router.get("/{produit_id}", summary="Récupère un produit par son ID")
def get_produit(produit_id: str):
    produit = next((p for p in PRODUITS_DB if p["id"] == produit_id), None)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit