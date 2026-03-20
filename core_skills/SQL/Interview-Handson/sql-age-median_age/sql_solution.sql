with
    ord_rank as (
        select
            e.*,
            row_number() over (
                order by
                    emp_age
            ) as rank_asc,
            row_number() over (
                order by
                    emp_age desc
            ) as rank_desc
        from
            emp e
    )
select
    *
from
    ord_rank
where
    abs(rank_asc - rank_desc) <= 1