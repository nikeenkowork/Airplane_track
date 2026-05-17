from unittest.mock import Mock, patch

from src.abstract_API import AeroplanesAPI


class TestAeroplanesAPI:
    """
    Набор тестов для класса AeroplanesAPI.
    """

    @patch("src.abstract_API.requests.get")
    def test_get_country_coords_success(self, mock_get):
        """
        Проверяет успешное получение координат страны.

        Ожидается:
        - API возвращает координаты
        - метод преобразует их в tuple(float, float)
        """
        mock_response = Mock()
        mock_response.json.return_value = [{"lat": "52.52", "lon": "13.405"}]

        mock_get.return_value = mock_response

        api = AeroplanesAPI()

        result = api.get_country_coords("Germany")

        assert result == (52.52, 13.405)

    @patch("src.abstract_API.requests.get")
    def test_get_country_coords_not_found(self, mock_get):
        """
        Проверяет случай, когда страна не найдена.

        Ожидается:
        - API возвращает пустой список
        - метод возвращает None
        """
        mock_response = Mock()
        mock_response.json.return_value = []

        mock_get.return_value = mock_response

        api = AeroplanesAPI()

        result = api.get_country_coords("Unknown")

        assert result is None

    @patch("src.abstract_API.requests.get")
    def test_get_aeroplanes_success(self, mock_get):
        """
        Проверяет успешное получение списка самолётов.

        Ожидается:
        - сначала получаются координаты страны
        - затем выполняется запрос в OpenSky API
        - метод возвращает список states
        """
        coords_response = Mock()
        coords_response.json.return_value = [{"lat": "50.0", "lon": "10.0"}]

        planes_response = Mock()
        planes_response.json.return_value = {"states": [["plane1"], ["plane2"]]}

        mock_get.side_effect = [coords_response, planes_response]

        api = AeroplanesAPI()

        result = api.get_aeroplanes("Germany")

        assert result == [["plane1"], ["plane2"]]

    @patch("src.abstract_API.requests.get")
    def test_get_aeroplanes_no_coords(self, mock_get):
        """
        Проверяет поведение при отсутствии координат страны.

        Ожидается:
        - get_country_coords возвращает None
        - запрос к OpenSky API не выполняется
        - метод возвращает пустой список
        """
        mock_response = Mock()
        mock_response.json.return_value = []

        mock_get.return_value = mock_response

        api = AeroplanesAPI()

        result = api.get_aeroplanes("Unknown")

        assert result == []

    @patch("src.abstract_API.requests.get")
    def test_get_country_coords_request_error(self, mock_get):
        """
        Проверяет обработку ошибки сетевого запроса.

        Ожидается:
        - requests.get вызывает исключение
        - исключение пробрасывается дальше
        """
        mock_get.side_effect = Exception("Network error")

        api = AeroplanesAPI()

        try:
            api.get_country_coords("Germany")
        except Exception as error:
            assert str(error) == "Network error"
