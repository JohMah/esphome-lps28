#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"

namespace esphome {
namespace lps28 {

class LPS28Component : public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void update() override;

  void set_pressure_sensor(sensor::Sensor *s) { pressure_sensor_ = s; }
  void set_temperature_sensor(sensor::Sensor *s) { temperature_sensor_ = s; }

 protected:
  sensor::Sensor *pressure_sensor_{nullptr};
  sensor::Sensor *temperature_sensor_{nullptr};
};

}  // namespace lps28
}  // namespace esphome
