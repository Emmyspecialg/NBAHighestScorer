use warehouse PC_DBT_WH;
--select * from PC_DBT_DB.INFORMATION_SCHEMA.ENABLED_ROLES;

select first_name, last_name, points 
from {{ ref('scores_2022_10_18')}}
order by points desc;
