use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::create_exception;
use pyo3::exceptions::PyException;

create_exception!(nusb, TransferError, PyException);
create_exception!(nusb.TransferError, Cancelled, TransferError);
create_exception!(nusb.TransferError, Stall, TransferError);
create_exception!(nusb.TransferError, Disconnected, TransferError);
create_exception!(nusb.TransferError, Fault, TransferError);
create_exception!(nusb.TransferError, Unknown, TransferError);

fn convert_error(err: ::nusb::transfer::TransferError) -> PyErr {
    match err {
        ::nusb::transfer::TransferError::Cancelled => Cancelled::new_err("Cancelled"),
        ::nusb::transfer::TransferError::Stall => Stall::new_err("Stall"),
        ::nusb::transfer::TransferError::Disconnected => Disconnected::new_err("Disconnected"),
        ::nusb::transfer::TransferError::Fault => Fault::new_err("Fault"),
        ::nusb::transfer::TransferError::Unknown => Unknown::new_err("Unknown"),
    }
}

#[pyclass]
struct ControlType(::nusb::transfer::ControlType);

#[pymethods]
impl ControlType {
    #[getter]
    fn name(&self) -> &str {
        match self.0 {
            ::nusb::transfer::ControlType::Standard => "Standard",
            ::nusb::transfer::ControlType::Class => "Class",
            ::nusb::transfer::ControlType::Vendor => "Vendor",
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Standard() -> ControlType {
        ControlType(::nusb::transfer::ControlType::Standard)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Class() -> ControlType {
        ControlType(::nusb::transfer::ControlType::Class)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Vendor() -> ControlType {
        ControlType(::nusb::transfer::ControlType::Vendor)
    }

    fn __str__(&self) -> String {
        format!("ControlType.{}", self.name())
    }
}

#[pyclass]
struct Recipient(::nusb::transfer::Recipient);

#[pymethods]
impl Recipient {
    #[getter]
    fn name(&self) -> &str {
        match self.0 {
            ::nusb::transfer::Recipient::Device => "Device",
            ::nusb::transfer::Recipient::Interface => "Interface",
            ::nusb::transfer::Recipient::Endpoint => "Endpoint",
            ::nusb::transfer::Recipient::Other => "Other",
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Device() -> Recipient {
        Recipient(::nusb::transfer::Recipient::Device)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Interface() -> Recipient {
        Recipient(::nusb::transfer::Recipient::Interface)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Endpoint() -> Recipient {
        Recipient(::nusb::transfer::Recipient::Endpoint)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Other() -> Recipient {
        Recipient(::nusb::transfer::Recipient::Other)
    }

    fn __str__(&self) -> String {
        format!("Recipient.{}", self.name())
    }
}

#[pyclass]
struct Speed(::nusb::Speed);

#[pymethods]
impl Speed {
    #[getter]
    fn name(&self) -> &str {
        match self.0 {
            ::nusb::Speed::Low => "Low",
            ::nusb::Speed::Full => "Full",
            ::nusb::Speed::High => "High",
            ::nusb::Speed::Super => "Super",
            ::nusb::Speed::SuperPlus => "SuperPlus",
            _ => "Unknown",
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Low() -> Speed {
        Speed(::nusb::Speed::Low)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Full() -> Speed {
        Speed(::nusb::Speed::Full)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn High() -> Speed {
        Speed(::nusb::Speed::High)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Super() -> Speed {
        Speed(::nusb::Speed::Super)
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn SuperPlus() -> Speed {
        Speed(::nusb::Speed::SuperPlus)
    }

    fn __eq__(&self, other: &Speed) -> bool {
        self.0 == other.0
    }

    fn __str__(&self) -> String {
        format!("Speed.{}", self.name())
    }
}

#[pyclass]
struct Device(::nusb::Device);

#[pymethods]
impl Device {
    fn control_in_blocking<'py>(
        &self,
        control_type: &ControlType,
        recipient: &Recipient,
        request: u8,
        value: u16,
        index: u16,
        length: usize,
        timeout: f64,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, PyBytes>> {
        let mut buf = vec![0u8; length];
        let length = py.allow_threads(|| self.0.control_in_blocking(
            ::nusb::transfer::Control {
                control_type: control_type.0,
                recipient: recipient.0,
                request,
                value,
                index,
            },
            buf.as_mut_slice(),
            ::std::time::Duration::from_secs_f64(timeout),
        )).map_err(convert_error)?;
        buf.truncate(length);
        Ok(PyBytes::new(py, &buf))
    }

    fn control_out_blocking(
        &self,
        control_type: &ControlType,
        recipient: &Recipient,
        request: u8,
        value: u16,
        index: u16,
        data: &[u8],
        timeout: f64,
        py: Python,
    ) -> PyResult<()> {
        py.allow_threads(|| self.0.control_out_blocking(
            ::nusb::transfer::Control {
                control_type: control_type.0,
                recipient: recipient.0,
                request,
                value,
                index,
            },
            data,
            ::std::time::Duration::from_secs_f64(timeout),
        )).map_err(convert_error)?;
        Ok(())
    }

    fn control_in<'py>(
        &self,
        control_type: &ControlType,
        recipient: &Recipient,
        request: u8,
        value: u16,
        index: u16,
        length: u16,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let device = self.0.clone();
        let control_type = control_type.0;
        let recipient = recipient.0;

        pyo3_async_runtimes::tokio::future_into_py(
            py,
            async move {
                let data = device.control_in(
                    ::nusb::transfer::ControlIn {
                        control_type: control_type,
                        recipient: recipient,
                        request,
                        value,
                        index,
                        length,
                    },
                ).await.into_result().map_err(convert_error)?;

                Python::with_gil(|py| Ok(PyBytes::new(py, &data).unbind()))
            },
        )
    }

    fn control_out<'py>(
        &self,
        control_type: &ControlType,
        recipient: &Recipient,
        request: u8,
        value: u16,
        index: u16,
        data: Vec<u8>,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let device = self.0.clone();
        let control_type = control_type.0;
        let recipient = recipient.0;

        pyo3_async_runtimes::tokio::future_into_py(
            py,
            async move {
                device.control_out(
                    ::nusb::transfer::ControlOut {
                        control_type: control_type,
                        recipient: recipient,
                        request,
                        value,
                        index,
                        data: &data,
                    },
                ).await.into_result().map_err(convert_error)?;
                Ok(())
            },
        )
    }

}

#[pyclass]
struct InterfaceInfo(::nusb::InterfaceInfo);

#[pymethods]
impl InterfaceInfo {
    #[getter]
    fn interface_number(&self) -> u8 {
        self.0.interface_number()
    }

    #[getter]
    fn class_(&self) -> u8 {
        self.0.class()
    }

    #[getter]
    fn subclass(&self) -> u8 {
        self.0.subclass()
    }

    #[getter]
    fn protocol(&self) -> u8 {
        self.0.protocol()
    }

    #[getter]
    fn interface_string(&self) -> Option<&str> {
        self.0.interface_string()
    }

    fn __repr__(&self) -> String {
        format!("<{:?}>", self.0)
    }
}

#[pyclass]
struct DeviceInfo(::nusb::DeviceInfo);

#[pymethods]
impl DeviceInfo {
    #[getter]
    fn bus_number(&self) -> u8 {
        self.0.bus_number()
    }

    #[getter]
    fn device_address(&self) -> u8 {
        self.0.device_address()
    }

    #[getter]
    fn vendor_id(&self) -> u16 {
        self.0.vendor_id()
    }

    #[getter]
    fn product_id(&self) -> u16 {
        self.0.product_id()
    }

    #[getter]
    fn device_version(&self) -> u16 {
        self.0.device_version()
    }

    #[getter]
    fn class_(&self) -> u8 {
        self.0.class()
    }

    #[getter]
    fn subclass(&self) -> u8 {
        self.0.subclass()
    }

    #[getter]
    fn protocol(&self) -> u8 {
        self.0.protocol()
    }

    #[getter]
    fn speed(&self) -> Option<Speed> {
        Some(Speed(self.0.speed()?))
    }

    #[getter]
    fn manufacturer_string(&self) -> Option<&str> {
        self.0.manufacturer_string()
    }

    #[getter]
    fn product_string(&self) -> Option<&str> {
        self.0.product_string()
    }

    #[getter]
    fn serial_number(&self) -> Option<&str> {
        self.0.serial_number()
    }

    #[getter]
    fn interfaces(&self) -> Vec<InterfaceInfo> {
        self.0.interfaces()
            .map(|info| InterfaceInfo(info.clone()))
            .collect::<Vec<_>>()
    }

    fn open(&self, py: Python) -> PyResult<Device> {
        let device = py.allow_threads(|| self.0.open());
        Ok(Device(device?))
    }

    fn __repr__(&self) -> String {
        format!("<{:?}>", self.0)
    }
}

#[pyfunction]
fn list_devices() -> PyResult<Vec<DeviceInfo>> {
    Ok(::nusb::list_devices()?.map(DeviceInfo).collect::<Vec<_>>())
}

#[pymodule]
fn nusb(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("TransferError", py.get_type::<TransferError>())?;
    let transfer_error = m.getattr("TransferError")?;
    transfer_error.setattr("Cancelled", py.get_type::<Cancelled>())?;
    transfer_error.setattr("Stall", py.get_type::<Stall>())?;
    transfer_error.setattr("Disconnected", py.get_type::<Disconnected>())?;
    transfer_error.setattr("Fault", py.get_type::<Fault>())?;
    transfer_error.setattr("Unknown", py.get_type::<Unknown>())?;

    m.add_class::<DeviceInfo>()?;
    m.add_class::<InterfaceInfo>()?;
    m.add_class::<Device>()?;
    m.add_class::<Speed>()?;
    m.add_class::<ControlType>()?;
    m.add_class::<Recipient>()?;

    m.add_function(wrap_pyfunction!(list_devices, m)?)?;

    Ok(())
}
