import pytest
import nusb

import enum
from random import Random
from facedancer import *

class Request(enum.IntEnum):
    ACK = enum.auto()
    STALL = enum.auto()
    RANDOM = enum.auto()

@use_inner_classes_automatically
class MockDevice(USBDevice):
    vendor_id            : int = 0x1209
    product_id           : int = 0x0008
    manufacturer_string  : str = "python-nusb"
    product_string       : str = "test usb device"
    serial_number_string : str = "12345"
    device_speed         : DeviceSpeed = DeviceSpeed.HIGH

    @vendor_request_handler()
    @to_device
    def out_test_handler(self, request: USBControlRequest):
        match request.number:
            case Request.ACK:
                request.ack()

            case Request.STALL:
                request.stall()

            case Request.RANDOM:
                match request.direction:
                    case USBDirection.IN:
                        request.reply(Random(request.value).randbytes(request.length))
                    case USBDirection.OUT:
                        assert request.data == Random(request.value).randbytes(request.length)
                        request.ack()

            case _:
                request.stall()

    class MyConfiguration(USBConfiguration):
        pass

class TestHitl:
    mock_device = MockDevice()

    async def test_metadata(self, device_info):
        assert device_info.vendor_id == self.mock_device.vendor_id
        assert device_info.product_id == self.mock_device.product_id
        assert device_info.manufacturer_string == self.mock_device.manufacturer_string.string
        assert device_info.product_string == self.mock_device.product_string.string
        assert device_info.serial_number == self.mock_device.serial_number_string.string
        assert device_info.speed == nusb.Speed.High

    async def test_device_control_out_blocking(self, device, run_in_executor):
        await run_in_executor(device.control_out_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.ACK, 0, 0, b'', 5)

        await run_in_executor(device.control_out_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.RANDOM, 1234, 0, Random(1234).randbytes(96), 5)

        with pytest.raises(nusb.TransferError.Stall):
            await run_in_executor(device.control_out_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.STALL, 0, 0, b'', 5)

    async def test_device_control_in_blocking(self, device, run_in_executor):
        assert await run_in_executor(device.control_in_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.ACK, 0, 0, 64, 5) == b''

        assert await run_in_executor(device.control_in_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.RANDOM, 1234, 0, 96, 5) == Random(1234).randbytes(96)

        with pytest.raises(nusb.TransferError.Stall):
            await run_in_executor(device.control_in_blocking, nusb.ControlType.Vendor, nusb.Recipient.Device, Request.STALL, 0, 0, 64, 5)

    async def test_device_control_out(self, device):
        await device.control_out(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.ACK, 0, 0, b'')

        await device.control_out(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.RANDOM, 1234, 0, Random(1234).randbytes(96))

        with pytest.raises(nusb.TransferError.Stall):
            await device.control_out(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.STALL, 0, 0, b'')

    async def test_device_control_in(self, device):
        assert await device.control_in(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.ACK, 0, 0, 64) == b''

        assert await device.control_in(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.RANDOM, 1234, 0, 96) == Random(1234).randbytes(96)

        with pytest.raises(nusb.TransferError.Stall):
            await device.control_in(nusb.ControlType.Vendor, nusb.Recipient.Device, Request.STALL, 0, 0, 64)
