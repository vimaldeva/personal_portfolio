with
    friend_marks as (
        select
            pid,
            count(*) as no_of_friends,
            sum(score) as total_friend_score
        from
            friend f
            inner join person p on f.fid = p.personid
        group by
            pid
        having
            sum(score) > 100
    )
select
    pid ,
    total_friend_score,
    no_of_friends,
    name as person_name
from
    friend_marks f
    inner join person p on p.personid = f.pid


