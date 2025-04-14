# LED Controller API Wrapper

used to communicate with different LED-Controllers via TCP to read and set the overall brightness.

## Example Usage

```python
import asyncio
from ledwallcontroller import Multivision, TCPHandler, OnlyGlass


async def main():
    conn1 = TCPHandler(host="192.168.20.197", port=4010)
    mv = Multivision(conn1, controller_id=1)
    await mv.set_brightness_percent(98)
    await mv.update()

    print(f"Multivision 1 brightness: {mv.brightness_percent}")

    mv2 = Multivision(conn1, controller_id=2)
    await mv2.set_brightness_percent(98)
    await mv2.update()

    print(f"Multivision 2 brightness: {mv2.brightness_percent}")

    conn2 = TCPHandler(host="192.168.20.197", port=4001)
    og = OnlyGlass(conn2)
    await og.set_brightness_percent(50)
    await og.update()

    print(f"OnlyGlass brightness: {og.brightness_percent}")


asyncio.run(main())
```


## Example Communication for Multivision

Sending an ASCII-encoded String via TCP

### Setting Values

Set Brightness to 75%

```
SOH L E D S B R I G H 0 1 = 7 5 CR
```

-> No return

### Getting Values

Get current Brightnesss

```
SOH L E D G B R I G H 0 1 = ? CR
```

->

```
SOH L E D R B R I G H 0 1 = 7 5 CR
```

Brightness 75%
