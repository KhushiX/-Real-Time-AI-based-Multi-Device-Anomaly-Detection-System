import asyncio
import time
import requests
import threading
from bleak import BleakClient, BleakScanner, BleakError

# ==========================
# 🔴 CHANGE ONLY THIS
# ==========================
API_URL = "http://192.168.149.182:8000/api/unified-activity/"  # Friend's API URL

# ==========================
# BLE UUIDs
# ==========================
HR_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

# ==========================
# GLOBAL BATTERY CACHE
# ==========================
last_battery = None

# ==========================
# SEND DATA (NON-BLOCKING)
# ==========================
def send_to_api(payload):
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )
        print("📡 API STATUS:", response.status_code)
        print("📡 API RESPONSE:", response.text)
    except Exception as e:
        print("❌ API SEND FAILED:", e)

# ==========================
# SCAN BLE DEVICES
# ==========================
async def scan_devices():
    print("🔍 Scanning BLE devices (5 seconds)...\n")
    devices = await BleakScanner.discover(timeout=5)

    if not devices:
        print("❌ No BLE devices found")
        return []

    for i, d in enumerate(devices):
        print(f"{i}. {d.name or 'Unknown Device'} | {d.address}")

    return devices

# ==========================
# SELECT DEVICE
# ==========================
def select_device(devices):
    while True:
        try:
            idx = int(input("\nSelect device number: "))
            return devices[idx].address
        except (ValueError, IndexError):
            print("❌ Invalid selection, try again")

# ==========================
# BATTERY UPDATER (SAFE)
# ==========================
async def battery_updater(client):
    global last_battery
    while True:
        try:
            data = await client.read_gatt_char(BATTERY_CHAR_UUID)
            last_battery = int(data[0])
            print(f"🔋 Battery updated: {last_battery}%")
        except Exception as e:
            print("⚠ Battery read failed:", e)
        await asyncio.sleep(30)

# ==========================
# STREAM & SEND DATA
# ==========================
async def stream_and_send(device_addr):
    global last_battery
    client = BleakClient(device_addr)

    async def hr_handler(sender, data):
        try:
            ts = time.time()

            # Correct HR parsing
            flags = data[0]
            if flags & 0x01:
                heart_rate = int.from_bytes(data[1:3], "little")
            else:
                heart_rate = data[1]

            payload = {
                "device_id": device_addr,   # MAC address
                "device_type": "watch",     # default value
                "heart_rate": heart_rate,
                "battery_level": last_battery,
                "timestamp": ts
            }

            print("➡ Sending payload:", payload)

            threading.Thread(
                target=send_to_api,
                args=(payload,),
                daemon=True
            ).start()

        except Exception as e:
            print("❌ HR handler error:", e)

    try:
        print(f"\n🔵 Connecting to {device_addr} ...")
        await client.connect()
        print("✅ Connected")

        # Start battery polling
        asyncio.create_task(battery_updater(client))

        # Start HR notifications
        await client.start_notify(HR_CHAR_UUID, hr_handler)
        print("📡 Streaming started (Ctrl+C to stop)\n")

        while True:
            await asyncio.sleep(1)

    except BleakError as e:
        print("BLE error:", e)

    finally:
        if client.is_connected:
            await client.disconnect()
            print("🔴 Disconnected")

# ==========================
# MAIN
# ==========================
async def main():
    devices = await scan_devices()
    if not devices:
        return

    device_addr = select_device(devices)
    await stream_and_send(device_addr)

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    asyncio.run(main())
