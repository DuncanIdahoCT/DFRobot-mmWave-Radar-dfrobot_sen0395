import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ['uart']
CODEOWNERS = ['@yourname']  # Replace with your GitHub username

leapmmw_ns = cg.esphome_ns.namespace('leapmmw')
LeapMMW = leapmmw_ns.class_('LeapMMW', cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(LeapMMW),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)