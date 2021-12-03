
import asyncio


class Limiter:
    def __init__(self, actions_per_second):
        self.wait_time = 1 / actions_per_second
        self.waiting = False

    def wait(self):
        asyncio.create_task(self._lockout())

    async def _lockout(self):
        self.waiting = True
        await asyncio.sleep(self.wait_time)
        self.waiting = False
