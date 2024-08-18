from microHTMX.state import ReactiveComponent,ReactiveProperty
from microHTMX.base_elemets import H3
import machine
import asyncio


conversion_factor = 3.3 / 65535
def get_temp():
    reading = machine.ADC(4).read_u16() * conversion_factor
    return 27 - (reading - 0.706)/0.001721


class TemperatureDisplay(ReactiveComponent):
    _temp = ReactiveProperty(0)

    def __init__(self, interval=0.1) -> None:
        super().__init__()
        self.inteval= interval
        asyncio.create_task(self._update())


    async def _update(self):
        while True:
            self._temp = get_temp()
            await asyncio.sleep(self.inteval)

    def render(self):
        return H3(f"The Temperature is {self._temp:.2f}C")