#include "lps28.h"
#include "esphome/core/log.h"

namespace esphome {
namespace lps28 {

static const char *TAG = "lps28.sensor";

void LPS28Component::setup() {
  ESP_LOGCONFIG(TAG, "Setting up LPS28DFW at address 0x%02X...", this->address_);

  if (!this->write_byte(0x10, 0x24)) {
    ESP_LOGE(TAG, "Failed to initialize LPS28DFW at 0x%02X via I2C!", this->address_);
    this->mark_failed();
  }
}

void LPS28Component::update() {
  uint8_t buffer[3];

  if (this->read_register(0x28, buffer, 3) == i2c::ERROR_OK) {
    uint32_t raw_press = ((uint32_t)buffer[2] << 16) | ((uint32_t)buffer[1] << 8) | buffer[0];
    float pressure = (float)raw_press / 4096.0f;

    if (this->pressure_sensor_ != nullptr) {
      this->pressure_sensor_->publish_state(pressure);
    }
  }

  if (this->read_register(0x2B, buffer, 2) == i2c::ERROR_OK) {
    int16_t raw_temp = ((int16_t)buffer[1] << 8) | buffer[0];
    float temperature = (float)raw_temp / 100.0f;

    if (this->temperature_sensor_ != nullptr) {
      this->temperature_sensor_->publish_state(temperature);
    }
  }
}

}  // namespace lps28
}  // namespace esphome
