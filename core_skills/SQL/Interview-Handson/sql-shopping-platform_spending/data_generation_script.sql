with
    combined_data as (
        select
            spend_date,
            platform,
            count(*) as total_sales,
            sum(amount) as total_amount
        from
            spending
        group by
            spend_date,
            platform
        order by
            spend_date,
            platform
    )
select
    *
from
    combined_data
union
select
    spend_date,
    'both' as platform,
    sum(total_sales) as total_sales,
    sum(total_amount) as total_amount
from
    combined_data
group by
    spend_date,
    platform
