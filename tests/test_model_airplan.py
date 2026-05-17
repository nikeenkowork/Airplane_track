from src.model_airplan import Aeroplane


def test_init_defaults():
    """
    Проверяет, что при None-значениях в конструкторе
    устанавливаются значения по умолчанию:
    - callsign = "UNKNOWN"
    - country = "UNKNOWN"
    - velocity = 0.0
    - altitude = 0.0
    """
    plane = Aeroplane(None, None, None, None)

    assert plane.callsign == "UNKNOWN"
    assert plane.country == "UNKNOWN"
    assert plane.velocity == 0.0
    assert plane.altitude == 0.0


def test_init_values():
    """
    Проверяет корректную инициализацию объекта Aeroplane
    при передаче валидных значений.
    """
    plane = Aeroplane("ABC123", "CZ", 250, 10000)

    assert plane.callsign == "ABC123"
    assert plane.country == "CZ"
    assert plane.velocity == 250.0
    assert plane.altitude == 10000.0


def test_cast_to_object_list():
    """
    Проверяет преобразование сырых данных OpenSky
    в список объектов Aeroplane.
    """
    raw_data = [
        [
            0,
            "CS123",
            "CZ",
            None,
            None,
            None,
            None,
            None,
            None,
            300,
            None,
            None,
            None,
            5000,
        ],
        [
            0,
            "DE456",
            "DE",
            None,
            None,
            None,
            None,
            None,
            None,
            250,
            None,
            None,
            None,
            3000,
        ],
    ]

    planes = Aeroplane.cast_to_object_list(raw_data)

    assert len(planes) == 2
    assert planes[0].callsign == "CS123"
    assert planes[1].country == "DE"


def test_comparison_lt():
    """
    Проверяет работу оператора < для Aeroplane.
    Сравнение идёт по (altitude, velocity).
    """
    p1 = Aeroplane("A", "CZ", 200, 3000)
    p2 = Aeroplane("B", "CZ", 200, 5000)

    assert p1 < p2


def test_comparison_eq():
    """
    Проверяет равенство двух объектов Aeroplane.
    Объекты равны, если совпадают altitude и velocity.
    """
    p1 = Aeroplane("A", "CZ", 200, 3000)
    p2 = Aeroplane("B", "CZ", 200, 3000)

    assert p1 == p2


def test_sorting():
    """
    Проверяет корректность сортировки списка самолётов.
    Сортировка выполняется по высоте, затем по скорости (по убыванию при reverse=True).
    """
    planes = [
        Aeroplane("A", "CZ", 200, 1000),
        Aeroplane("B", "CZ", 200, 5000),
        Aeroplane("C", "CZ", 200, 3000),
    ]

    sorted_planes = sorted(planes, reverse=True)

    assert sorted_planes[0].altitude == 5000
    assert sorted_planes[-1].altitude == 1000
