with
    customer_count as (
        select
            customer_id,
            min(order_date) as first_visit
        from
            customer_orders
        group by
            customer_id
    ),
    visit_frequency as (
        select
            order_date,
            o.customer_id,
            first_visit,
            case
                when order_date = first_visit then 1
                else 0
            end as first_customer,
            case
                when order_date != first_visit then 1
                else 0
            end as repeated_customer
        from
            customer_orders o
            inner join customer_count c on o.customer_id = c.customer_id
    )
select
    order_date,
    sum(first_customer) as new_customers,
    sum(repeated_customer) as repeat_customers
from
    visit_frequency
group by
    order_date
order by
    order_date
