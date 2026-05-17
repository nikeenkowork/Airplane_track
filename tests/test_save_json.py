import json
import os

import pytest

from src.save_json import JSONSaver


class FalsePlane:
    """
    Тестовый объект самолёта.

    Используется вместо реального Aeroplane,
    чтобы упростить проверку JSONSaver.
    """

    def __init__(self, callsign, country="Test", velocity=0, altitude=0):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude


@pytest.fixture
def storage(tmp_path):
    """
    Fixture создаёт временный JSONSaver с тестовым файлом.

    tmp_path — временная директория pytest.
    """
    file_path = tmp_path / "test_planes.json"
    return JSONSaver(filename=str(file_path))


def test_add(storage):
    """
    Тест проверяет добавление самолёта в JSON.

    Проверяется:
    - объект сохраняется
    - данные корректно записываются в файл
    """
    plane = FalsePlane("SU123")

    storage.add(plane)

    data = storage.get()

    assert len(data) == 1
    assert data[0]["callsign"] == "SU123"


def test_delete(storage):
    """
    Тест проверяет удаление самолёта по callsign.

    Проверяется:
    - объект добавляется
    - затем удаляется
    - в файле остаётся только нужный самолёт
    """
    plane1 = FalsePlane("SU123")
    plane2 = FalsePlane("LH777")

    storage.add(plane1)
    storage.add(plane2)

    storage.delete(plane1)

    data = storage.get()

    assert len(data) == 1
    assert data[0]["callsign"] == "LH777"


def test_get(storage):
    """
    Тест проверяет получение всех данных из JSON.

    Проверяется:
    - метод возвращает список
    - данные корректно сохраняются и читаются
    """
    plane = FalsePlane("A1")

    storage.add(plane)

    data = storage.get()

    assert isinstance(data, list)
    assert len(data) == 1


def test_filter(storage):
    """
    Тест проверяет метод filter (сейчас это заглушка).

    Ожидаемое поведение:
    - метод возвращает все данные без фильтрации
    """
    plane = FalsePlane("X1")

    storage.add(plane)

    data = storage.filter(country="Any")

    assert len(data) == 1


def test_file_created(storage):
    """
    Тест проверяет создание JSON-файла.

    Проверяется:
    - файл создаётся после добавления данных
    - содержимое файла корректное
    """
    plane = FalsePlane("TEST")

    storage.add(plane)

    assert os.path.exists(storage.filename)

    with open(storage.filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data[0]["callsign"] == "TEST"
