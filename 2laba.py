import socket
import threading
import time

# Флаг для управления работой серверов
server_running = True

# Функция для TCP-сервера
def start_tcp_server():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('localhost', 12345))
    tcp_socket.listen(1)  # Сервер ожидает одно подключение
    print("TCP-сервер готов к подключению...")

    # Основной цикл работы TCP-сервера
    while server_running:
        try:
            client_connection, client_address = tcp_socket.accept()  # Ожидание клиента сервер подверждает запрос
            print(f"Клиент подключен: {client_address}")

            # Получение сообщения от клиента
            client_message = client_connection.recv(1024).decode('utf-8')
            print(f"Принятое сообщение: {client_message}")

            # Отправка полученного сообщения обратно клиенту
            client_connection.sendall(client_message.encode('utf-8'))
            client_connection.close()  # Закрытие соединения
            print("Соединение с клиентом закрыто.")
        except OSError:
            break  # Завершаем сервер в случае ошибки

    tcp_socket.close()
    print("TCP-сервер остановлен.")

# Функция для TCP-клиента
def connect_tcp_client():
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect(('localhost', 12345))  # Подключение к TCP-серверу, клиент иницирует соединение
    client_message = "Привет, TCP-сервер!"
    tcp_client_socket.sendall(client_message.encode('utf-8'))  # Отправка сообщения серверу клиент подтверждает соединение
    
    # Получение ответа от сервера
    server_response = tcp_client_socket.recv(1024).decode('utf-8')
    print(f"Ответ от TCP-сервера: {server_response}")
    
    tcp_client_socket.close()

# Функция для UDP-сервера
def start_udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('localhost', 12346))  # Привязываем сокет к адресу и порту
    print("UDP-сервер готов к приёму данных...")

    # Основной цикл работы UDP-сервера
    while server_running:
        try:
            udp_data, udp_client_address = udp_socket.recvfrom(1024)  # Получение данных от клиента
            print(f"Данные получены от {udp_client_address}: {udp_data.decode('utf-8')}")
            udp_socket.sendto(udp_data, udp_client_address)  # Отправка данных обратно клиенту
        except OSError:
            break  # Завершаем сервер в случае ошибки

    udp_socket.close()
    print("UDP-сервер остановлен.")

# Функция для UDP-клиента
def connect_udp_client():
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_message = "Привет, UDP-сервер!"
    udp_client_socket.sendto(client_message.encode('utf-8'), ('localhost', 12346))  # Отправка данных на сервер
    
    # Получение ответа от сервера
    udp_response, udp_server = udp_client_socket.recvfrom(1024)
    print(f"Ответ от UDP-сервера: {udp_response.decode('utf-8')}")
    
    udp_client_socket.close()

if __name__ == "__main__":
    # Запуск TCP-сервера в отдельном потоке
    tcp_server_thread = threading.Thread(target=start_tcp_server)
    tcp_server_thread.start()

    # Даем серверу время для инициализации
    time.sleep(1)

    # Подключение TCP-клиента
    connect_tcp_client()

    # Запуск UDP-сервера в отдельном потоке
    udp_server_thread = threading.Thread(target=start_udp_server)
    udp_server_thread.start()

    # Даем серверу время для инициализации
    time.sleep(1)

    # Подключение UDP-клиента
    connect_udp_client()

    # Остановка работы серверов
    server_running = False
    tcp_server_thread.join()  # Ожидание завершения TCP-сервера
    udp_server_thread.join()  # Ожидание завершения UDP-сервера

    print("Все серверы остановлены. Программа завершена.")
