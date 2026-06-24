# dbt-pipeline
Pipeline ELT complète, de la génération des données jusqu'à leur restitution, construite autour d'une architecture médaillon (bronze / silver / gold).

Le projet illustre une chaîne data end-to-end : 

| Étape | Rôle | Stack | Dossier |
|-------|------|-------|-------|
| **Extract** | Une API REST expose les données source | FastAPI | api |
| **Load** | Ingestion des données de l'API vers PostgreSQL | Python, psycopg2 / SQLAlchemy | ingestion |
| **Transform** | Modélisation en couches bronze / silver / gold | dbt, PostgreSQL | dbt_project |

## Structure du projet

<img width="978" height="331" alt="image" src="https://github.com/user-attachments/assets/73347952-001f-462d-a855-2182221bfdbc" />


## L'architecture médaillon

Le pipeline organise les données en trois couches de qualité croissante :

- **Bronze** — données brutes ingérées telles quelles depuis l'API, sans transformation. Elles constituent la source de vérité et permettent de rejouer le pipeline.
- **Silver** — données nettoyées : typage, suppression des doublons, normalisation, gestion des valeurs manquantes.
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

## Technologies

- **FastAPI** — exposition des données source via une API REST
- **Python** — orchestration de l'ingestion (Extract & Load)
- **PostgreSQL** — entrepôt de données
- **dbt** — transformation, modélisation et tests de qualité

## Auteur

**Mijin PARK** —  [LinkedIn](https://www.linkedin.com/in/mijin-park-a44182227/)
