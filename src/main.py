import server
import gc
import asyncio


async def gc_print():
    while True:
        gc.collect()
        
        await asyncio.sleep(1)

asyncio.create_task(gc_print())


server.run()

