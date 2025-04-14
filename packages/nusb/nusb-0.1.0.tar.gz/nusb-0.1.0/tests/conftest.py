import pytest
import asyncio
from facedancer import USBDevice

import nusb

@pytest.fixture(scope = 'class')
def run_in_executor():
    '''Return a function that runs a blocking function in an executor.'''

    return lambda func, *args: asyncio.get_event_loop().run_in_executor(None, func, *args)

def find_devices(device_type):
    return [info for info in nusb.list_devices() if info.vendor_id == device_type.vendor_id and info.product_id == device_type.product_id]

@pytest.fixture(scope = 'class')
async def device_info(request):
    '''Start a mock device, wait for it to enumerate and return the corresponding nusb.DeviceInfo object.'''

    assert hasattr(request.cls, 'mock_device'), 'Test class must have a mock_device attribute'
    mock_device = request.cls.mock_device
    assert isinstance(request.cls.mock_device, USBDevice), 'mock_device attribute must be a USBDevice instance'

    assert len(find_devices(mock_device)) == 0, 'Found existing device before starting mock device, please check test setup'

    mock_device.connect()
    try:
        device_task = asyncio.create_task(mock_device.run())
        try:
            # Wait for the device to be enumerated by the host.
            while mock_device.configuration is None:
                await asyncio.sleep(0.1) # TODO: timeout

            # Wait for the host to list the device.
            await asyncio.sleep(0.5) # TODO: retry with timeout
            devices = find_devices(mock_device)
            assert len(devices) == 1

            yield devices[0]

        finally:
            device_task.cancel()
    finally:
        mock_device.disconnect()

        # Wait for the device to be removed from the system.
        await asyncio.sleep(0.5) # TODO: retry with timeout
        assert len(find_devices(mock_device)) == 0, 'Mock device not removed from system after disconnecting, please check test setup'

@pytest.fixture(scope = 'class')
async def device(device_info, run_in_executor):
    '''Return an nusb.Device object for the current mock device.'''

    return await run_in_executor(device_info.open)
