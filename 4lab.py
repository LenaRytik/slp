import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex

# подрубаемся к базе данных SQLite
conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

# создаем таблицу posts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT
    )
''')
conn.commit() # фиксируем изменения в бд

# Модель данных для таблицы
class PostsTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data # тут хранятся данные

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self.rowCount() > 0 else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return str(self._data[row][column])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["ID", "User ID", "Заголовок", "Текст"][section]
            if orientation == Qt.Vertical:
                return str(section + 1)

# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # макет
        self.layout = QVBoxLayout(self.central_widget)

        # таблица для данных
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        # поле поиска
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Поиск по заголовку...")
        self.search_line_edit.textChanged.connect(self.filter_data)
        self.layout.addWidget(self.search_line_edit)

        # кнопки
        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.load_data)
        self.buttons_layout.addWidget(self.update_button)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)
        self.buttons_layout.addWidget(self.delete_button)

        # Загрузка данных
        self.load_data()

    def load_data(self):
        """Загрузка данных из базы данных в таблицу."""
        cursor.execute("SELECT * FROM posts")
        data = cursor.fetchall()
        self.model = PostsTableModel(data)
        self.table_view.setModel(self.model)

    def filter_data(self):
        """Поиска по заголовку."""
        search_text = self.search_line_edit.text().lower()
        cursor.execute("SELECT * FROM posts WHERE LOWER(title) LIKE ?", ('%' + search_text + '%',))
        filtered_data = cursor.fetchall()
        self.model = PostsTableModel(filtered_data)
        self.table_view.setModel(self.model)

    def add_record(self):
        """Добавление новой записи в базу данных."""
        user_id = 1  
        title = "Новый пост"
        body = "Содержание нового поста: пахпаххвывхахва"

        cursor.execute("INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)", (user_id, title, body))
        conn.commit()
        self.load_data()  

    def delete_record(self):
        """Удаление выбранной записи."""
        selected_row = self.table_view.currentIndex().row()
        if selected_row >= 0:
            post_id = self.model._data[selected_row][0]
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            conn.commit()
            self.load_data()  # обнова таблицы
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
