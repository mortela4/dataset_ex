
from sensor_properties.sensor_props import ComplexValue


# static functions - could as well be @staticmethod-decorated methods in 'Sensors' class.
# =======================================================================================
def configure_i2c_sensor(bus_no=None, i2c_addr=None):
    if bus_no is None or i2c_addr is None:
        print("Skipping config ...")
    else:
        print("Configuring I2C-sensor on bus no.%d, address=%d ..." % (bus_no, i2c_addr))


def configure_spi_sensor(bus_no=None, cs_no=None):
    if bus_no is None or cs_num is None:
        print("Skipping config ...")
    else:
        print("Configuring SPI-sensor on bus no.%d, CS-num=%d..." % (bus_no, cs_num))


def get_i2c_val():
    print("Getting I2C-sensor value ...")
    # Returns a single value (which would typically be float-type):
    return 1.12345


def get_spi_val():
    print("Getting SPI-sensor value ...")
    # Demonstrates returning a complex object:
    return ComplexValue(True, 7, 8.765)


def get_uart_val():
    print("Getting UART-sensor value ...")
    # Demonstrate returning a list (of values), instead of a single value:
    return [3, 4, 5]

