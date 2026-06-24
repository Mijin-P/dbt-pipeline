# dbt-pipeline

## A propos 
Ce projet est un projet portfolio réalisé dans le cadre de ma montée en compétences vers la Data Engineering. L'objectif est double : m'entraîner sur une chaîne de données de bout en bout, et démontrer concrètement ma maîtrise des outils et des bonnes pratiques du métier. Plutôt qu'un simple exercice théorique, j'ai voulu construire un pipeline complet et fonctionnel, reproductible et documenté.
Note : ce projet sera amené à évoluer

## Structure du projet

<img width="978" height="331" alt="image" src="https://github.com/user-attachments/assets/73347952-001f-462d-a855-2182221bfdbc" />

Le projet illustre une chaîne data end-to-end : 

| Étape | Rôle | Stack | Dossier |
|-------|------|-------|-------|
| **Extract** | Une API REST expose les données source | FastAPI | api |
| **Load** | Ingestion des données de l'API vers PostgreSQL | Python | ingestion |
| **Transform** | Modélisation en couches bronze / silver / gold | dbt, PostgreSQL | dbt_project |

### Choix des données :
**Pourquoi utiliser FastAPI ?** J'ai d'abord envisagé d'utiliser une API publique disponible en ligne comme source de données. Après en avoir testé plusieurs, j'ai préféré développer ma propre API en Python : les API publiques présentent souvent des limites pénalisantes pour un pipeline (lenteurs, instabilité, quotas, passage à un modèle payant). Créer mon API me garantit un flux de données fiable, maîtrisé et reproductible.
**Quelles sont les données analysées ?** Les données sont fictives et générées aléatoirement, mais conçues pour être représentatives de données bancaires réelles telles qu'on les rencontre en entreprise. Cela permet de travailler sur un cas réaliste sans aucune contrainte de confidentialité.
  
## L'architecture médaillon

Le pipeline organise les données en trois couches de qualité croissante :

- **Bronze** — données brutes ingérées telles quelles depuis l'API, sans transformation. 
- **Silver** — données nettoyées
- **Gold** — données agrégées et modélisées selon les besoins métier, directement exploitables pour l'analyse ou la visualisation.

## Prérequis

- Python 3.10+
- PostgreSQL 14+
- dbt (`dbt-postgres`)

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/Mijin-P/dbt-pipeline.git
cd dbt-pipeline

# Créer un environnement virtuel et installer les dépendances
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Copier le fichier d'exemple et renseigner vos propres valeurs :

```bash
cp .env.example .env
```

Variables attendues dans `.env` :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dbt_pipeline
POSTGRES_USER=votre_user
POSTGRES_PASSWORD=votre_mot_de_passe
```


## Utilisation

Exécuter les étapes dans l'ordre :

```bash
# 1. Lancer l'API qui expose les données source
uvicorn api.main:app --reload

# 2. Ingérer les données de l'API vers PostgreSQL (couche bronze)
python -m ingestion.run

# 3. Transformer les données avec dbt
cd dbt_project
dbt deps          # installe les packages dbt
dbt run           # exécute les modèles bronze ▸ silver ▸ gold
dbt test          # lance les tests de qualité de données
```

## Auteur

**Mijin PARK** —  [LinkedIn](https://www.linkedin.com/in/mijin-park-a44182227/)
