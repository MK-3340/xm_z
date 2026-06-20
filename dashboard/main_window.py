import sys 

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from database.db_manager import (query_latest_sensor_data,query_latest_alarms)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("工业物联网网关监控面板")
        self.resize(900, 500)

        self.title_label  = QLabel("最近 10 条传感器数据")

        self.sensor_table = QTableWidget()
        self.sensor_table.setColumnCount(7)
        self.sensor_table.setHorizontalHeaderLabels(
            ["ID", "设备ID", "时间", "温度", "振幅", "电流", "状态"]
        )

        self.alarm_title_label = QLabel("最近 10 条报警记录")

        self.alarm_table = QTableWidget()
        self.alarm_table.setColumnCount(6)
        self.alarm_table.setHorizontalHeaderLabels(
            ["ID", "设备ID", "时间","报警类型","报警原因","严重程度"]
        )       

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.sensor_table)
        layout.addWidget(self.alarm_title_label)
        layout.addWidget(self.alarm_table)        


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_latest_data()
        self.load_latest_alarms()

        self.refresh_time = QTimer(self)
        self.refresh_time.timeout.connect(self.refresh_dashboard)
        self.refresh_time.start(2000)

    def load_latest_data(self):
        rows = query_latest_sensor_data(limit=10)

        self.sensor_table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            values = [
                row["id"],
                row["device_id"],
                row["timestamp"],
                row["temperature"],
                row["vibration"],
                row["current"],
                row["status"],
            ] 

            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.sensor_table.setItem(row_index, col_index, item)

    def load_latest_alarms(self):
        rows = query_latest_alarms(limit=10)

        self.alarm_table.setRowCount(len(rows))
        
        for row_index, row in enumerate(rows):
            values = [
                row["id"],
                row["device_id"],
                row["timestamp"],
                row["alarm_type"],
                row["alarm_reason"],
                row["severity"],
            ] 

            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.alarm_table.setItem(row_index, col_index, item)


    def refresh_dashboard(self):
        """每 2 秒从SQLite 刷新两张表。"""
        self.load_latest_data()
        self.load_latest_alarms()


def main():
    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
