with
    temp_pivot as (
        select
            emp_id,
            case
                when salary_component_type = 'salary' then val
                else null
            end as salary,
            case
                when salary_component_type = 'bonus' then val
                else null
            end as bonus,
            case
                when salary_component_type = 'hike_percent' then val
                else null
            end as hike_percent
        from
            emp_compensation
    )
select
    emp_id,
    sum(salary) as salary,
    sum(bonus) as bonus,
    sum(hike_percent) as hike_percent
from
    temp_pivot
group by
    emp_id
