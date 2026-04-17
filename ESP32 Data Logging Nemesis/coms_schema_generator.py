import struct
from enum import Enum


class telemetry_data_type:
    def __init__(self, name_c: str, alias_struct: str, data_size: int):
        self.name_c: str = name_c
        self.alias_struct: str = alias_struct
        self.data_size: int = data_size


# alias_struct from here: https://docs.python.org/3/library/struct.html

data_type_mapping: dict[str, telemetry_data_type] = {
    "float": telemetry_data_type("float", "f", 4),
    "int": telemetry_data_type("int", "i", 4),
    "uint": telemetry_data_type("unsigned int", "I", 4),
    "bool": telemetry_data_type("_Bool", "?", 1),
}


class SignalType(Enum):
    SENSOR = "SENSOR"
    CONTROL = "CONTROL"


class DeviceType(Enum):
    ARDUINO = "ARDUINO"
    ESP32 = "ESP32"


class serial_to_computer_data:
    data_format: list[tuple[str, str, SignalType]]

    def __init__(
        self,
        data_format: list[tuple[str, str]],
        telemetry_name: str,
        device_type: DeviceType,
    ):
        self.data_format = data_format
        self.telemetry_name = telemetry_name

        self.struct_format = "<"
        self.data_length: int = 0

        for name, type, signal_type in data_format:
            self.struct_format += data_type_mapping[type].alias_struct
            self.data_length += data_type_mapping[type].data_size

    def unpack_values(self, data: bytes):
        assert len(data) == self.data_length
        return struct.unpack(self.struct_format, data)

    def make_python_file(self, path: str):
        python_file_text = f'import struct\nclass {self.telemetry_name}:\n\tdata_length = {self.data_length}\n\tstruct_format = "{self.struct_format}"\n'

        for name, type, signal_type in self.data_format:
            python_file_text += f"\t{name}: {type}\n"

        python_file_text += "\tdef unpack_values(self, data: bytes):\n\t\tassert len(data) == self.data_length\n\t\tunpacked_values = struct.unpack(self.struct_format, data)\n"

        position = 0

        make_header_text = '\tdef make_header(self) -> str:\n\t\treturn "'

        make_csv_text = '\tdef make_csv_line(self) -> str:\n\t\treturn f"'

        for name, type, signal_type in self.data_format:
            python_file_text += (
                f"\t\tself.{name} = {type}(unpacked_values[{position}])\n"
            )
            position += 1

            make_header_text += f"{name}, "
            make_csv_text += f"{{self.{name}}},"

        make_header_text += '\\n"\n'
        make_csv_text += '\\n"\n'

        python_file_text += make_header_text
        python_file_text += make_csv_text

        with open(path, "w") as file:
            file.write(python_file_text)

        return

    def make_c_file(self, path: str):
        c_file_text = f"#define BUFFER_SIZE {self.data_length}\nclass {self.telemetry_name}\n{{\npublic:\n"

        for name, type, signal_type in self.data_format:
            c_data_type = data_type_mapping[type]
            c_file_text += f"\t{c_data_type.name_c} {name};\n"

        c_file_text += "\tint size = BUFFER_SIZE;\n\tchar buffer[BUFFER_SIZE];\n\n\tchar *make_data_buffer()\n\t{\n"

        current_position: int = 0
        for name, type, signal_type in self.data_format:
            c_data_type = data_type_mapping[type]

            c_file_text += f"\t\tmemcpy(&buffer[{current_position}], &{name}, {c_data_type.data_size});\n"
            current_position += c_data_type.data_size
        c_file_text += "\t\treturn buffer;\n\t};\n};"

        with open(path, "w") as file:
            file.write(c_file_text)

        return
