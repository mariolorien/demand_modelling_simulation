from PyQt6.QtWidgets import QApplication, QLabel

import sys

app = QApplication(sys.argv)

label = QLabel("Hello, PyQt!")
label.resize(200, 100)
label.show()

sys.exit(app.exec())
