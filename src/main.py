import server
import gc
import asyncio


async def gc_print():
    while True:
        gc.collect()
        print(gc.mem_free())
        
        await asyncio.sleep(1)

asyncio.create_task(gc_print())

server.run()

