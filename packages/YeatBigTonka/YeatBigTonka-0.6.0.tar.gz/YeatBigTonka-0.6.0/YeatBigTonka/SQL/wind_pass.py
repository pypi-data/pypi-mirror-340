
"""Для пассажиров летавших у окна (места a или d) вывести следующую информацию: имя пассажира, название авиакомпании,
 дата и время вылета (одно значение), город вылета, город прилета.
"""
def sql():
    a = """
        SELECT
            p.name AS Name_psg,
            c.name AS Name_comp,
            CONCAT(pt.date_trip, ' ', t.time_out) AS dt_out,
            t.town_from,
            t.town_to
        FROM Pass_in_trip pt
        JOIN Passenger p ON pt.id_psg = p.id_psg
        JOIN Trip t ON pt.trip_no = t.trip_no
        JOIN Company c ON t.id_comp = c.id_comp
        WHERE LOWER(SUBSTRING(pt.place, -1)) IN ('a', 'd');
    """