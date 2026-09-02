import socket
import json
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# НАСТРОЙКА: Укажите локальный IP-адрес вашего ПК в Wi-Fi сети (можно узнать через команду 'ip a')
PC_IP = "192.168.1.104"  
PORT = 9999

class MonitorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Меняем self.title на self.title_label (строка 21)
        self.title_label = Label(text="🎮 PC MONITOR", font_size='28sp', bold=True, color=get_color_from_hex('#00FFCC'))
        self.cpu_label = Label(text="CPU: ---", font_size='22sp', halign='left')
        self.ram_label = Label(text="RAM: ---", font_size='22sp', halign='left')
        self.status_label = Label(text="Статус: Подключение...", font_size='14sp', color=get_color_from_hex('#777777'))
        
        # И добавляем тоже self.title_label (строка 26)
        layout.add_widget(self.title_label)
        layout.add_widget(self.cpu_label)
        layout.add_widget(self.ram_label)
        layout.add_widget(self.status_label)
        
        threading.Thread(target=self.network_loop, daemon=True).start()
        
        return layout

    def network_loop(self):
        while True:
            try:
                # Пытаемся подключиться к серверу на ПК
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2.0) # Защита от долгого зависания, если ПК выключен
                s.connect((PC_IP, PORT))
                
                # Читаем ответ
                response = s.recv(1024).decode('utf-8')
                data = json.loads(response)
                s.close()
                
                # Передаем данные в основной поток интерфейса Kivy
                Clock.schedule_once(lambda dt: self.update_ui(data))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error())
                
            # Запрос каждые 2 секунды
            time.sleep(2)

    def update_ui(self, data):
        self.cpu_label.text = f"Процессор:  {data['cpu']}"
        self.ram_label.text = f"Память:  {data['ram']}"
        self.status_label.text = f"Обновлено: {data['time']}"
        self.status_label.color = get_color_from_hex('#00FF00')

    def show_error(self):
        self.status_label.text = "Нет связи с ПК. Повтор..."
        self.status_label.color = get_color_from_hex('#FF0033')

if __name__ == '__main__':
    MonitorApp().run()
