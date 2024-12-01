from PyQt6.QtWidgets import QApplication, QMessageBox
from portSelect import PortSelectionWindow
import sys

app = QApplication(sys.argv)

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    QMessageBox.information(None, "Selection Complete", f"COM Port: {port}\nBaud Rate: {baudrate}")
else:
    QMessageBox.warning(None, "No Selection", "No COM port or baud rate was selected.")
