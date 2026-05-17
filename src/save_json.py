import json
class BaseStorage:
    """
    Базовый класс для хранилищ.
    """

    def save(self, data):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError


class JSONSaver(BaseStorage):
    """
    Хранение самолётов в JSON.
    """

    def __init__(self, filename="planes.json"):
        self.filename = filename

    def add(self, airplane):
        data = self._load()
        data.append(airplane.__dict__)
        self._save(data)

    def delete(self, airplane):
        data = self._load()
        data = [a for a in data if a["callsign"] != airplane.callsign]
        self._save(data)

    def get(self):
        return self._load()

    # заглушка под БД
    def filter(self, **kwargs):
        return self._load()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
