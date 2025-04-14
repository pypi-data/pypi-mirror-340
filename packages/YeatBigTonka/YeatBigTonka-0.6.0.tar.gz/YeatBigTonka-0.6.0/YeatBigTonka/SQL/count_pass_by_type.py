"""Для каждой авиакомпании посчитать количество перевезенных пассажиров по типам самолетов.
Вывод: название авиакомпании, тип самолета, количество перевезенных пассажиров.
"""

def sql():
    a = """
        SELECT
            c.name AS name,
            t.plane AS plane,
            COUNT(*) AS cnt_pass
        FROM Company c
        JOIN Trip t ON c.ID_comp = t.ID_comp
        JOIN Pass_in_trip pt ON t.trip_no = pt.trip_no
        GROUP BY c.name, t.plane;
    """