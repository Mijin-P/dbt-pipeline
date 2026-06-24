with raw_data as (
    select * from {{ref('bronze_clients')}}
)

select
    (data ->> 'client_id')::varchar as client_id,
    (data ->> 'civilite')::varchar as civilite,
    (data ->> 'nom')::varchar as nom,
    (data ->> 'prenom')::varchar as prenom,
    (data ->> 'email')::varchar as email,
    (data ->> 'telephone')::varchar as telephone,
    (data ->> 'adresse')::varchar as adresse,
    (data ->> 'ville')::varchar as ville,
    (data ->> 'code_postal')::varchar as code_postal,
    (data ->> 'pays')::varchar as pays,
    (data ->> 'agence')::varchar as agence,
    (data ->> 'segment')::varchar as segment,
    (data ->> 'date_adhesion')::date as date_adhesion,
    (data ->> 'date_naissance')::date as date_naissance

from raw_data