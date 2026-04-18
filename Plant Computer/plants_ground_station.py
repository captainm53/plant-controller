from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMainWindow,
    QPushButton,
    QTableView,
    QGridLayout,
    QWidget,
)
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QTextTableCell

import sys

import serial

from datetime import date, datetime, timezone

from coms_schema_generator import serial_to_computer_data, SignalType, DeviceType
from planter_data_schema import PlanterToPC

data_format: list[tuple[str, str, SignalType]] = [
    ("time", "float", SignalType.SENSOR),
    ("vlv0", "bool", SignalType.CONTROL),
    ("vlv1", "bool", SignalType.CONTROL),
    ("vlv2", "bool", SignalType.CONTROL),
    ("vlv3", "bool", SignalType.CONTROL),
    ("vlv4", "bool", SignalType.CONTROL),
    ("vlv5", "bool", SignalType.CONTROL),
    ("light0", "bool", SignalType.CONTROL),
    ("light1", "bool", SignalType.CONTROL),
    ("sns0", "float", SignalType.SENSOR),
    ("sns1", "float", SignalType.SENSOR),
    ("sns2", "float", SignalType.SENSOR),
    ("sns3", "float", SignalType.SENSOR),
    ("sns4", "float", SignalType.SENSOR),
    ("sns5", "float", SignalType.SENSOR),
    ("sns6", "float", SignalType.SENSOR),
    ("sns7", "float", SignalType.SENSOR),
]


class MainWindow(QMainWindow):
    saving_data_to_file: bool = False
    data_format = PlanterToPC()

    def __init__(self):
        super().__init__()

        # Set up telemetry worker thread
        self.threadpool = QThreadPool()

        datetime_now = datetime.now(timezone.utc)
        self.worker = TelemetryWorker(
            PlanterToPC(), f"./data/{datetime_now:%Y%m%d-%H%M%S}.csv"
        )

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.kickOffWorker)
        self.timer.start()

        cental_widget = QWidget()

        self.setWindowTitle("My App")

        # Logging button
        check_box_log_data = QPushButton("Logging")
        check_box_log_data.setCheckable(True)
        check_box_log_data.clicked.connect(self.set_logging_state)

        # Table of live data
        standard_item = QStandardItemModel()
        standard_item.setColumnCount(3)
        standard_item.setRowCount(len(data_format))
        standard_item.setHorizontalHeaderLabels(["Name", "Value"])

        control_index = 0
        for i, (name, type, signal_type) in enumerate(data_format):
            name_item = QStandardItem(name)
            value_item = QStandardItem(10)

            standard_item.setItem(i, 0, name_item)
            standard_item.setItem(i, 1, value_item)
            if signal_type == SignalType.CONTROL:
                checkbox_item = QStandardItem()
                checkbox_item.setCheckable(True)
                checkbox_item.setData(control_index)

                standard_item.setItem(i, 2, checkbox_item)

                control_index += 1

        self.data_table = QTableView()
        self.data_table.setSortingEnabled(True)
        self.data_table.setModel(standard_item)

        standard_item.itemChanged.connect(self.send_command)

        self.standard_item = standard_item

        # Set the central widget of the Window.
        grid_layout = QGridLayout()

        grid_layout.addWidget(self.data_table)
        grid_layout.addWidget(check_box_log_data)

        cental_widget.setLayout(grid_layout)

        self.setCentralWidget(cental_widget)

    def send_command(self, item: QStandardItem):
        if item.isCheckable():
            print(item.checkState(), item.data())
            channel_bytes = int(item.data()).to_bytes()
            checked = item.checkState() == Qt.CheckState.Checked
            channel_bytes += checked.to_bytes()
            print(channel_bytes)
            self.worker.serial_port.write(channel_bytes)

    def set_logging_state(self, state):
        self.saving_data_to_file = state
        if self.saving_data_to_file:
            datetime_now = datetime.now()
            self.worker.path = f"./data/{datetime_now:%Y%m%d-%H%M%S}.csv"
            with open(self.worker.path, "a") as f:
                f.write(self.worker.converter.make_header())

    def kickOffWorker(self):
        # self.threadpool.start(self.worker)
        self.worker.run(self.saving_data_to_file, self.standard_item)


class TelemetryWorker(QRunnable):
    """Worker thread for recieving/sending data in the background"""

    def __init__(self, converter: PlanterToPC, logging_path: str):
        super().__init__()
        self.serial_port = serial.Serial("COM3", 115200, timeout=1.5)

        self.converter = converter

        self.path = logging_path

        self.data = bytes()

    @pyqtSlot()
    def run(self, logging: bool, standard_item: QStandardItemModel):  # ty:ignore[invalid-method-override]
        new_data = self.serial_port.read_all()
        self.data += new_data

        while len(self.data) >= self.converter.data_length:
            self.converter.unpack_values(self.data[0 : self.converter.data_length])
            # print("Received:", self.converter.time, self.converter.sns0)
            self.data = self.data[self.converter.data_length :]

            # print(self.converter.make_csv_line())
            for i, (name, type, signal_type) in enumerate(data_format):
                value = getattr(self.converter, name)
                value_item = QStandardItem(str(value))
                standard_item.setItem(i, 1, value_item)

            if logging:
                with open(self.path, "a") as f:
                    f.write(self.converter.make_csv_line())


data_formatter = serial_to_computer_data(data_format, "PlanterToPC", DeviceType.ARDUINO)
data_formatter.make_c_file("../Plant Arduino/include/data_schema.h")
data_formatter.make_python_file("./planter_data_schema.py")

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)


# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
