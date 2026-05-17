from abstract_API import AeroplanesAPI
from model_airplan import Aeroplane


class AeroplaneService:
    """
    Сервисный класс для обработки и анализа данных о самолётах.

    Предоставляет методы для:
    - преобразования сырых данных в объекты самолётов;
    - фильтрации самолётов по стране и высоте полёта;
    - сортировки списка самолётов;
    - получения первых N элементов из отсортированного списка.

    Все методы реализованы как статические и не требуют создания экземпляра класса.
    """

    @staticmethod
    def to_objects(raw):
        """
        Преобразует сырые данные в список объектов Aeroplane.

        :param raw: исходные данные о самолётах
        :return: список объектов Aeroplane
        """
        return Aeroplane.cast_to_object_list(raw)

    @staticmethod
    def filter_by_country(planes, countries):
        """
        Фильтрует самолёты по странам.

        :param planes: список объектов Aeroplane
        :param countries: список или множество стран
        :return: список самолётов, принадлежащих указанным странам
        """
        return [p for p in planes if p.country in countries]

    @staticmethod
    def filter_by_altitude(planes, min_alt, max_alt):
        """
        Фильтрует самолёты по диапазону высоты полёта.

        :param planes: список объектов Aeroplane
        :param min_alt: минимальная высота
        :param max_alt: максимальная высота
        :return: список самолётов в заданном диапазоне высот
        """
        return [p for p in planes if min_alt <= p.altitude <= max_alt]

    @staticmethod
    def sort_planes(planes):
        """
        Сортирует самолёты в обратном порядке.

        :param planes: список объектов Aeroplane
        :return: отсортированный список самолётов
        """
        return sorted(planes, reverse=True)

    @staticmethod
    def top_n(planes, n):
        """
        Возвращает первые N самолётов из списка.

        :param planes: список объектов Aeroplane
        :param n: количество элементов
        :return: список из первых N самолётов
        """
        return planes[:n]


def user_interaction():
    """
    Консольный интерфейс пользователя.
    """

    api = AeroplanesAPI()

    country = input("Страна: ")
    top_n = int(input("Top N: "))
    filters = input("Страны регистрации: ").split()
    alt_range = input("Диапазон высоты min-max: ")

    min_alt, max_alt = map(int, alt_range.split("-"))

    raw = api.get_aeroplanes(country)
    planes = AeroplaneService.to_objects(raw)

    planes = AeroplaneService.filter_by_country(planes, filters)
    planes = AeroplaneService.filter_by_altitude(planes, min_alt, max_alt)

    planes = AeroplaneService.sort_planes(planes)
    planes = AeroplaneService.top_n(planes, top_n)

    for p in planes:
        print(p)


if __name__ == "__main__":
    user_interaction()
