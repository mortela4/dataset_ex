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
        if first_pass:
            tmp = builder.with_field(entry_name, val)
            first_pass = False
        else:
            tmp = tmp.with_field(sensor_prop_name, prop_value)
    #
    sensor = tmp.build()
    #
    return sensor


def build_sensor(sensor_clsname=None, base_clsname=None, props=None):
    if sensor_clsname is None or base_clsname is None or props is None:
        # TODO: possibly emit ERROR msg here - and/or throw??
        print("ERROR: build_sensor() requires all of 'sensor_clsname', "
              "'base_clsname' and 'ppack' parameters to be provided!")
        return None
    #
    raw_obj = sensor_clsname(base_type=base_clsname)
    sensor_builder = SensorBuilder(sensor_instance=raw_obj)
    #
    # Set up list of props:
    # Build sensor:
    first_pass = True
    for sensor_prop_name, prop_value in props.items():
        if sensor_prop_name != "sensor_type":
            if first_pass:
                tmp = sensor_builder.with_field(sensor_prop_name, prop_value)
                first_pass = False
            else:
                tmp = tmp.with_field(sensor_prop_name, prop_value)
    # Get final object:
    sensor = tmp.build()
    #
    return sensor


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

