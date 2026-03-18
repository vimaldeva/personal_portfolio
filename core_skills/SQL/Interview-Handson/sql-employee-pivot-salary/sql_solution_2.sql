select
    emp_id,
    salary,
    bonus,
    hike_percent
from
    (
        select
            emp_id,
            salary_component_type,
            val
        from
            emp_compensation
    ) as Source_table pivot (
        max(val) for salary_component_type in ('salary', 'bonus', 'hike_percent')
    ) as Pivot_table