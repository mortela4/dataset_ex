from sensor_types.sensor_base import ExternalSensorBase
from sensor_types.sensor_devices import I2cSensor, SpiSensor, UartSensor


sensor_type_map = {'i2c': I2cSensor, 'spi': SpiSensor, 'uart': UartSensor}


def show_sensor_info(sensor_data):
    for entry_name, entry_value in sensor_data.items():
        if entry_name == "uuid":
            uuid_hex_val = entry_value.hex()
            print("Property '%s': %s (%s)" % (entry_name, uuid_hex_val, int(uuid_hex_val, 16)))
        else:
            print("Property '%s': %s" % (entry_name, entry_value))


def build_sensor_from_dataset(sensor_data_set=None):
    show_sensor_info(sensor_data_set)
    #
    sensor_type = sensor_data_set['sensor_type']
    sensor_in = sensor_type_map[sensor_type]()
    #
    print("Built sensor of type: ", repr(sensor_in))
    #
    sensor_in.base = ExternalSensorBase()
    builder = SensorBuilder(sensor_in)
    #
    for entry_name, entry_value in sensor_data_set.items():
        if entry_name == "uuid":
            val = int(entry_value.hex(), 16)
        else:
            val = entry_value
        #
        builder = builder.with_field(entry_name, entry_value)
    #
    return



# **************** SENSOR-BUILDER ********************
class SensorBuilder(object):
    """
    Generic (almost ...) sensor builder.
    """
    def __init__(self, sensor_instance=None):
        self.sensor_obj = sensor_instance

    def with_field(self, field_name, field_value):
        existing_base_props = self.sensor_obj.base.__dict__
        existing_dev_props = self.sensor_obj.__dict__
        # Start with 'base' object = base class:
        if field_name not in existing_base_props:
            # Then device-specific props:
            self.sensor_obj.__dict__[field_name] = field_value
            if field_name not in existing_dev_props:
                print("Warning: field named '%s' - not in (sub)class! Possibly extending class ..." % field_name)
        else:
            self.sensor_obj.base.__dict__[field_name] = field_value
        #
        return self

    def build(self):
        return self.sensor_obj

