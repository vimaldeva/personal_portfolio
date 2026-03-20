with
    temp_table as (
        select
            1 as my_col
        union all
        select
            my_col + 1
        from
            temp_table
        where
            my_col < 10
    )
select
    *
from
    temp_table
