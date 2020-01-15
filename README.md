# ttn-provision-device
Simple script to read data from TheThingsNetwork and provision OTAA and ABP devices.

## Key features (TODO):
1. Accept command line arguments for `device-name`, `otaa/abp`, `deveui`
1. Load the list of already registered devices
1. Notify if device exists already
1. Fetch keys for the device
1. Provision the keys to file or directly upload firmware to the device

## Setup
Download this repository. Set up the environment, recommended to use python virtual environment `pip install virtualenv`.

```
git clone https://github.com/SloMusti/ttn-signal-test-python
cd ttn-signal-test-python
python3 -m venv ./env
source env/bin/activate
pip install -r requirements.txt
```

## Prepare config
Create the config file `config.yaml` with the following structure, you can have multiple TTN applications defined, data will be shown for all nodes sending on those applications.
```
ttn-app:
  id: <ttn application id>
firmware:
  compile_keys: arduino-cli compile --fqbn TleraCorp:stm32l0:IRNAS-env-module-L072Z LoRaWAN_Save_Commissioning_Rhino
  upload_keys: arduino-cli upload -p /dev/ttyACM0 --fqbn TleraCorp:stm32l0:IRNAS-env-module-L072Z LoRaWAN_Save_Commissioning_Rhino
  upload_firmware: arduino-cli upload -p /dev/ttyACM0 --fqbn TleraCorp:stm32l0:IRNAS-env-module-L072Z -i board.cpp.dfu
```

## Run the application
Run the application within the active virtual environment with `python main.py` and expect a similar output to:
