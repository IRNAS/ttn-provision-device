# config.yml file must be present, sample input
"""ttn-app:
   id: <ttn application id>
   key: <ttn application key> """

import yaml
import os
import argparse
import sys
import json


def parse_device_info(string):
    # keys and table headers to populate
    keys = ["Device ID","Last Seen","AppEUI","DevEUI","DevAddr","AppKey","AppSKey","NwkSKey","FCntUp","FCntDown","Options"]
    device_info={}
    for line in string.splitlines():
        # reject INFO lines
        if "INFO" in line:
            continue
        # merge spaces
        parse_line =  ' '.join(line.split())
        # check if any of the keys present in this line
        for item in keys:
            if item in parse_line:
                device_info[item]=parse_line[parse_line.find(": ")+2:]
    return device_info

def parse_devices_list():
    ttnctl_device_list = os.popen('ttnctl devices list').read()
    # get a list of parsed device ids
    ttnctl_device_list_devid=[]
    for line in ttnctl_device_list.splitlines():
        if "DevID"in line:
            pass
        elif "INFO"in line:
            pass
        else:
            line_split =  ' '.join(line.split())
            line_split = line_split.split(" ")
            if line_split[0] is not '':
                ttnctl_device_list_devid.append(line_split[0])
    return ttnctl_device_list_devid

### Command line argument parser
parser = argparse.ArgumentParser(description='Lorawan device credential fetch tool!')
parser.add_argument("--name", default="credentials.json", type=str,required=False, help="Filename of where storing csv")

args = parser.parse_args()


#dictionary to store all data
device_dict = {}

# load config file, to store keys separtely and not commit to git
with open("config.yml", 'r') as ymlfile:
    try:
        cfg = yaml.safe_load(ymlfile)
    except yaml.YAMLError as exc:
            print(exc)

# get the keys to a variable
app_id=cfg["ttn-app"]["id"]

### Make sure user is logged in
ttnctl_user_login = os.popen('ttnctl user').read()
if "FATAL" in ttnctl_user_login:
    ttnctl_user_login_now=os.popen('ttnctl user login '+args.key).read()
    if "experied" in ttnctl_user_login_now:
      print("Key is expired")
    elif "FATAL" in ttnctl_user_login_now:
      print("User not logged in, provide the access key")
else:
    print("Logged in!")


ttnctl_application_select = os.popen('ttnctl applications select '+app_id).read()
print(ttnctl_application_select)

# Get the list of devices
ttnctl_device_list_devid = parse_devices_list()

devices_info=[]

# fetch info for every device
for device in ttnctl_device_list_devid:
    device_info_string= os.popen('ttnctl devices info '+device).read()
    device_info=parse_device_info(device_info_string)
    devices_info.append(device_info)
    print("Reading device info: " + device)

# store
f = open(args.name, "w")
f.write(json.dumps(devices_info, sort_keys=False, indent=4))
f.close()

print("Done")


