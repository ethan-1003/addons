# Home Assistant Add-on: Sensor Integration

This Home Assistant add-on allows you to collect and monitor environmental data from multiple I2C sensors, including:

- **BMP180**: Pressure and temperature.
- **BMP280**: Enhanced pressure and temperature.
- **SHT31**: Temperature and humidity.
- **SHT45**: High-accuracy temperature and humidity.
- **Oxygen (O2)**: Oxygen concentration.

The add-on sends sensor data to Home Assistant using a secure API connection.

---

## Features

- Easy integration with Home Assistant.
- Support for multiple I2C sensors.
- Configurable I2C address for each sensor.
- Sends real-time data to Home Assistant.

---

## Installation

1. Add the repository to your Home Assistant Add-on Store.
2. Install the add-on and start it.
3. Configure the add-on with your Home Assistant `base_url`, `long_lived_token`, sensor type, and I2C address.

---

## Configuration

Example `config.json`:

```json
{
  "base_url": "http://192.168.1.10:8123",
  "long_lived_token": "your-long-lived-token",
  "sensor_type": "bmp280",
  "i2c_address": "0x76"
}

