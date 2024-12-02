import serial
from comsel.portSelect import PortSelectionWindow  # Импортируем из пакета comsel

def connect_and_read(port, baudrate):
    try:
        # Открываем соединение с выбранным COM портом
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud.")

            while True:
                # Читаем данные из порта
                data = ser.readline().decode('utf-8').strip()  # Считываем строку данных
                if data:
                    print(f"Received: {data}")  # Выводим данные в консоль
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nDisconnected from port.")

if __name__ == "__main__":
    # Получаем порт и битрейт из окна выбора
    port, baudrate = PortSelectionWindow.get_port_and_baudrate()
    if port and baudrate:
        connect_and_read(port, baudrate)
    else:
        print("No COM port or baudrate selected.")
