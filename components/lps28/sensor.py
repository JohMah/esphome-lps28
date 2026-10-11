import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.constants import (
    STATE_CLASS_MEASUREMENT,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
)
from . import lps28_ns

LPS28Component = lps28_ns.class_("LPS28Component", cg.PollingComponent, i2c.I2CDevice)

DEPENDENCIES = ["i2c"]

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(LPS28Component),
            cv.Optional("pressure"): sensor.sensor_schema(
                unit_of_measurement="hPa",
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PRESSURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional("temperature"): sensor.sensor_schema(
                unit_of_measurement="°C",
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(i2c.i2c_device_schema(0x5C))
)

async def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if "pressure" in config:
        sens = await sensor.new_sensor(config["pressure"])
        cg.add(var.set_pressure_sensor(sens))
    if "temperature" in config:
        sens = await sensor.new_sensor(config["temperature"])
        cg.add(var.set_temperature_sensor(sens))
