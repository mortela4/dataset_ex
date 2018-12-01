import dataset


if __name__ == "__main__":
    print("DataSet version: ", dataset.__version__)
    db = dataset.connect('sqlite:///:memory:')  # use 'sqlite:///sensors.db' to persist ...

    sensor_table = db['sensors']

    sensor_table.insert(dict(name='SHT711', type="spi", bus_no=3, cs_num=6, alias="RHT-1A"))
    sensor_table.insert(dict(name='SHT711', type="i2c", bus_no=1, i2c_addr=78, alias="RHT-1B"))
    sensor_table.insert(dict(name='SHT711', type="i2c", bus_no=1, i2c_addr=71, alias="RHT-1C"))

    rht1b = sensor_table.find_one(alias='RHT-1B')
    print(repr(rht1b))
    rht1a = sensor_table.find_one(alias='RHT-1A')
    print(repr(rht1a))
    # Find many
    i2c_sensors = sensor_table.find(type="i2c")
    print("I2C-sensors:")
    print("============")
    for sensor in i2c_sensors:
        print(repr(sensor))
