"""Определить количество перевезенных пассажиров авиакомпаниями по месяцам и годам.
Вывод: название авиакомпании, месяц, год, число перевезенных пассажиров.
 Упорядочить результат по возрастанию года и месяца и по убыванию числа пассажиров.
"""

def sql():
    a = """
        SELECT
            c.name AS name,
            EXTRACT(MONTH FROM pt.date_trip) AS month_trip,
            EXTRACT(YEAR FROM pt.date_trip) AS year_trip,
            COUNT(*) AS cnt_trip
        FROM Company c
        JOIN Trip t ON c.ID_comp = t.ID_comp
        JOIN Pass_in_trip pt ON t.trip_no = pt.trip_no
        GROUP BY c.name, EXTRACT(YEAR FROM pt.date_trip), EXTRACT(MONTH FROM pt.date_trip)
        ORDER BY year_trip, month_trip, cnt_trip DESC;
    """


