from faker import Faker
from datetime import date, timedelta
import random
import uuid

fake = Faker("fr_FR")  # données en français

PRODUITS = [
    {"id": "P001", "nom": "Compte Courant",        "type": "compte",    "frais_mensuels": 0.00},
    {"id": "P002", "nom": "Livret A",              "type": "epargne",   "frais_mensuels": 0.00},
    {"id": "P003", "nom": "Assurance Vie",         "type": "assurance", "frais_mensuels": 15.00},
    {"id": "P004", "nom": "Carte Visa Premier",    "type": "carte",     "frais_mensuels": 12.00},
    {"id": "P005", "nom": "Prêt Immobilier",       "type": "credit",    "frais_mensuels": 0.00},
    {"id": "P006", "nom": "Prêt Consommation",     "type": "credit",    "frais_mensuels": 0.00},
    {"id": "P007", "nom": "Plan Épargne Retraite", "type": "epargne",   "frais_mensuels": 5.00},
    {"id": "P008", "nom": "Carte Visa Classic",    "type": "carte",     "frais_mensuels": 4.50},
]

STATUTS_CONTRAT = ["actif", "résilié", "suspendu", "en_attente"]
AGENCES = ["Paris Centre", "Lyon Part-Dieu", "Marseille Vieux-Port",
           "Bordeaux Saint-Jean", "Lille Grand Place", "Nantes Centre"]

def generer_client():
    sexe = random.choice(["M", "F"])
    prenom = fake.first_name_male() if sexe == "M" else fake.first_name_female()
    nom = fake.last_name()
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=85)
    date_adhesion = fake.date_between(start_date="-10y", end_date="today")

    return {
        "client_id":       str(uuid.uuid4()),
        "civilite":        "M." if sexe == "M" else "Mme",
        "prenom":          prenom,
        "nom":             nom,
        "date_naissance":  str(date_naissance),
        "email":           fake.email(),
        "telephone":       fake.phone_number(),
        "adresse":         fake.street_address(),
        "code_postal":     fake.postcode(),
        "ville":           fake.city(),
        "pays":            "France",
        "agence":          random.choice(AGENCES),
        "date_adhesion":   str(date_adhesion),
        "segment":         random.choice(["particulier", "premium", "professionnel"]),
    }

def generer_contrat(client_id: str, produit: dict):
    date_debut = fake.date_between(start_date="-8y", end_date="today")
    statut = random.choices(
        STATUTS_CONTRAT,
        weights=[70, 15, 10, 5]  # surtout des contrats actifs
    )[0]

    date_fin = None
    if statut == "résilié":
        date_fin = str(date_debut + timedelta(days=random.randint(30, 1500)))

    montant = None
    if produit["type"] == "credit":
        montant = round(random.uniform(5000, 350000), 2)
    elif produit["type"] in ["epargne", "assurance"]:
        montant = round(random.uniform(500, 80000), 2)

    return {
        "contrat_id":      str(uuid.uuid4()),
        "client_id":       client_id,
        "produit_id":      produit["id"],
        "statut":          statut,
        "date_debut":      str(date_debut),
        "date_fin":        date_fin,
        "montant":         montant,
        "frais_mensuels":  produit["frais_mensuels"],
    }


def generer_base(nb_clients: int = 100):
    clients = [generer_client() for _ in range(nb_clients)]
    contrats = []

    for client in clients:
        # chaque client souscrit entre 1 et 4 produits
        nb_produits = random.randint(1, 4)
        produits_choisis = random.sample(PRODUITS, nb_produits)
        for produit in produits_choisis:
            contrats.append(generer_contrat(client["client_id"], produit))

    return clients, PRODUITS, contrats


# Génération unique au démarrage (base en mémoire)
CLIENTS, PRODUITS_DB, CONTRATS = generer_base(nb_clients=100)