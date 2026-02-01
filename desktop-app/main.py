import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
)
from charts import BarChartCanvas
from api_client import upload_csv, fetch_history, fetch_dataset_by_id
import os

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(200, 200, 900, 600)

        # -------- Root layout --------
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)

        # -------- Main horizontal layout --------
        self.main_layout = QHBoxLayout()
        root_layout.addLayout(self.main_layout)

        # -------- Left panel (History) --------
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel, 1)

        self.left_panel.addWidget(QLabel("Previous Uploads"))

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_from_history)
        self.left_panel.addWidget(self.history_list)

        # -------- Right panel (Main content) --------
        self.right_panel = QVBoxLayout()
        self.main_layout.addLayout(self.right_panel, 3)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_file)
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setEnabled(False)
        self.right_panel.addWidget(self.pdf_btn)

        self.right_panel.addWidget(self.upload_btn)

        self.summary_label = QLabel("Upload a CSV file to see summary")
        self.right_panel.addWidget(self.summary_label)

        self.table = QTableWidget()
        self.right_panel.addWidget(self.table)

        self.chart = None

        # Load history at startup
        self.load_history()
        self.current_dataset_id = None

    # ----------------- Upload CSV -----------------
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            data = upload_csv(file_path)
            self.render_dataset(data)
            self.load_history()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ----------------- History -----------------
    def load_history(self):
        self.history_list.clear()
        datasets = fetch_history()

        for ds in datasets:
            item = QListWidgetItem(
                f"Dataset #{ds['id']} ({ds['summary']['total_count']} items)"
            )
            item.setData(1, ds["id"])
            self.history_list.addItem(item)

    def load_from_history(self, item):
        dataset_id = item.data(1)
        data = fetch_dataset_by_id(dataset_id)
        self.render_dataset(data)

    # ----------------- Rendering helpers -----------------
    def render_dataset(self, data):
        self.show_summary(data["summary"])
        self.show_table(data["preview"])
        self.show_chart(data["summary"]["type_distribution"])

    def show_summary(self, summary):
        text = (
            f"Total: {summary['total_count']} | "
            f"Avg Flowrate: {summary['avg_flowrate']} | "
            f"Avg Pressure: {summary['avg_pressure']} | "
            f"Avg Temperature: {summary['avg_temperature']}"
        )
        self.summary_label.setText(text)

    def show_table(self, rows):
        if not rows:
            return

        headers = rows[0].keys()
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(rows):
            for col_idx, key in enumerate(headers):
                self.table.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(row[key]))
                )

    def show_chart(self, distribution):
        if self.chart:
            self.right_panel.removeWidget(self.chart)
            self.chart.deleteLater()

        self.chart = BarChartCanvas(distribution)
        self.right_panel.addWidget(self.chart)

    def render_dataset(self, data):
        self.current_dataset_id = data["id"]
        self.show_summary(data["summary"])
        self.show_table(data["preview"])
        self.show_chart(data["summary"]["type_distribution"])
        self.pdf_btn.setEnabled(True)

    def download_pdf(self):
        if not self.current_dataset_id:
            return

        import requests
        from PyQt5.QtWidgets import QFileDialog

        url = f"http://127.0.0.1:8000/api/report/{self.current_dataset_id}/"
        headers = {
            "Authorization": f"Token {os.getenv('API_TOKEN')}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to download PDF")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "report.pdf", "PDF Files (*.pdf)"
        )

        if file_path:
            with open(file_path, "wb") as f:
                f.write(response.content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())