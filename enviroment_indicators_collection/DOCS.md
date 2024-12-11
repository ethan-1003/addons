# Add-on Configuration Guide

This add-on allows you to collect data from various environmental sensors via the I2C protocol and send the data to Home Assistant or other applications using a Long-Lived Token. Below is a step-by-step guide to retrieve the required parameters and configure the add-on.

---

## 1. Select a Sensor

The add-on supports multiple sensor types. You only need to configure the one(s) you are using:

- **BMP180**: Pressure and temperature sensor.
- **BMP280**: Pressure and temperature sensor (enhanced version of BMP180).
- **SHT31**: Temperature and humidity sensor.
- **SHT45**: High-accuracy temperature and humidity sensor.
- **Oxygen (O2)**: Oxygen concentration sensor.

In the config.json file (or the add-on configuration section), specify the sensor you are using by setting the sensor_type parameter. Example:

json
{
  "bmp180": true,
  "sht31": false,
  "oxygen": true,
  "bmp280": false,
  "ssl": false,
  "sht45": true
}
