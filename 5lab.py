# Импорт библиотек
import sys  # Для работы с аргументами командной строки и выхода из приложения
import asyncio  # Для асинхронного выполнения кода
import aiohttp  # Для выполнения асинхронных HTTP-запросов
import aiosqlite  # Для работы с SQLite в асинхронном режиме
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QProgressBar, QWidget  # Для создания графического интерфейса
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer  # Для работы с потоками, сигналами и таймерами в PyQt5

# Класс потока для выполнения HTTP-запросов
class DataLoader(QThread):
    data_loaded = pyqtSignal(list)  # Сигнал для передачи загруженных данных в основной поток

    def run(self):
        asyncio.run(self.fetch_data())  # Запускаем асинхронную функцию для загрузки данных

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:  # Создаем асинхронную сессию HTTP
            async with session.get("https://jsonplaceholder.typicode.com/posts") as response:  # Выполняем GET-запрос
                data = await response.json()  # Преобразуем ответ в JSON
                self.data_loaded.emit(data)  # Передаем данные в основной поток через сигнал

# Класс потока для асинхронного сохранения данных в SQLite
class DataSaver(QThread):
    data_saved = pyqtSignal()  # Сигнал об успешном сохранении данных

    def __init__(self, data):
        super().__init__()
        self.data = data  # Данные для сохранения

    def run(self):
        asyncio.run(self.save_data())  # Запускаем асинхронную функцию для сохранения данных

    async def save_data(self):
        async with aiosqlite.connect("database.db") as db:  # Подключаемся к базе данных SQLite
            await db.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT)")  # Создаем таблицу, если она не существует
            await db.executemany("INSERT INTO posts (id, title) VALUES (?, ?)",
                                 [(item['id'], item['title']) for item in self.data])  # Вставляем данные в таблицу
            await db.commit()  # Фиксируем изменения в базе данных
            self.data_saved.emit()  # Передаем сигнал об успешном сохранении данных

# Основной класс приложения PyQt5
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронная загрузка данных")  # Устанавливаем заголовок окна
        
        # Настройка элементов интерфейса
        self.layout = QVBoxLayout()  # Создаем вертикальный макет

        # Кнопка для загрузки данных
        self.load_button = QPushButton("Загрузить данные")  # Создаем кнопку
        self.load_button.clicked.connect(self.load_data)  # Подключаем к функции load_data
        self.layout.addWidget(self.load_button)  # Добавляем кнопку в макет

        # Индикатор выполнения
        self.progress = QProgressBar()  # Создаем индикатор выполнения
        self.progress.setAlignment(Qt.AlignCenter)  # Выравниваем индикатор по центру
        self.layout.addWidget(self.progress)  # Добавляем индикатор в макет

        # Метка для отображения статуса
        self.status_label = QLabel("Ожидание загрузки данных...")  # Создаем метку
        self.layout.addWidget(self.status_label)  # Добавляем метку в макет

        self.setLayout(self.layout)  # Устанавливаем макет для окна

        # Создаем таймер для проверки обновлений
        self.timer = QTimer()  # Создаем таймер
        self.timer.timeout.connect(self.load_data)  # Подключаем таймер к функции load_data
        self.timer.start(10000)  # Запускаем таймер с интервалом 10 секунд

    # Функция для запуска загрузки данных в отдельном потоке
    def load_data(self):
        self.progress.setValue(0)  # Обнуляем индикатор выполнения
        self.status_label.setText("Загрузка данных...")  # Обновляем текст метки
        
        # Запускаем DataLoader
        self.loader = DataLoader()  # Создаем экземпляр DataLoader
        self.loader.data_loaded.connect(self.on_data_loaded)  # Подключаем сигнал к функции обработки данных
        self.loader.start()  # Запускаем поток

    # Обработка данных после загрузки
    def on_data_loaded(self, data):
        self.status_label.setText("Сохранение данных...")  # Обновляем текст метки
        self.progress.setValue(50)  # Обновляем индикатор выполнения

        # Запускаем DataSaver
        self.saver = DataSaver(data)  # Создаем экземпляр DataSaver с загруженными данными
        self.saver.data_saved.connect(self.on_data_saved)  # Подключаем сигнал к функции обработки завершения сохранения
        self.saver.start()  # Запускаем поток

    # Обновление интерфейса после успешного сохранения данных
    def on_data_saved(self):
        self.status_label.setText("Данные успешно сохранены в базу данных")  # Обновляем текст метки
        self.progress.setValue(100)  # Устанавливаем индикатор выполнения на 100

# Запуск приложения
app = QApplication(sys.argv)  # Создаем приложение PyQt5
window = MainWindow()  # Создаем главное окно
window.show()  # Показываем окно
sys.exit(app.exec_())  # Запускаем основной цикл приложения и завершаем работу при закрытии окна
