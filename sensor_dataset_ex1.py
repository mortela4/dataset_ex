import dataset
import uuid

from sensor_types.sensor_base import ExternalSensorBase
from sensor_utils.sensor_builder import build_sensor_from_dataset, show_sensor_info, sensor_type_map


def insert_class_as_dict(sensor_db=None, cls_instance=None, debug=False):
    def debug_print(msg):
        if debug:
            print(msg)
    if sensor_db is None:
        print("NO database connector given - bailing out!")
    if cls_instance is None:
        print("NO sensor object passed as argument - bailing out!")
    #
    if not isinstance(cls_instance, ExternalSensorBase):
        print("Unkown object type - cannot use!")
        return
    # Set up table
    sensor_table = sensor_db['sensors']
    # Insert data if any ...
    prop_dict = {}
    for key, val in cls_instance.__dict__.items():
        if val is None:
            debug_print("Key '%s' has no value - skipping ..." % key)
        elif callable(val):
            debug_print("Key '%s' is a callable (func or method reference) - skipping ..." % key)
        elif isinstance(val, uuid.UUID):
            debug_print("Key '%s' is a UUID - need conversion to DB-acknowledged type ..." % key)
            prop_dict[key] = val.bytes_le
        else:
            debug_print("Key '%s' is a property with value = %s - adding to persisted data ..." % (key, val))
            prop_dict[key] = val
    # Store to DB
    sensor_table.insert(prop_dict)
    sensor_db.commit()


if __name__ == "__main__":
    print("DataSet version: ", dataset.__version__)
    db = dataset.connect('sqlite:///:memory:')  # use 'sqlite:///sensors.db' to persist ...

    s1 = ExternalSensorBase(type_name='spi', bus_no=3, dev_name='sht711', alias='hygrometer-1A')
    print(s1.__dict__)
    s2 = ExternalSensorBase(type_name='i2c', bus_no=1, dev_name='sht711', alias='hygrometer-1B')
    print(s1.__dict__)
    s3 = ExternalSensorBase(type_name='spi', bus_no=3, dev_name='sht711', alias='hygrometer-1C')
    print(s1.__dict__)
    #
    insert_class_as_dict(db, s1)
    insert_class_as_dict(db, s2)
    insert_class_as_dict(db, s3)
    #
    print("\n\nFind single sensors by alias:")
    print("=================================")
    table = db['sensors']
    rht1b = table.find_one(alias='hygrometer-1B')
    print(repr(rht1b))
    rht1a = table.find_one(alias='hygrometer-1A')
    print(repr(rht1a))
    # Find many
    spi_sensors = table.find(type_name="spi")
    print("SPI-sensors:")
    print("============")
    for idx, sensor in enumerate(spi_sensors):
        print("Data for sensor no %d:" % idx)
        print("-----------------------")
        # print(repr(sensor))
        show_sensor_info(sensor)
    #
    # Delete inserts:
    # db.rollback()


