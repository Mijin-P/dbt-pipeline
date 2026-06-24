with clients as (
    select * from {{ ref('slv_clients') }}
),
contrats as (
    select * from {{ ref('slv_contrats') }}
    where statut = 'actif' -- On ne prend que les contrats en cours
),
stats_contrats as (
    select
        client_id,
        count(contrat_id) as nb_contrats_actifs,
        sum(montant) as encours_total,
        sum(frais_mensuels) as total_frais_mensuels
    from contrats
    group by client_id
)

select
    cl.client_id,
    cl.nom,
    cl.prenom,
    cl.segment,
    cl.agence,
    cl.date_adhesion,
    
    -- Données calculées
    coalesce(sc.nb_contrats_actifs, 0) as nb_contrats_actifs,
    coalesce(sc.encours_total, 0) as encours_total,
    coalesce(sc.total_frais_mensuels, 0) as total_frais_mensuels

from clients cl
left join stats_contrats sc on cl.client_id = sc.client_id