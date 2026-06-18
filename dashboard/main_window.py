import sys 


from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from database.db_manager import query_latest_sensor_data


class MainWinow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("工业物联网网关监控面板")
        self.resize(900, 500)

        self.title_label  = QLabel("最近 10 条传感器数据")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "设备ID", "时间", "温度", "振幅", "电流", "状态"]
        )

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_latest_data()

    def load_latest_data(self):
        rows = query_latest_sensor_data(limit=10)

        self.table.setRowCount(len(rows))

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
                self.table.setItem(row_index, col_index, item)


def main():
    app = QApplication(sys.argv)


    window = MainWinow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
