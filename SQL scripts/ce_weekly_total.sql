SELECT 
    b.*,
    s.amount,
    b.bonus_sum + b.game_sum + s.amount AS weekly_total
FROM (
    -- base: your existing aggregation by date
    SELECT 
        date,
        SUM(bonus) AS bonus_sum,
        SUM(
            CASE
                WHEN isChampion = 1 THEN (
                    CASE WHEN gameTotal + gameTotal >= 40000 THEN 75000 ELSE 50000 END
                )
                WHEN (isChampion = 0 AND isSecondChance = 1) THEN gameTotal + 5000
                WHEN (isChampion = 0 AND isCashChallenge = 1) THEN gameTotal + gameTotal
                ELSE gameTotal
            END
        ) AS game_sum,
        SUM(isChampion) AS champCount
    FROM players
    GROUP BY date
) AS b
JOIN (
    -- streak/amount calc, derived table instead of CTE
    SELECT
        id,
        date,
        playerID,
        LEAST(streak_pos - 1, 2) * 50000 AS amount
    FROM (
        SELECT
            id,
            date,
            playerID,
            ROW_NUMBER() OVER (PARTITION BY playerID, grp_id ORDER BY id) AS streak_pos
        FROM (
            SELECT
                id,
                date,
                playerID,
                ROW_NUMBER() OVER (ORDER BY id)
                - ROW_NUMBER() OVER (PARTITION BY playerID ORDER BY id) AS grp_id
            FROM champions
        ) AS grp
    ) AS streak
) AS s
    ON b.date = s.date;