with RECURSIVE
    s_days as (
        select
            product_id,
            period_start,
            period_end,
            average_daily_sales,
            period_start as sales_date
        from
            sales
        union all
        select
            product_id,
            period_start,
            period_end,
            average_daily_sales,
            sales_date + 1 as sales_date
        from
            s_days
        where
            sales_date < period_end
    )
select
    PRODUCT_ID,
    year (sales_date) as a_year,
    sum(average_daily_sales) as total_sales
from
    s_days
group by
    product_id,
    a_year
order by
    product_id,
    a_year