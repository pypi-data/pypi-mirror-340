"""Для всех городов из таблицы Trip посчитать количество вылетов и прилетов за апрель 2025 года.
"""

def sql():
    a = """
        SELECT
            town,
            COUNT(CASE WHEN town = t.town_from THEN 1 END) AS cnt_out,
            COUNT(CASE WHEN town = t.town_to THEN 1 END) AS cnt_in
        FROM (
            SELECT town_from AS town FROM Trip
            UNION
            SELECT town_to FROM Trip
        ) AS all_towns
        JOIN Trip t ON t.town_from = all_towns.town OR t.town_to = all_towns.town
        JOIN Pass_in_trip pt ON t.trip_no = pt.trip_no
        WHERE pt.date_trip BETWEEN '2025-04-01' AND '2025-04-30'
        GROUP BY town;
    """

