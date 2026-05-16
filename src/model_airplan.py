from functools import total_ordering


@total_ordering
class Aeroplane:
    """
    Модель самолёта.

    Атрибуты:
        callsign (str): позывной
        country (str): страна регистрации
        velocity (float): скорость (m/s из OpenSky)
        altitude (float): высота (m)
    """

    def __init__(self, callsign, country, velocity, altitude):
        self.callsign = callsign or "UNKNOWN"
        self.country = country or "UNKNOWN"
        self.velocity = float(velocity or 0.0)
        self.altitude = float(altitude or 0.0)

    @classmethod
    def cast_to_object_list(cls, raw_data):
        """
        Преобразует OpenSky states в список объектов Aeroplane.
        """
        result = []

        for item in raw_data:
            result.append(cls(
                callsign=item[1],
                country=item[2],
                velocity=item[9],
                altitude=item[13]
            ))

        return result

    # сравнение: сначала высота, потом скорость
    def __lt__(self, other):
        return (self.altitude, self.velocity) < (other.altitude, other.velocity)

    def __eq__(self, other):
        return (self.altitude, self.velocity) == (other.altitude, other.velocity)

    def __repr__(self):
        return f"{self.callsign} | {self.country} | {self.velocity:.1f} | {self.altitude:.1f}"
