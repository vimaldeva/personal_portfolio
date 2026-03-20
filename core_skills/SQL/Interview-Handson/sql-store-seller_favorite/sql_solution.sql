with
    rnk_orders as (
        select
            *,
            rank() over (
                partition by
                    seller_id
                order by
                    order_date asc
            ) as rn
        from
            orders
    )
select
    u.user_id as seller_id,
    case
        when i.item_brand = u.favorite_brand then 'Yes'
        else 'No'
    end as item_fav_brand
from
    users u
    LEFT join rnk_orders ro on ro.seller_id = u.user_id
    and rn = 2
    LEFT join items i on i.item_id = ro.item_id