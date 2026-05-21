-- stg_weather: clean and rename raw weather fields
-- this is the first layer — just cleaning, no business logic yet

with source as (

    select * from raw_weather  -- we'll seed this from our extract step

),

staged as (

    select
        city,
        extracted_at,
        temp_c,
        feels_like_c,
        humidity_pct,
        weather_desc,
        wind_kmph,

        -- derive comfort level in SQL instead of PySpark
        case
            when temp_c >= 18 and humidity_pct <= 60 then 'comfortable'
            when temp_c < 5                          then 'cold'
            when humidity_pct > 80                   then 'humid'
            else                                          'moderate'
        end as comfort_level

    from source

)

select * from staged