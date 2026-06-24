with contrats as (
    select * from {{ ref('slv_contrats') }}
),
clients as (
    select * from {{ ref('slv_clients') }}
),
produits as (
    select * from {{ ref('slv_produits') }}
)

select
    c.contrat_id,
    c.statut,
    c.montant,
    c.date_debut,
    
    -- Infos Produit
    p.nom_produit,
    p.type_produit,
    
    -- Frais réels (si null dans contrat, on prend le prix de base du produit)
    coalesce(c.frais_mensuels, p.frais_mensuels_base) as frais_mensuels_applicables,
    
    -- Infos Client
    cl.client_id,
    cl.civilite || ' ' || cl.prenom || ' ' || cl.nom as nom_complet,
    cl.segment,
    cl.agence,
    cl.ville

from contrats c
left join produits p on c.produit_id = p.produit_id
left join clients cl on c.client_id = cl.client_id