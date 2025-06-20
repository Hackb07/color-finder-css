import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont
from PyQt5.QtCore import QTimer, Qt


class ColorFinderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAKE LABS - COLOR-FINDER")
        self.setFixedSize(600, 520)

        layout = QGridLayout()

        # --- Color Display Box ---
        self.color_display = QLabel()
        self.color_display.setFixedSize(250, 250)
        self.color_display.setStyleSheet("border: 2px solid black;")
        layout.addWidget(self.color_display, 0, 0)

        # --- RGB Value Label ---
        self.rgb_label = QLabel("R: 0 | G: 0 | B: 0")
        self.rgb_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.rgb_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.rgb_label, 1, 0)

        # --- Logo Display ---
        self.logo_label = QLabel()
        try:
            pixmap = QPixmap("logo.png")
            if pixmap.isNull():
                raise FileNotFoundError
            self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        except:
            self.logo_label.setText("LOGO\nNOT FOUND")
            self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label, 0, 1)

        # --- Branding ---
        self.branding = QLabel("MAKE LABS\nCOLOR-FINDER")
        self.branding.setFont(QFont("Arial", 14, QFont.Bold))
        self.branding.setStyleSheet("color: black;")
        self.branding.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.branding, 1, 1)

        # --- RGB Input Fields ---
        self.r_input = QLineEdit()
        self.g_input = QLineEdit()
        self.b_input = QLineEdit()
        self.r_input.setPlaceholderText("R")
        self.g_input.setPlaceholderText("G")
        self.b_input.setPlaceholderText("B")

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("R"))
        input_layout.addWidget(self.r_input)
        input_layout.addWidget(QLabel("G"))
        input_layout.addWidget(self.g_input)
        input_layout.addWidget(QLabel("B"))
        input_layout.addWidget(self.b_input)
        layout.addLayout(input_layout, 2, 0, 1, 2)

        # --- Submit Button ---
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.start_animation)
        layout.addWidget(self.submit_button, 3, 0, 1, 2)

        # --- Timer for RGB Animation ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_color)

        self.setLayout(layout)

        # Variables for animation
        self.r = self.g = self.b = 0
        self.r_target = self.g_target = self.b_target = 0

    def start_animation(self):
        try:
            self.r_target = min(max(int(self.r_input.text()), 0), 255)
            self.g_target = min(max(int(self.g_input.text()), 0), 255)
            self.b_target = min(max(int(self.b_input.text()), 0), 255)

            self.r = self.g = self.b = 0
            self.timer.start(1000)  # 1 second per update
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter valid numbers between 0 and 255 for R, G, B.")

    def update_color(self):
        updated = False
        if self.r < self.r_target:
            self.r += 1
            updated = True
        if self.g < self.g_target:
            self.g += 1
            updated = True
        if self.b < self.b_target:
            self.b += 1
            updated = True

        # Update the color display
        img = QImage(250, 250, QImage.Format_RGB32)
        img.fill(QColor(self.r, self.g, self.b))
        self.color_display.setPixmap(QPixmap.fromImage(img))

        # Update RGB label
        self.rgb_label.setText(f"R: {self.r} | G: {self.g} | B: {self.b}")

        if not updated:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ColorFinderApp()
    win.show()
    sys.exit(app.exec_())
