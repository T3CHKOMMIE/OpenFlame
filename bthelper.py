import asyncio
from bleak import BleakScanner

async def scan_for_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print("Device Name: "+str(device.name))
        print("Device Address: "+str(device.address))

if __name__ == "__main__":
    asyncio.run(scan_for_devices())