with raw_data as (
    select * from {{ref('bronze_contrats')}}
)

select
    (data ->> 'contrat_id')::varchar as contrat_id,
    (data ->> 'client_id')::varchar as client_id,
    (data ->> 'produit_id')::varchar as produit_id,
    (data ->> 'statut')::varchar as statut,
    (data ->> 'montant')::numeric as montant,
    (data ->> 'frais_mensuels')::numeric as frais_mensuels,
    (data ->> 'date_debut')::date as date_debut,
    (data ->> 'date_fin')::date as date_fin

from raw_data