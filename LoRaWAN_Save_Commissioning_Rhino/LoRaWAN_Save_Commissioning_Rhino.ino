/* Save commissioning data to EEPROM for later reuse.
 *
 *  Please edit the keys below as they are just debugging samples.
 *    
 *    
 * This example code is in the public domain.
 */

#include "LoRaWAN.h"
#include "provisioning.h"
#include "EEPROM.h"
    
#define EEPROM_DATA_START_SETTINGS 0

struct calibrationData_t{
  uint8_t settings_byte;
  uint8_t dtc_value;
  float ads_calib;
}__attribute__((packed));


union calibrationPacket_t{
  calibrationData_t data;
  byte bytes[sizeof(calibrationData_t)];
};

calibrationPacket_t calibration_packet;

void setup( void ){

calibration_packet.data.settings_byte=0;
calibration_packet.data.dtc_value=0;
calibration_packet.data.ads_calib=0;
// DTC tuning
#ifdef DTC_VALUE
    calibration_packet.data.dtc_value=DTC_VALUE;
#endif //DTC_VALUE

// DTC tuning
#ifdef ADS_CALIB_VALUE
    calibration_packet.data.ads_calib=ADS_CALIB_VALUE;
#endif //DTC_VALUE

// write calibration to flash
for(int i=0;i<sizeof(calibrationData_t);i++){
    EEPROM.write(EEPROM_DATA_START_SETTINGS+i,calibration_packet.bytes[i]);
}

//OTAA
#ifdef OTAA
//const char *appEui  = "0101010101010101";
//const char *appKey  = "2B7E151628AED2A6ABF7158809CF4F3C";
//const char *devEui  = "0101010101010101";
//char devEui[32]; // read from the processor




    //LoRaWAN.getDevEui(devEui, 18);
    // OTAA
    LoRaWAN.setAppEui(appEui);
    LoRaWAN.setAppKey(appKey);
    LoRaWAN.setDevEui(devEui);
    const char *devAddr = "01010101";
    const char *nwkSKey = "01010101010101010101010101010101";
    const char *appSKey = "01010101010101010101010101010101";
    // clean ABP keys
    LoRaWAN.setDevAddr(devAddr);
    LoRaWAN.setNwkSKey(nwkSKey);
    LoRaWAN.setAppSKey(appSKey);
#endif

//ABP
#ifdef ABP

    // ABP
    LoRaWAN.setDevAddr(devAddr);
    LoRaWAN.setNwkSKey(nwkSKey);
    LoRaWAN.setAppSKey(appSKey);
    // clear OTAA keys
    const char *appEui  = "0101010101010101";
    const char *appKey  = "2B7E151628AED2A6ABF7158809CF4F3C";
    const char *devEui  = "0101010101010101";
    LoRaWAN.setAppEui(appEui);
    LoRaWAN.setAppKey(appKey);
    LoRaWAN.setDevEui(devEui);

#endif

}

void loop( void )
{
}
