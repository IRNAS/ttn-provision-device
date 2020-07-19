# config.yml file must be present, sample input
"""ttn-app:
   id: <ttn application id>
   key: <ttn application key> """

import time
#import ttn
import yaml
import binascii
import os
import base64
import argparse
import sys

### Command line argument parser
parser = argparse.ArgumentParser(description='Lorawan device provisioning tool!')
parser.add_argument("--name", default="", type=str,required=False, help="This is the device name")
parser.add_argument("--key", default="", type=str,required=False, help="This is ttn access key https://account.thethingsnetwork.org/users/authorize?client_id=ttnctl&redirect_uri=/oauth/callback/ttnctl&response_type=code")
parser.add_argument("--type", 
                    choices=["abp", "otaa"],
                    required=True, type=str, help="abp/otaa")
parser.add_argument("--dtc", default="0", type=str,required=False, help="DTC tuning value")

args = parser.parse_args()
activation_type = args.type
dtc_value=args.dtc

if activation_type == "abp":
    print("ABP")
elif activation_type == "otaa":
  print("OTAA")
else:
    print("undefined")

#dictionary to store all data
device_dict = {}

# load config file, to store keys separtely and not commit to git
with open("config.yml", 'r') as ymlfile:
    try:
        cfg = yaml.safe_load(ymlfile)
    except yaml.YAMLError as exc:
            print(exc)
f = open('log.txt', 'a')
f.write(str(time.time())+ " start" + "\r\n")
f.close()

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

device_name=args.name


while True:
    input_var = input("Enter device name to register or type a for automatic numbering: ")
    # TODO enable the name to be overwritten from cli
    if(input_var == "a"):
        device_name="auto"
    else:
        device_name=input_var #TODO: calidate device naming convention
    print("Device name selected: "+device_name)

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
    #determine the largest number of all
    maximum_id=0
    for item in ttnctl_device_list_devid:
        try:
            number=int(item.split("-")[-1])
            maximum_id=max(number,maximum_id)
        except:
            pass

    print(ttnctl_device_list)
    print(ttnctl_device_list_devid)
    print(maximum_id)

    if device_name in ttnctl_device_list:
        input_var = input("Device "+device_name+ " already registered, continue? [y/n] ")
        if(input_var == "y"):
            pass
        else:
            break

    device_id=""
    print("device_name: " + device_name)
    if device_name == "auto":
        # find the largest device id already registered and take the next one
        device_id="%s-%03d" % (app_id, maximum_id+1)
        print(device_id)

    else:
        device_id=device_name
    
    ttnctl_device_register = os.popen('ttnctl devices register '+device_id).read()
    print(ttnctl_device_register)
    #first register as OTAA, then provision to ABP if required
    # all of these is to parse outputs to variables
    input_string=""
    for line in ttnctl_device_register.splitlines():
        if "Registered device" in line:
            input_string=line
    input_string =  ' '.join(input_string.split())
    input_string_list = input_string.split(" ")

    AppKey=""
    DevEUI=""
    AppEUI=""
    for item in input_string_list:
        #print(item)
        if "AppKey" in item:
            AppKey=item.split("=")[1]
            #print(AppKey)
        elif "DevEUI" in item:
            DevEUI=item.split("=")[1]
            #print(DevEUI)
        elif "AppEUI" in item:
            AppEUI=item.split("=")[1]
            #print(AppEUI)
    # then write to .h file for compiling
    f = open("LoRaWAN_Save_Commissioning_Rhino/provisioning.h", "w")
    f.write("#define OTAA\n\r")
    f.write("#define DTC_VALUE "+dtc_value+"\n\r")
    f.write("const char *appKey = \""+AppKey+"\";\n\r")
    f.write("const char *devEui = \""+DevEUI+"\";\n\r")
    f.write("const char *appEui = \""+AppEUI+"\";\n\r")
    f.close()

            
    if activation_type == "abp":
        ttnctl_device_register_abp = os.popen('ttnctl devices personalize '+device_id).read()
        print(ttnctl_device_register_abp)
        input_string=""
        for line in ttnctl_device_register_abp.splitlines():
            #print("line "+ line)
            if "Personalized device" in line:
                input_string=line
                #print("input_string "+ input_string)

        if input_string == "":
            print("Key error")
            break
            
        input_string =  ' '.join(input_string.split())
        input_string_list = input_string.split(" ")

        AppSKey=""
        DevAddr=""
        NwkSKey=""
        for item in input_string_list:
            #print(item)
            if "AppSKey" in item:
                AppSKey=item.split("=")[1]
                #print(AppSKey)
            elif "DevAddr" in item:
                DevAddr=item.split("=")[1]
                #print(DevEUI)
            elif "NwkSKey" in item:
                NwkSKey=item.split("=")[1]
                #print(AppEUI)

        f = open("LoRaWAN_Save_Commissioning_Rhino/provisioning.h", "w")
        f.write("#define ABP\n\r")
        f.write("#define DTC_VALUE "+dtc_value+"\n\r")
        f.write("const char *devAddr = \""+DevAddr+"\";\n\r")
        f.write("const char *nwkSKey = \""+NwkSKey+"\";\n\r")
        f.write("const char *appSKey = \""+AppSKey+"\";\n\r")
        f.close()
    ### flas clear 
    device_output = os.popen(cfg["firmware"]["device_connect"]).read()
    if "STM32L07x/STM32L08x" in device_output:
        print("Device connected successful!")
    else:
        print("Device connection failed!")

    flash_output = os.popen(cfg["firmware"]["flash_erase"]).read()
    if "erased" in flash_output:
        print("Flash erase successful!")
    else:
        print("Flash erase failed!")

    eeprom_output = os.popen(cfg["firmware"]["eeprom_erase"]).read()
    if "erased" in eeprom_output:
        print("Eeprom erase successful!")
    else:
        print("Eeprom erase failed!")

    ### Provision the keys to the device
    compile_output = os.popen(cfg["firmware"]["compile_keys"]).read()
    if "Sketch uses" in compile_output:
        print("Compile successful!")
    else:
        print("Compile failed!")

    upload_output = os.popen(cfg["firmware"]["upload_keys"]).read()
    # this does not work because upload does not give the output to the variable
    '''if "Verified OK" in upload_output:
        print("Upload successful!")
    else:
        print("Upload failed!")'''
    #print(upload_output)

    time.sleep(1)

    ### Upload the firmware to the device

    upload_output = os.popen(cfg["firmware"]["upload_firmware"]).read()
