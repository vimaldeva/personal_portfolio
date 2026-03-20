WITH
    productwise_sales AS (
        SELECT
            product_id,
            round(sum(sales)) as prod_sales
        from
            orders
        group by
            product_id
    ),
    running_sales as (
        select
            product_id,
            prod_sales,
            (
                sum(prod_sales) over (
                    order by
                        prod_sales desc
                )
            ) as run_sales
        from
            productwise_sales
    ),
    total_sales AS (
        SELECT
            ROUND(SUM(sales) * 0.8) AS total_sales
        FROM
            orders
    )
SELECT
    *
FROM
    running_sales
    cross join total_sales
where
    run_sales <= total_sales;


---------------------------

select  ROUND(SUM(sales)) from orders ;

select count(distinct product_id) from orders
-- total sales = 304660
-- 80% sales = 243728
-- distinct product = 1010
-- query as per paletto principle = 232 (satisfiles 80% revenue)
