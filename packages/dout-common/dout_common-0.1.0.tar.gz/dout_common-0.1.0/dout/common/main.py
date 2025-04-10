#import typer
import serial
import serial.tools.list_ports
from tabulate import tabulate

def get_modules():

    TARGET_VID = 0xf00d
    TARGET_PID = 0xbabe

    list_of_modules = []

    available_system_ports = serial.tools.list_ports.comports()

    for io_module in available_system_ports:
        if io_module.vid == TARGET_VID and io_module.pid == TARGET_PID:
            list_of_modules.append({"serial_id" : io_module.serial_number, "comport" : io_module.device})

    return list_of_modules

def print_modules_in_table(list_of_modules):
    table_rows = []
    for i, module in enumerate(list_of_modules, start=0):
        table_rows.append([f"Module {i}", module["serial_id"], module["comport"]])

    headers = ["Module" "Serial ID", "Com Port"]

    print(tabulate(table_rows, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    print_modules_in_table(get_modules())
