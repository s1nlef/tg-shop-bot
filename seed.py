from app.database.models import async_main, async_session
from app.database.models import Game
from sqlalchemy import select
from datetime import date
import asyncio

async def main():
    await async_main()
    async with async_session() as session:
        new_games = [Game(name="Factorio", genre="Simulation, Strategy, Indie, Automation", daterelease=date(2020, 8, 14), description='Players control an engineer who crash-lands on an alien planet, aiming to harvest resources, build complex automated factories, and eventually launch a rocket. The game features a "no sale" policy and is known for its high replayability.', price=15),
            Game(name="Dishonored", genre="Action-adventure, stealth, immersive sim", daterelease=date(2012, 10, 9), description="Set in the plague-ridden whaling city of Dunwall, you play as Corvo Attano, the former Royal Protector framed for the assassination of the Empress. Armed with a supernatural arsenal, gadgets, and weapons, you must eliminate targets, choosing either a non-lethal stealth approach or a violent, high-chaos path.", price=10),
            Game(name="Mortal Kombat 1", genre="Fighting", daterelease=date(2023, 9, 19), description='Mortal Kombat 1 is the twelfth main installment, taking place in a "New Era" timeline created by Fire God Liu Kang after the events of Mortal Kombat 11: Aftermath. The gameplay features a revamped story, new combat mechanics, and a "Kameo" system that allows players to bring a partner fighter into combat. It features a large roster of reimagined characters and extensive online functionality, including cross-platform play.', price=70)]

        session.add_all(new_games)
        await session.commit()

asyncio.run(main())


# Factorio	Simulation, Strategy, Indie, Automation.	August 14, 2020	Players control an engineer who crash-lands on an alien planet, aiming to harvest resources, build complex automated factories, and eventually launch a rocket. The game features a "no sale" policy and is known for its high replayability. 15
# Dishonored	Action-adventure, stealth, immersive sim.	October 9, 2012	Set in the plague-ridden whaling city of Dunwall, you play as Corvo Attano, the former Royal Protector framed for the assassination of the Empress. Armed with a supernatural arsenal, gadgets, and weapons, you must eliminate targets, choosing either a non-lethal stealth approach or a violent, high-chaos path.	10
# Mortal Kombat 1	Fighting	September 19, 2023	Mortal Kombat 1 is the twelfth main installment, taking place in a "New Era" timeline created by Fire God Liu Kang after the events of Mortal Kombat 11: Aftermath. The gameplay features a revamped story, new combat mechanics, and a "Kameo" system that allows players to bring a partner fighter into combat. It features a large roster of reimagined characters and extensive online functionality, including cross-platform play.	70
