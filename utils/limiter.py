
import asyncio


class Limiter:
    def __init__(self, rate):
        self.wait_time = 1 / rate
        self.waiting = False

    async def wait(self):
        self.waiting = True
        await asyncio.sleep(self.wait_time)
        self.waiting = False
