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

void setup( void ){

// DTC tuning
#ifdef DTC_VALUE
    EEPROM.write(EEPROM_DATA_START_SETTINGS+1,DTC_VALUE);
#endif //DTC_VALUE

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
