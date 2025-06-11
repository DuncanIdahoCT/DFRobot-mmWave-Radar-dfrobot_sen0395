# DFRobot mmWave Radar (dfrobot_sen0395)
### This repository seeks to address the breaking change in esphome 2025.2 where the ability to use custom components, in this case mmWave sensors, were removed causing the typical use of most ESP MCU based mmWave modules to fail update in ESPHome Device Builder.

My initial solution (see [see here](/Initial%20Solution.md)) was a bit of a hack job/workaround but I've now managed to get back full functionality by refactoring the c++ code that we've all known and loved for the DFRobot (sen0395) mmWave modules. There is zero loss of original functionality and once again, it's possible to query the modules settings and switch states instead of blind setting or toggling switch states which is both bad for the module (see MFGR note on limited writes to module) and also not very clean as far as knowing what the actual setting is vs. just blind fire changing it and hoping it worked.

The (very limited) built-in component for the dfrobot_sen0395 module
https://github.com/esphome/esphome/tree/dev/esphome/components/dfrobot_sen0395

The change notes from ESPHome:
https://esphome.io/guides/contributing#a-note-about-custom-components

The installation below is largely the same as previous projects I've posted here. The notable changes are in the yaml file and now the creation of an external component structure and python init file along with header and c++ source:

The notable changes to yaml are...
  
  Removal of the deprecated custom component:
  ```
  sensor:      
  - platform: custom
    lambda: |-
      auto s = new leapmmw(id(uart_bus));
      App.register_component(s);
      return {};
    sensors:
  ```
 Removal of package references and the header_file "substitution" variable along with include references:
```
packages:
  inclusions: !include packages/leapmmw_sensor.yml
header_file: header/leapmmw_sensor.h
esphome:
  name: ${device_name}
  includes:
    - ${header_file}
```
 As before, the "custom" component (now a proper external component) allows all get/set methods:
```
id(mmw_sensor).getmmwConf("getSensitivity")
id(mmw_sensor).getmmwConf("getRange")
id(mmw_sensor).getmmwConf("getLatency")
id(mmw_sensor).getmmwConf("getLedMode")
```

### Installation:
 * Download the files and copy them (keeping their subfolder paths) into your Home Assistant config/esphome main folder:

   ```
   root_esphome_folder_path
   ├── espresence-occupancy-nightlight-multi-sensor.yaml
   └── external_components
       └── leapmmw
           ├── __init__.py
           ├── leapmmw.h
           └── leapmmw.cpp
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
  
  And the framework when you're using/if you choose to use BLE/BT should be esp-idf, not arduino
    framework:
      type: esp-idf
