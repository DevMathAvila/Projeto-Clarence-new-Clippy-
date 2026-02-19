import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, 
    QPushButton, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from services.openai_service import ask_openai

class OpenAIWorker(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt

    def run(self):
        response = ask_openai(self.prompt)
        self.result_ready.emit(response)

class Clarence(QWidget):
    def __init__(self):
        super().__init__()
        self._expanded = False
        self._drag_pos = None
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setup_ui()
        self.apply_appearance()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel("C")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.container = QFrame()
        self.container.setVisible(False)
        
        chat_layout = QVBoxLayout(self.container)
        chat_layout.setContentsMargins(15, 10, 15, 15)
        chat_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(QApplication.quit)
        header_layout.addWidget(self.close_btn)
        
        self.response_view = QTextEdit()
        self.response_view.setReadOnly(True)
        self.response_view.setPlaceholderText("Aguardando sua pergunta...")

        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(65)
        self.input_field.setPlaceholderText("Escreva algo e aperte Enter...")
        self.input_field.installEventFilter(self)

        self.submit_btn = QPushButton("Enviar")
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self.process_request)

        chat_layout.addLayout(header_layout)
        chat_layout.addWidget(self.response_view)
        chat_layout.addWidget(self.input_field)
        chat_layout.addWidget(self.submit_btn)

        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.container)

    def apply_appearance(self):
        """Define o estilo QSS responsivo aos estados."""
        accent = "#0072ff"
        
        if not self._expanded:
            self.setFixedSize(80, 80)
            self.setStyleSheet(f"""
                Clarence {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00c6ff, stop:1 {accent});
                    border-radius: 40px;
                }}
                QLabel {{ color: white; font-size: 32px; font-weight: bold; background: transparent; }}
                QPushButton {{ border: none; }}
            """)
        else:
            self.setFixedSize(350, 480)
            self.setStyleSheet(f"""
                Clarence {{
                    background: rgba(25, 25, 35, 250);
                    border: 1px solid {accent};
                    border-radius: 20px;
                }}
                QTextEdit {{
                    background: rgba(0, 0, 0, 80);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 20);
                    border-radius: 10px;
                    padding: 8px;
                }}
                QPushButton {{
                    background: {accent};
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background: #00c6ff; }}
                QPushButton#close_btn {{ color: #888; background: transparent; }}
            """)

    def process_request(self):
        prompt = self.input_field.toPlainText().strip()
        if not prompt: return

        self.input_field.clear()
        self.response_view.setText("Clarence está pensando...")
        self.submit_btn.setEnabled(False)

        self.worker = OpenAIWorker(prompt)
        self.worker.result_ready.connect(self.on_response_received)
        self.worker.start()

    def on_response_received(self, response):
        self.response_view.setText(response)
        self.submit_btn.setEnabled(True)
        self.input_field.setFocus()

    def toggle_state(self):
        self._expanded = not self._expanded
        self.icon_label.setVisible(not self._expanded)
        self.container.setVisible(self._expanded)
        self.apply_appearance()

    def mouseDoubleClickEvent(self, event):
        self.toggle_state()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def eventFilter(self, source, event):
        if source == self.input_field and event.type() == event.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.process_request()
                return True
        return super().eventFilter(source, event)

def run_clarence():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = Clarence()
    window.show()
    sys.exit(app.exec())