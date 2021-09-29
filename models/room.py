from models.light import Light


class Room:
    room_types = (
        'attic', 'balcony', 'bar', 'basement', 'bathroom', 'bedroom', 'corridor',
        'dining', 'dressing', 'entrance', 'garage', 'garden', "kid's room",
        'kitchen', 'living room', 'office', 'playroom', 'terrace', 'tv'
    )

    def __init__(self, room_name: str, room_type: str, room_id: str):
        self._id = room_id  # read only
        self.type: str = room_type
        self.name = room_name
        self.lights: list[Light] = []

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    def add_light(self, light: Light) -> None:
        self.lights.append(light)