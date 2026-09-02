import socket
import json
import time
import psutil

PORT = 9999  # Порт, который мы откроем в локальной сети для телефона

def get_system_stats():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    return {
        "cpu": f"{cpu}%",
        "ram": f"{ram}%",
        "time": time.strftime("%H:%M:%S")
    }

def start_server():
    # Создаем стандартный сетевой сокет (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Слушаем все входящие соединения на порту 9999
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"[*] Сервер пет-проекта запущен на порту {PORT}. Ожидание телефона...")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"[*] Телефон подключился: {addr}")
            
            # Как только телефон подключился, шлем ему JSON-строку с данными
            stats = get_system_stats()
            data = json.dumps(stats)
            client_socket.sendall(data.encode('utf-8'))
            
            # Закрываем сессию, ждем следующего запроса
            client_socket.close()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка сокета: {e}")

if __name__ == "__main__":
    start_server()