from fastapi import FastAPI
from api.routers import clients, produits, contrats

app = FastAPI(
    title="API Bancaire Fictive",
    description="API de données fictives pour pipeline data — portfolio data ingénieur",
    version="1.0.0",
)

# Enregistrement des routers
app.include_router(clients.router)
app.include_router(produits.router)
app.include_router(contrats.router)


@app.get("/", tags=["Accueil"])
def accueil():
    return {
        "message": "API Bancaire Fictive",
        "endpoints": ["/clients", "/produits", "/contrats"],
        "docs": "/docs",
    }

# python -m uvicorn api.main:app --reload