from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для работы с внешними авиационными API.

    Определяет интерфейс для получения координат стран и данных о самолётах.
    """

    @abstractmethod
    def get_country_coords(self, country: str):
        """
        Получает географические координаты страны.

        :param country: Название страны
        :return: (latitude, longitude) или None, если страна не найдена
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str):
        """
        Получает список самолётов, находящихся над указанной страной.

        :param country: Название страны
        :return: список сырых данных о самолётах
        """
        pass


class AeroplanesAPI(BaseAPI):
    """
    Реализация API для получения:
    - координат страны через Nominatim (OpenStreetMap)
    - данных о самолётах через OpenSky Network
    """

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def get_country_coords(self, country: str):
        """
        Получает координаты страны через Nominatim API.

        :param country: Название страны
        :return: tuple (lat, lon) или None
        """
        params = {
            "q": country,
            "format": "json",
            "limit": 1
        }

        response = requests.get(
            self.NOMINATIM_URL,
            params=params,
            headers={"User-Agent": "aeroplanes-app"}
        )

        data = response.json()

        if not data:
            return None

        return float(data[0]["lat"]), float(data[0]["lon"])

    def get_aeroplanes(self, country: str):
        """
        Получает список самолётов в воздушном пространстве страны.

        Использует координаты страны для формирования зоны запроса OpenSky API.

        :param country: Название страны
        :return: список самолётов (raw OpenSky states)
        """
        coords = self.get_country_coords(country)

        if not coords:
            return []

        lat, lon = coords

        # создаём "bounding box" вокруг страны
        lamin, lamax = lat - 5, lat + 5
        lomin, lomax = lon - 5, lon + 5

        params = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax
        }

        response = requests.get(self.OPENSKY_URL, params=params)
        data = response.json()

        return data.get("states", [])
