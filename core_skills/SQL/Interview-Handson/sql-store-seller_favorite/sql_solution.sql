    WITH com_player AS (
        SELECT first_player,  first_score
        FROM matches
        UNION ALL                                    
        SELECT second_player, second_score
        FROM matches
    ),
    group_points AS (
        SELECT
            first_player,
            group_id,
            SUM(first_score) AS total_score,
            ROW_NUMBER() OVER (
                PARTITION BY group_id
                ORDER BY SUM(first_score) DESC,      
                        first_player ASC
            ) AS point_rank
        FROM com_player c
        INNER JOIN players p ON c.first_player = p.player_id
        GROUP BY first_player, group_id             
    )
    SELECT
        group_id,
        first_player as player_id,
        total_score as score
    FROM group_points
    WHERE point_rank = 1
    ORDER BY group_id;                               