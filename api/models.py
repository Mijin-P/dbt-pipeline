from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    client_id:       str
    civilite:        str
    prenom:          str
    nom:             str
    date_naissance:  str
    email:           str
    telephone:       str
    adresse:         str
    code_postal:     str
    ville:           str
    pays:            str
    agence:          str
    date_adhesion:   str
    segment:         str  # particulier | premium | professionnel


class Produit(BaseModel):
    id:             str
    nom:            str
    type:           str   # compte | epargne | assurance | carte | credit
    frais_mensuels: float


class Contrat(BaseModel):
    contrat_id:     str
    client_id:      str
    produit_id:     str
    statut:         str           # actif | résilié | suspendu | en_attente
    date_debut:     str
    date_fin:       Optional[str] = None
    montant:        Optional[float] = None
    frais_mensuels: float