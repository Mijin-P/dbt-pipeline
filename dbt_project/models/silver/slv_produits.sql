with raw_data as (
    select * from {{ref('bronze_produits')}}
)

select
    (data ->> 'id')::varchar as produit_id,
    (data ->> 'nom')::varchar as nom_produit,
    (data ->> 'type')::varchar as type_produit,
    (data ->> 'frais_mensuels')::numeric as frais_mensuels_base

from raw_data