from comsel.portSelect import PortSelectionWindow  # Импортируем из пакета comsel

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    print(f"Selected COM port: {port}, Baud rate: {baudrate}")
else:
    print("No selection made.")
