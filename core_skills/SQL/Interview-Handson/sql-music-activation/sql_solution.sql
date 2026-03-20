    with
        joined_table as (
            select
                u.*,
                type,
                access_date,
                case
                    when type = 'P' then access_date
                    else null
                end as prime_membership_date,
                case
                    when type = 'Music' then access_date
                    else null
                end as music_date
            from
                users u
                inner join events e on e.user_id = u.user_id
        ),
        grouped_table as (
            select
                user_id,
                name,
                max(join_date) as join_date,
                max(prime_membership_date) as prime_membership_date,
                max(music_date) as music_date
            from
                joined_table
            group by
                user_id,
                name
        ),
        total_users as (
            select
                count(user_id) as t_users 
            from
                users T INNER JOIN EVENTS E ON T.USER_ID = E.USER_ID WHERE E.TYPE = 'Music'
        ),
        activated_users as (
            select
                count(*) as a_users
            from
                grouped_table g
            where
                datediff ('day', join_date, prime_membership_date) <= 30
                and music_date is not null
        )
    select
        t_users as total_users,
        a_users as users_within_30_days,
        cast(((a_users * 100) / t_users) as decimal) as percentage_within_30_days
    from
        total_users
        cross join activated_users
