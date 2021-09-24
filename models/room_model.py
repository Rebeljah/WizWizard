from models.light_model import Light


class Room:
    def __init__(self, room_name: str, room_id: str):
        self._id = room_id  # read only
        self.name = room_name
        self.lights: list[Light] = []

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    def add_light(self, light: Light) -> None:
        self.lights.append(light)
