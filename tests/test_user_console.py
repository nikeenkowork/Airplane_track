from unittest.mock import Mock, patch

from src.user_console import Aeroplane, AeroplaneService


def test_to_objects():
    """
    Проверяет преобразование сырых данных в объекты Aeroplane.
    """
    raw = [
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
    ]

    result = AeroplaneService.to_objects(raw)

    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
    assert result[0].callsign == "CS123"


def test_filter_by_country():
    """
    Проверяет фильтрацию самолётов по странам.
    """
    planes = [
        Aeroplane("A", "CZ", 200, 1000),
        Aeroplane("B", "DE", 200, 2000),
        Aeroplane("C", "CZ", 200, 3000),
    ]

    result = AeroplaneService.filter_by_country(planes, ["CZ"])

    assert len(result) == 2
    assert all(p.country == "CZ" for p in result)


def test_filter_by_altitude():
    """
    Проверяет фильтрацию самолётов по диапазону высоты.
    """
    planes = [
        Aeroplane("A", "CZ", 200, 1000),
        Aeroplane("B", "CZ", 200, 5000),
        Aeroplane("C", "CZ", 200, 10000),
    ]

    result = AeroplaneService.filter_by_altitude(planes, 2000, 8000)

    assert len(result) == 1
    assert result[0].callsign == "B"


def test_sort_planes():
    """
    Проверяет сортировку самолётов по (altitude, velocity).
    """
    planes = [
        Aeroplane("A", "CZ", 100, 1000),
        Aeroplane("B", "CZ", 200, 5000),
        Aeroplane("C", "CZ", 150, 3000),
    ]

    result = AeroplaneService.sort_planes(planes)

    assert result[0].altitude == 5000
    assert result[-1].altitude == 1000


def test_top_n():
    """
    Проверяет возврат первых N элементов списка.
    """
    planes = [
        Aeroplane("A", "CZ", 100, 1000),
        Aeroplane("B", "CZ", 200, 2000),
        Aeroplane("C", "CZ", 300, 3000),
    ]

    result = AeroplaneService.top_n(planes, 2)

    assert len(result) == 2
    assert result[0].callsign == "A"
    assert result[1].callsign == "B"


@patch("src.user_console.AeroplanesAPI")
def test_user_interaction_mock(mock_api):
    """
    Проверяет user_interaction с использованием mock API.
    """

    mock_instance = Mock()
    mock_api.return_value = mock_instance

    # мок ответа API
    mock_instance.get_aeroplanes.return_value = [
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

    # имитируем ввод пользователя
    with patch(
        "builtins.input",
        side_effect=[
            "CZ",  # country
            "1",  # top_n
            "CZ DE",  # filters
            "0-10000",  # altitude range
        ],
    ):

        with patch("builtins.print") as mock_print:
            from src.user_console import user_interaction

            user_interaction()

            assert mock_print.called
