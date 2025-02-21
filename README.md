# DFRobot mmWave Radar (dfrobot_sen0395)
#### This repository seeks to address the breaking change in esphome 2025.2 where the ability to use custom components, in this case mmWave sensors, were removed causing the typical use of most ESP MCU based mmWave modules to fail update in ESPHome Device Builder. There has been a built-in component (dfrobot_sen0395) to work with the sensor but it has some fairly odd limitations and odd behaviors with how you interact and control the module plus seemingly no way to read settings even though it does use UART... so instead I've made a bit of a hybrid test here that still uses simple UART messages to send configuration and diagnostic commands to the DFRobot radar module, but since reading back messages requires elements of the custom component which is now not possible without refactoring or finding a true "External Component" we simply forego reading the settings from the module and instead store the last updated setting in the ESP MCU flash-and restore them to the device card/web portal upon power up or reboot of the MCU. The settings themselves aren't lost once set, but if you have played with the ESPHome built-in dfrobot_sen0395 component or looked at it's underlying code, you've no doubt noticed it has no get- method only set-. Once set they persist but you have no way using this built-in component to "see" they are set, the swtiches, sliders, and numbers boxes default to blank/zero/off.

The change notes from ESPHome:
https://esphome.io/guides/contributing#a-note-about-custom-components

The (very limited) built-in component for the dfrobot_sen0395 module
https://github.com/esphome/esphome/tree/dev/esphome/components/dfrobot_sen0395

This is a working example of one of my units that I've applied this change to and am testing to see how it works over time:
  https://github.com/DuncanIdahoCT/espresence-occupancy-nightlight-multi-sensor

The installation below is largely the same as previous projects I've posted here. The notable changes are in the yaml files:

  
  Removal of the entire custom component:
  ```
  sensor:      
  - platform: custom
    lambda: |-
      auto s = new leapmmw(id(uart_bus));
      App.register_component(s);
      return {};
    sensors:
  ```
 Elimination of include.h (CPP) code file dependency and removal of all leapmmw(getmmwConf) app references:
```
leapmmw(id(uart_bus)).getmmwConf("getRange");
leapmmw(id(uart_bus)).getmmwConf("getLatency");
leapmmw(id(uart_bus)).getmmwConf("getSensitivity");
leapmmw(id(uart_bus)).getmmwConf("getLedMode 1");
```
 Usage of global flash variables to allow settings to persist after reboot:
```
globals: #such as...

# distance
  - id: distance_flash
    type: float
    restore_value: true
    #initial_value: '9.45'
```

Technically, settings are set just fine using the built-in component dfrobot_sen0395 but I find it's odd limitations to be... limiting lol so I just use the tried and trusted - uart.write: method but to make it clear what settings a unit has, the global flash stow and restore functions come in quite handy

You'll also notice that the led switch never really worked well in previous iterations, so I've changed it to also use a global flash option. On reboot the switch position will be saved and restored via global custom flash attribute.

As documented, some switches don't behave correctly during reboot and so the native flash save for switch position is disabled via:
```
restore_mode: DISABLED
```

### Installation:
 * Download the file and copy them (keeping their subfolder paths) into your Home Assistant config/esphome main folder:

   ```
   ** header/leapmmw_sensor.h ** - no longer needed due to removal of the custom component
   
   packages/leapmmw_sensor.yml
   ```
 
 * In Home Assistant add-on, click ESPHome>open web gui and create a new device choosing the "continue" option and give it a name such as:

   ```
   espresence-occupancy-nightlight-multi-sensor
   ```

* Click next and choose the type of ESP module you used in your build, this isn't a critical thing to have match but as long as it's some kind of ESP32 you can just select that for now and click next.
* You'll see a new card appear in the background for your ESP device, this is just an empty shell with only basic initialization code so far... click skip because you don't want to install this basic code to the ESP quite yet.
* Now click edit on your new sensor in ESPHome and you'll see the basic code:
   ```
   esphome:
    name: espresence-occupancy-nightlight-multi-sensor

   esp32:
    board: esp32dev
    framework:
      type: arduino

   # Enable logging
   logger:

   # Enable Home Assistant API
   api:
     encryption:
       key: "your-key-here"

   ota:
     password: "your-password-here"

   wifi:
    ssid: !secret wifi_ssid
    password: !secret wifi_password

     # Enable fallback hotspot (captive portal) in case wifi connection fails
    ap:
      ssid: "Your-New-Esp-Multi-Sensor"
     password: "wifipass"

   captive_portal:
   ```

* The easiest way to proceed is to copy all the code above out to notepad++ or your favorite editor and then paste back in the entire code from:
   ```
   espresence-occupancy-nightlight-multi-sensor.yaml
   ```
* Now just copy some key lines you saved from your new basic config and paste them into the relevant sections of the full config:

   ```
   substitutions:
      # change device name to match your desired name
      device_name: espresence-occupancy-nightlight-multi-sensor
      # change sensor name below to the one you want to see in Home Assistant
      device_name_pretty: ESpresence Occupancy Night Light Multi-Sensor
      # change room name below to the one you want to see in Home Assistant
      room: "Bathroom"
   ```
* The room: "name" is key as it will be the name of each sensor object in HA so if you choose "Office" here, your sensors will be Office Motion, Office Temperature, etc...

* You'll also want to copy the generated api encryption key and ota password into this section of the full code:

   ```
   # Enable Home Assistant API
   api:
      encryption:
         key: "assigned_when_you_add_to_esphome"

   ota:
      password: "assigned_when_you_add_to_esphome"
   ```

* Lastly, in the wifi: section, there is a line that says "use_address: XXX.XXX.XXX.XXX" this is an optional element to work around typical issues with mDNS and wifi/subnets. Basically, if you find your device is always showing as offline in ESPHome or has any issues at all when making changes or updating OTA, you'll want this setting. Note: this is not a static IP, it just tells ESPHome to use an IP address to do all OTA work with a given ESP device. You can of course set a static IP but this isn't that. You'll also notice that the wifi ssid and passwords are variables, you'll also see at the top of the full config are references to "secrets" file. You'll need to create one or update the one in this repo and copy it to the config/esphome main folder... if you have setup other esp devices, changes are you have this already.

   ```
   # Connect to WiFi & create captive portal and web server
   wifi:
      ssid: "${ssid}"
      password: "${wifi_password}"
      use_address: XXX.XXX.XXX.XXX
   ```
A couple notes:
  
  The M5Stack Atom has it's own board name:
    esp32:
      board: m5stack-atom
  
  And the framework when you're using/if you choose to use BLE/BT shoudl be esp-idf, not arduino
    framework:
      type: esp-idf

# Comments are welcome

I've only created a few projects here now, so I'm happy to hear any suggestions.
