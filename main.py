import asyncio
from arena import Game


async def main():
    game = Game()
    await game.run()


asyncio.run(main())
