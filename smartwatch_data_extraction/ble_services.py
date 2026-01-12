# ble_modules/ble_services.py
import asyncio
import sys
import traceback
from bleak import BleakClient

async def show_services(address, timeout=10):
    print("Connecting to", address, "...")
    client = BleakClient(address, timeout=timeout)
    try:
        await client.connect()

        # is_connected: may be coroutine or property depending on bleak version
        try:
            connected = await client.is_connected() if callable(getattr(client, "is_connected", None)) else client.is_connected
        except TypeError:
            # some versions expose it as property
            connected = client.is_connected

        print("Connected ->", connected)

        # get services: prefer method, fallback to property
        services = None
        if callable(getattr(client, "get_services", None)):
            try:
                services = await client.get_services()
            except TypeError:
                # maybe get_services is synchronous (rare)
                services = client.get_services()
        else:
            # try attribute
            services = getattr(client, "services", None)

        if services is None:
            print("Could not enumerate services (services is None).")
            return

        print("Services for", address)
        for s in services:
            print(f"- Service {s.uuid} ({getattr(s, 'description', '')})")
            for c in s.characteristics:
                print(f"   CHAR {c.uuid} | props: {c.properties}")

    except Exception as e:
        print("Error while connecting/enumerating services:", type(e).__name__, e)
        traceback.print_exc()
    finally:
        try:
            if client and (callable(getattr(client, "is_connected", None)) and await client.is_connected() or getattr(client, "is_connected", False)):
                await client.disconnect()
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ble_modules/ble_services.py <DEVICE_ADDRESS>")
        sys.exit(1)
    asyncio.run(show_services(sys.argv[1]))
