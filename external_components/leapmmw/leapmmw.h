#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include <string>

namespace esphome {
namespace leapmmw {

class LeapMMW : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  
  void publishNumber(std::string sensor, float resp);
  void publishSwitch(std::string sensor, int state);
  void getmmwConf(std::string mmwparam);

 protected:
  int readline(int readch, char *buffer, int len);
  std::string getline;
};

}  // namespace leapmmw
}  // namespace esphome