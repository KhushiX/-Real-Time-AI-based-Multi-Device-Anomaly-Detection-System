# ble_modules/ble_scan.py
import asyncio
from bleak import BleakScanner

def get_rssi(dev):
    # try a few common places where RSSI might be available
    r = getattr(dev, "rssi", None)
    if r is not None:
        return r
    # some bleak versions expose RSSI in metadata
    meta = getattr(dev, "metadata", None)
    if isinstance(meta, dict):
        # keys vary by platform/version
        for k in ("rssi", "RSSI"):
            if k in meta:
                return meta[k]
        # sometimes metadata['props'] or metadata['manufacturer_data'] can contain info, but skip for brevity
    # some versions have 'details'
    details = getattr(dev, "details", None)
    if isinstance(details, dict):
        for k in ("rssi", "RSSI"):
            if k in details:
                return details[k]
    return None

async def scan():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=6)
    for i, d in enumerate(devices):
        name = d.name or "<unknown>"
        addr = getattr(d, "address", str(d))
        rssi = get_rssi(d)
        rssi_str = f"RSSI={rssi}" if rssi is not None else "RSSI=<unknown>"
        print(f"{i}: {name} [{addr}] {rssi_str}")

if __name__ == "__main__":
    asyncio.run(scan())

