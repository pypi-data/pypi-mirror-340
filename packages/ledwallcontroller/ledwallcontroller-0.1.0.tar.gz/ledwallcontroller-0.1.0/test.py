import asyncio
from ledwallcontroller import Multivision, TCPHandler, OnlyGlass


async def main():
    conn1 = TCPHandler(host="192.168.20.197", port=4010)
    mv = Multivision(conn1, controller_id=1)
    # await mv.set_brightness_percent(98)
    await mv.update()

    print(f"Multivision brightness: {mv.brightness_percent}")

    mv2 = Multivision(conn1, controller_id=2)
    await mv2.set_brightness_percent(98)
    await mv2.update()

    print(f"Multivision brightness: {mv2.brightness_percent}")

    conn2 = TCPHandler(host="192.168.20.197", port=4001)
    og = OnlyGlass(conn2)
    await og.set_brightness_percent(50)
    await og.update()

    print(f"OnlyGlass brightness: {og.brightness_percent}")


asyncio.run(main())
