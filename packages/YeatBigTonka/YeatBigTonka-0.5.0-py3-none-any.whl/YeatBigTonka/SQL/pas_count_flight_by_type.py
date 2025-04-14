"""Для каждого пассажира определить количество полетов по типам самолетов.
Вывод: имя пассажира, тип самолета, количество перелетов этим типом самолета. Результат упорядочить по именам пассажиров (в алфавитном порядке) и убыванию количества перелетов.
Примечание: Задача «с подвохом» в БД есть полные тезки (Bruce Willis), они отличаются кодом (Id_psg), поэтому группировать результат надо не по имени пассажира, а по его коду
"""

def sql():
    a = """
        SELECT
            p.name,
            t.plane,
            COUNT(*) AS cnt_trip
        FROM Passenger p
        JOIN Pass_in_trip pt ON p.ID_psg = pt.ID_psg
        JOIN Trip t ON pt.trip_no = t.trip_no
        GROUP BY p.ID_psg, p.name, t.plane
        ORDER BY p.name, cnt_trip DESC;
    """