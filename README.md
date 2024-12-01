Вот обновленный `README.md` файл с учетом структуры вашего проекта и добавленных примеров:

---

```markdown
# COM Port Selection Tool

This is a PyQt6-based GUI application for selecting COM ports and setting the baud rate. It is designed for ease of use
in Python projects that require serial communication. The tool allows dynamic detection of available COM ports, error
handling for invalid input, and a clean modern interface.

![Screenshot](./docs/app_screenshot.png)


---

## Features

- **Dynamic COM Port Detection:** Automatically updates the list of available COM ports every second.
- **Custom Input:** Allows manual entry of COM port and baud rate.
- **Error Handling:** Validates user input for both COM port and baud rate.
- **Professional Interface:** Includes a white-blue modern design with an application icon.

---

## Requirements

- Python 3.9 or higher
- PyQt6
- pyserial

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/com-port-selection-tool.git
cd com-port-selection-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

Run the main script to launch the COM Port Selection Tool:

```bash
python portSelect.py
```

The application window will appear, allowing you to select a COM port and baud rate.

---

## Examples

This repository includes example scripts to demonstrate the usage of the COM Port Selection Tool. Examples are located
in the `examples/` directory:

### 1. **Basic Usage**

This script demonstrates the simplest way to use the tool. It selects a COM port and baud rate and prints the results to
the console.

```bash
python examples/basic_usage.py
```

**Code:**

```python
from portSelect import PortSelectionWindow

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    print(f"Selected COM port: {port}, Baud rate: {baudrate}")
else:
    print("No selection made.")
```

---

### 2. **GUI Output**

This script displays the selected COM port and baud rate in a graphical message box.

```bash
python examples/gui_output.py
```

**Code:**

```python
from PyQt6.QtWidgets import QApplication, QMessageBox
from portSelect import PortSelectionWindow
import sys

app = QApplication(sys.argv)

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    QMessageBox.information(None, "Selection Complete", f"COM Port: {port}\nBaud Rate: {baudrate}")
else:
    QMessageBox.warning(None, "No Selection", "No COM port or baud rate was selected.")
```

---

### 3. **Read Data from COM Port**

This script connects to the selected COM port and continuously reads data, printing it to the console.

```bash
python examples/read_from_port.py
```

**Code:**

```python
import serial
from portSelect import PortSelectionWindow


def connect_and_read(port, baudrate):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud.")

            while True:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Received: {data}")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nDisconnected from port.")


if __name__ == "__main__":
    port, baudrate = PortSelectionWindow.get_port_and_baudrate()
    if port and baudrate:
        connect_and_read(port, baudrate)
    else:
        print("No COM port or baud rate selected.")
```

---

## File Structure

```
com-port-selection-tool/
├── .venv/                      # Virtual environment (optional, not included in repo)
├── docs/
│   └── screenshot.png          # Screenshot of the application
├── examples/
│   ├── basic_usage.py          # Example 1: Basic usage
│   ├── gui_output.py           # Example 2: GUI output
│   └── read_from_port.py       # Example 3: Reading data from COM port
├── icons/
│   └── icon.ico                # Application icon
├── portSelect.py               # Main script (contains PortSelectionWindow class)
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to submit issues or pull requests if you find any bugs or want to add features.

```
