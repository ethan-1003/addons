# Add-on Configuration Guide

This add-on allows you to collect data from various environmental sensors via the I2C protocol and send the data to Home Assistant or other applications using a Long-Lived Token. Below is a step-by-step guide to retrieve the required parameters and configure the add-on.

---

## 1. Retrieve a Long-Lived Access Token from Home Assistant

A **Long-Lived Access Token** allows the add-on to interact with Home Assistant without needing repeated logins.

1. Open the Home Assistant UI.
2. Navigate to your **Profile** by clicking your user name in the bottom-left corner or visiting `http://<your_base_url>/profile`.
3. In the **Security** section, scroll down to the bottom.
4. Click **Create Token**.
5. Enter a name for the token (e.g., "Addon Sensor Integration") and click **OK**.
6. **Important**: The token will only appear once. Copy and save it securely. You will need this token for the add-on configuration.

---

## 2. Retrieve the `base_url` for Home Assistant

The `base_url` is the address used to access your Home Assistant instance, including the protocol, IP/domain, and port.

- If you access Home Assistant via a domain or IP address, the `base_url` is the URL you use in your browser. Examples:
  - `http://homeassistant.local:8123/api/states`
  - `http://192.168.1.10:8123/api/states`
  - `https://my-home.duckdns.org/api/states`
  
Make sure to include the correct protocol (`http` or `https`) and the port (default is 8123).

---

## 3. Select a Sensor

The add-on supports multiple sensor types. You only need to configure the one(s) you are using:

- **BMP180**: Pressure and temperature sensor.
- **BMP280**: Pressure and temperature sensor (enhanced version of BMP180).
- **SHT31**: Temperature and humidity sensor.
- **SHT45**: High-accuracy temperature and humidity sensor.
- **Oxygen (O2)**: Oxygen concentration sensor.

In the `config.json` file (or the add-on configuration section), specify the sensor you are using by setting the `sensor_type` parameter. Example:

```json
{
  "sensor_type": "bmp280"
}

