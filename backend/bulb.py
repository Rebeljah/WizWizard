import pywizlight as pwz


class Bulb(pwz.wizlight):
    def __init__(self, ip, mac):
        super().__init__(ip=ip, mac=mac, connect_on_init=True)
