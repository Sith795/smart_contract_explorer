from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
import sys
from utils.abi_loader import get_contract_abi
from utils.contract_parser import parse_contract
from utils.monitor import monitor_events
import json

class ContractExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Довідник смарт-контрактів")
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введіть адресу контракту")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.load_button = QPushButton("Завантажити контракт")
        self.load_button.clicked.connect(self.load_contract)

        layout.addWidget(QLabel("Адреса контракту:"))
        layout.addWidget(self.address_input)
        layout.addWidget(self.load_button)
        layout.addWidget(QLabel("Інформація:"))
        layout.addWidget(self.output)
        self.setLayout(layout)

    def load_contract(self):
        address = self.address_input.text()
        abi = get_contract_abi(address)
        functions, events = parse_contract(address, abi)
        info = "📘 Функції:"
        for f in functions:
            info += f" - {f.fn_name}()"
        info += "\n📗 Події:"
        for e in events.__dict__.get("_events", []):
            info += f" - {e.event_name}\n"
        self.output.setText(info)

        # Моніторинг
        def handle_event(ev):
            self.output.append(f"📡 Подія: {json.dumps(dict(ev), indent=2)}")

        monitor_events(address, abi, handle_event)

def run_gui():
    app = QApplication(sys.argv)
    explorer = ContractExplorer()
    explorer.show()
    sys.exit(app.exec_())
