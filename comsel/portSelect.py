from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
)
import serial.tools.list_ports
import sys, re
from importlib.resources import files


class PortSelectionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор COM порта и скорости передачи данных")

        # Устанавливаем иконку окна
        icon_path = files("comsel.icons").joinpath("icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        # Применяем бело-голубой стиль
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F7FF; /* Голубой фон */
            }
            QLabel {
                color: #003366; /* Темно-синий текст */
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #FFFFFF; /* Белый фон */
                color: #003366; /* Темно-синий текст */
                border: 1px solid #99CCFF; /* Голубая рамка */
                border-radius: 4px;
                padding: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #99CCFF; /* Светло-голубой */
                color: #FFFFFF; /* Белый текст */
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #66B2FF; /* Темнее при наведении */
            }
            QPushButton:pressed {
                background-color: #3399FF; /* Еще темнее при нажатии */
            }
        """)

        # Получаем размеры экрана
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Устанавливаем размер окна на основе экрана
        window_width = screen_width // 3
        window_height = screen_height // 4
        self.setFixedSize(window_width, window_height)  # Фиксированный размер окна

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Горизонтальный layout для COM-порта и baudrate
        horizontal_layout = QHBoxLayout()

        # Вертикальный layout для выбора COM-порта
        port_layout = QVBoxLayout()
        port_label = QLabel("Список доступных COM портов:")
        self.ports_combo = QComboBox()
        self.populate_combo_box()

        self.port_input_label = QLabel("Или введите COM порт вручную:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Введите COM порт")  # Устанавливаем placeholder

        port_layout.addWidget(port_label)
        port_layout.addWidget(self.ports_combo)
        port_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))  # Отступ
        port_layout.addWidget(self.port_input_label)
        port_layout.addWidget(self.port_input)

        horizontal_layout.addLayout(port_layout)

        # Вертикальный layout для выбора baudrate
        baudrate_layout = QVBoxLayout()
        baudrate_label = QLabel("Список доступных Baudrate:")
        self.baudrate_combo = QComboBox()
        self.populate_baudrate_combo()

        self.baudrate_input_label = QLabel("Или введите Baudrate вручную:")
        self.baudrate_input = QLineEdit()
        self.baudrate_input.setPlaceholderText("Введите Baudrate")
        self.baudrate_input.setValidator(QIntValidator(1, 1000000, self))  # Устанавливаем валидатор

        baudrate_layout.addWidget(baudrate_label)
        baudrate_layout.addWidget(self.baudrate_combo)
        baudrate_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))  # Отступ
        baudrate_layout.addWidget(self.baudrate_input_label)
        baudrate_layout.addWidget(self.baudrate_input)

        horizontal_layout.addLayout(baudrate_layout)

        # Добавляем горизонтальный layout в основной
        main_layout.addLayout(horizontal_layout)

        # Кнопка подтверждения внизу
        self.confirm_button = QPushButton("&Подтвердить")
        self.confirm_button.clicked.connect(self.confirm_selection)
        main_layout.addWidget(self.confirm_button)

        # Таймер для обновления COM портов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_com_ports)
        self.timer.start(1000)  # Обновление каждые 1000 мс (1 секунда)

    def populate_combo_box(self):
        ports = list(serial.tools.list_ports.comports())
        self.ports_combo.clear()
        if ports:
            for port in ports:
                self.ports_combo.addItem(port.device)
        else:
            self.ports_combo.addItem("Нет доступных COM портов")  # Если портов нет

    def update_com_ports(self):
        """Метод для обновления списка COM портов каждую секунду."""
        current_ports = [self.ports_combo.itemText(i) for i in range(self.ports_combo.count())]
        new_ports = [port.device for port in serial.tools.list_ports.comports()]

        # Обновляем только если список портов изменился
        if current_ports != new_ports:
            self.populate_combo_box()

    def populate_baudrate_combo(self):
        # Добавляем стандартные baudrate
        default_baudrates = [115200, 9600, 19200, 38400, 57600, 250000]
        self.baudrate_combo.addItems(map(str, default_baudrates))
        self.baudrate_combo.setCurrentText("115200")  # Устанавливаем значение по умолчанию

    def confirm_selection(self):
        # Проверяем COM порт
        selected_port = self.ports_combo.currentText()
        if self.port_input.text():
            selected_port = self.port_input.text()

        if not self.is_valid_port(selected_port):
            self.port_input_label.setText("Ошибка: Неверный формат COM порта")
            return
        else:
            self.port_input_label.setText("Или введите COM порт вручную:")

        # Проверяем Baudrate
        selected_baudrate = self.baudrate_combo.currentText()
        if self.baudrate_input.text():
            selected_baudrate = self.baudrate_input.text()

        if not selected_baudrate.isdigit() or int(selected_baudrate) <= 0:
            self.baudrate_input_label.setText("Ошибка: Baudrate должен быть положительным числом")
            return
        else:
            self.baudrate_input_label.setText("Или введите Baudrate вручную:")

        self.selected_port = selected_port
        self.selected_baudrate = int(selected_baudrate)
        self.accept()  # Закрываем окно с успешным результатом

    def is_valid_port(self, port):
        # Проверка на корректность формата COM порта (например, COM1, COM2 и т.д.)
        pattern = r'^COM\d+$'
        return re.match(pattern, port) is not None

    @staticmethod
    def get_port_and_baudrate():
        # Проверяем, существует ли экземпляр QApplication
        app = QApplication.instance()
        app_created = False

        if not app:
            app = QApplication(sys.argv)
            app_created = True

        # Создаем и отображаем окно
        port_window = PortSelectionWindow()
        if port_window.exec():  # Ожидаем завершения окна
            selected_port = port_window.selected_port
            selected_baudrate = port_window.selected_baudrate
        else:
            selected_port = None
            selected_baudrate = None

        # Если QApplication был создан внутри, завершаем его
        if app_created:
            app.quit()

        return selected_port, selected_baudrate


# Использование в основном коде
if __name__ == "__main__":
    portName, baudrate = PortSelectionWindow.get_port_and_baudrate()
    if portName and baudrate:
        print(f"Подключение к порту: {portName} с baudrate: {baudrate}")
    else:
        print("Порт или baudrate не были выбраны.")
