-- mart_weather_summary: aggregated view ready for reporting
-- this is what an analyst or dashboard would consume

with weather as (

    select * from {{ ref('stg_weather') }}

)

select
    comfort_level,
    count(*)                        as city_count,
    round(avg(temp_c), 1)           as avg_temp_c,
    round(avg(humidity_pct), 1)     as avg_humidity,
    round(avg(wind_kmph), 1)        as avg_wind_kmph,
    min(temp_c)                     as min_temp_c,
    max(temp_c)                     as max_temp_c

from weather
group by comfort_level
order by avg_temp_c desc