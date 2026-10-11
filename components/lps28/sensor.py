import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c

# 1. Declare the exact C++ namespace and binding class
lps28_ns = cg.esphome_ns.namespace("lps28")
LPS28Component = lps28_ns.class_("LPS28Component", cg.PollingComponent, i2c.I2CDevice)

DEPENDENCIES = ["i2c"]

# 2. Build the configuration schema using clean string literals instead of broken constants
CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(LPS28Component),
            cv.Optional("pressure"): sensor.sensor_schema(
                unit_of_measurement="hPa",
                accuracy_decimals=2,
                device_class="pressure",
                state_class="measurement",
            ),
            cv.Optional("temperature"): sensor.sensor_schema(
                unit_of_measurement="°C",
                accuracy_decimals=1,
                device_class="temperature",
                state_class="measurement",
            ),
        }
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(i2c.i2c_device_schema(0x5C))
)

# 3. Clean generator to link the pipeline variables
def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    if "pressure" in config:
        sens = yield sensor.new_sensor(config["pressure"])
        cg.add(var.set_pressure_sensor(sens))
    if "temperature" in config:
        sens = yield sensor.new_sensor(config["temperature"])
        cg.add(var.set_temperature_sensor(sens))
