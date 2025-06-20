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
        self.setWindowTitle("MAKE LABS - COLOR FINDER")
        self.setFixedSize(620, 520)

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

        # --- Title / Branding Text (instead of logo) ---
        self.branding = QLabel("MAKE LABS\nCOLOR FINDER")
        self.branding.setFont(QFont("Arial", 18, QFont.Bold))
        self.branding.setStyleSheet("color: #2c3e50; text-align: center;")
        self.branding.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.branding, 0, 1, 2, 1)  # span over 2 rows

        # --- RGB Inputs ---
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

        # --- Control Buttons ---
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_animation)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_animation)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_animation)

        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(self.continue_animation)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.continue_button)
        layout.addLayout(button_layout, 3, 0, 1, 2)

        # --- Counter Label ---
        self.counter = 0
        self.counter_label = QLabel("Completed Transitions: 0")
        self.counter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.counter_label, 4, 0, 1, 2)

        self.setLayout(layout)

        # --- Timer for animation ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_color)

        # --- Animation Variables ---
        self.r = self.g = self.b = 0
        self.r_target = self.g_target = self.b_target = 0

    def start_animation(self):
        try:
            self.r_target = max(0, min(255, int(self.r_input.text())))
            self.g_target = max(0, min(255, int(self.g_input.text())))
            self.b_target = max(0, min(255, int(self.b_input.text())))
            self.timer.start(333)  # 3 FPS (1000ms / 3)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter numbers between 0 and 255.")

    def continue_animation(self):
        if not self.timer.isActive():
            self.timer.start(333)

    def stop_animation(self):
        self.timer.stop()

    def reset_animation(self):
        self.timer.stop()
        self.r = self.g = self.b = 0
        self.update_display()

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

        self.update_display()

        if not updated:
            self.timer.stop()
            self.counter += 1
            self.counter_label.setText(f"Completed Transitions: {self.counter}")

    def update_display(self):
        img = QImage(250, 250, QImage.Format_RGB32)
        img.fill(QColor(self.r, self.g, self.b))
        self.color_display.setPixmap(QPixmap.fromImage(img))
        self.rgb_label.setText(f"R: {self.r} | G: {self.g} | B: {self.b}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ColorFinderApp()
    win.show()
    sys.exit(app.exec_())
