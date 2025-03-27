import sys
import psycopg2
from psycopg2 import sql
import hashlib
from datetime import datetime, timedelta

from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,
    QDateEdit, QDateTimeEdit, QTabWidget, QWidget, QFormLayout, QDialogButtonBox, QHBoxLayout,
)
from PySide6.QtCore import Qt, QDate

# Конфигурация БД
DB_CONFIG = {
    "dbname": "marketing_service",
    "user": "marketing_service",
    "password": "1234",
    "host": "localhost",
    "client_encoding": "UTF8"
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class AddDialog(QDialog):
    def __init__(self, table_name, columns):
        super().__init__()
        self.table_name = table_name
        self.columns = columns
        self.setWindowTitle(f"Добавить в {table_name}")
        self.layout = QVBoxLayout()
        self.fields = {}

        # Исключаем временные поля
        excluded_columns = {
            "created_at", "order_date", "distribution_date",
            "start_date", "end_date", "published_date",
            "user_id", "administrator_id", "author_id", "book_id",
            "customer_id", "marketer_id",
            "material_id", "order_id"
        }

        for col in columns:
            if col in excluded_columns:
                continue  # Пропускаем временные поля

            if col == 'role' and self.table_name == 'users':
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["Администратор", "Маркетолог", "Клиент"])
            elif col == 'material_type' and self.table_name == 'marketing_materials':
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["Email", "Баннер", "Видео", "Соцсети", "Брошюра", "Радио", "Landing Page", "Печать", "Вебинар", "Мобильное приложение"])
            elif col == 'campaign_id' and self.table_name in ['marketing_materials', 'orders']:
                self.fields[col] = QComboBox()
                self.load_foreign_key_options('campaigns', 'campaign_id', 'campaign_name')
            elif col == 'department' and self.table_name in ['marketers']:
                self.fields[col] = QComboBox()
                self.fields[col].addItems(
                    ["Digital", "SMM", "SEO", "Контент", "Аналитика", "PR", "Email", "PPC", "Видео",
                     "Мобильное"])
            elif col == 'genre' and self.table_name in ['books']:
                self.fields[col] = QComboBox()
                self.fields[col].addItems(
                    ["Роман", "Пьеса", "Повесть", "Роман в стихах", "Поэма", "Художественно-историческое"])
            elif col == 'genre' and self.table_name in ['orders']:
                self.fields[col] = QComboBox()
                self.fields[col].addItems(
                    ["Роман", "Пьеса", "Повесть", "Роман в стихах", "Поэма", "Художественно-историческое"])
            else:
                self.fields[col] = QLineEdit()

            label = QLabel(col.replace('_', ' ').title())
            self.layout.addWidget(label)
            self.layout.addWidget(self.fields[col])

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_save)
        self.setLayout(self.layout)



    def load_foreign_key_options(self, table, id_col, display_col):
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("SELECT {id}, {display} FROM {table}").format(
                        id=sql.Identifier(id_col),
                        display=sql.Identifier(display_col),
                        table=sql.Identifier(table)
                    )
                    cursor.execute(query)
                    options = cursor.fetchall()
                    self.fields[id_col].addItems([f"{opt[0]} - {opt[1]}" for opt in options])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def get_data(self):
        data = {}
        for col, field in self.fields.items():
            if isinstance(field, QComboBox):
                data[col] = field.currentText().split(' - ')[0]
            else:
                data[col] = field.text()
        return data

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.input_login = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.input_login)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.input_password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.authenticate)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def authenticate(self):
        """Аутентификация пользователя"""
        login = self.input_login.text()
        password = hash_password(self.input_password.text())

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    # Запрос для получения данных пользователя
                    query = """
                        SELECT u.user_id, u.role, a.administrator_id, m.marketer_id, c.customer_id
                        FROM users u
                        LEFT JOIN administrators a ON u.user_id = a.user_id
                        LEFT JOIN marketers m ON u.user_id = m.user_id
                        LEFT JOIN customers c ON u.user_id = c.user_id
                        WHERE u.username = %s AND u.password_hash = %s
                    """
                    cursor.execute(query, (login, password))
                    user = cursor.fetchone()

            if user:
                user_id, role, admin_id, marketer_id, customer_id = user

                if role == 'Администратор':
                    QMessageBox.information(self, "Успех", "Вход выполнен как Администратор")
                    self.admin_window = AdminWindow()
                    self.admin_window.show()
                elif role == 'Маркетолог':
                    QMessageBox.information(self, "Успех", "Вход выполнен как Маркетолог")
                    self.marketer_window = MarketerWindow(marketer_id)
                    self.marketer_window.show()
                elif role == 'Клиент':
                    QMessageBox.information(self, "Успех", "Вход выполнен как Клиент")
                    self.customer_window = CustomerWindow(customer_id)
                    self.customer_window.show()

                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def open_admin_window(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()

    def open_marketer_window(self, marketer_id):
        self.marketer_window = MarketerWindow(marketer_id)
        self.marketer_window.show()

    def open_customer_window(self, customer_id):
        self.customer_window = CustomerWindow(customer_id)
        self.customer_window.show()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Администратор")
        self.setGeometry(200, 200, 1000, 700)

        # Центральный виджет и layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Панель управления (toolbar)
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.addItems([
            "users", "administrators", "authors", "books",
            "campaigns", "customers", "marketers",
            "marketing_materials", "orders"
        ])
        self.toolbar_layout.addWidget(QLabel("Таблица:"))
        self.toolbar_layout.addWidget(self.table_combo)

        # Кнопки управления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")

        self.toolbar_layout.addWidget(self.btn_refresh)
        self.toolbar_layout.addWidget(self.btn_add)
        self.toolbar_layout.addWidget(self.btn_edit)
        self.toolbar_layout.addWidget(self.btn_delete)

        self.toolbar.setLayout(self.toolbar_layout)
        self.layout.addWidget(self.toolbar)

        # Таблица данных
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Установка layout в центральный виджет
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Привязка событий
        self.table_combo.currentTextChanged.connect(self.load_data)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        # Загрузка данных при старте
        self.load_data()

    def load_data(self):
        """Загружает данные из выбранной таблицы"""
        table = self.table_combo.currentText()
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

                    # Настройка таблицы
                    self.table.setColumnCount(len(col_names))
                    self.table.setHorizontalHeaderLabels(col_names)
                    self.table.setRowCount(len(rows))

                    for row_idx, row in enumerate(rows):
                        for col_idx, value in enumerate(row):
                            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def add_record(self):
        """Добавляет новую запись в выбранную таблицу"""
        table = self.table_combo.currentText()

        try:
            # Получаем список столбцов для выбранной таблицы
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = %s
                        ORDER BY ordinal_position
                        """,
                        (table,)
                    )
                    columns = [col[0] for col in cursor.fetchall()]

            # Создаем диалоговое окно с полученными столбцами
            dialog = AddDialog(table, columns)
            if dialog.exec():
                data = dialog.get_data()

                # Формируем SQL-запрос для добавления записи
                columns_str = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

                try:
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute(query, list(data.values()))
                            conn.commit()
                            self.load_data()  # Обновляем таблицу после добавления
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные о таблице: {str(e)}")

    def edit_record(self):
        """Редактирует выбранную запись"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()  # Первый столбец — ID
        id_value = self.table.item(selected_row, 0).text()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    # Получаем список столбцов таблицы
                    cursor.execute(
                        """
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = %s
                        ORDER BY ordinal_position
                        """,
                        (table,)
                    )
                    columns = [col[0] for col in cursor.fetchall()]

                    # Получаем текущую запись
                    query = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
                        sql.SQL(", ").join(map(sql.Identifier, columns)),
                        sql.Identifier(table),
                        sql.Identifier(id_col)
                    )
                    cursor.execute(query, (id_value,))
                    record = cursor.fetchone()

            # Создаем диалоговое окно редактирования
            dialog = QDialog()
            dialog.setWindowTitle(f"Редактирование записи в {table}")
            layout = QVBoxLayout()

            fields = {}
            for idx, col in enumerate(columns):
                label = QLabel(col.replace('_', ' ').title())
                layout.addWidget(label)

                if col == id_col:
                    # Пропускаем ID-поле (оно не редактируется)
                    continue

                if col == 'role' and table == 'users':
                    # Выпадающий список для ролей
                    fields[col] = QComboBox()
                    fields[col].addItems(["Администратор", "Маркетолог", "Клиент"])
                    fields[col].setCurrentText(str(record[idx]) if record[idx] is not None else "")
                elif col == 'material_type' and table == 'marketing_materials':
                    # Выпадающий список для типов маркетинговых материалов
                    fields[col] = QComboBox()
                    fields[col].addItems([
                        "Email", "Баннер", "Видео", "Соцсети", "Брошюра",
                        "Радио", "Landing Page", "Печать", "Вебинар", "Мобильное приложение"
                    ])
                    fields[col].setCurrentText(str(record[idx]) if record[idx] is not None else "")
                elif col in ['start_date', 'end_date', 'distribution_date', 'order_date']:
                    # Поле для даты
                    fields[col] = QDateEdit(calendarPopup=True)
                    fields[col].setDisplayFormat("yyyy-MM-dd")
                    if record[idx]:
                        fields[col].setDate(QDate.fromString(str(record[idx]), "yyyy-MM-dd"))
                    else:
                        fields[col].setDate(QDate.currentDate())
                elif col == 'budget' and table == 'campaigns':
                    # Поле для бюджета с валидацией
                    fields[col] = QLineEdit()
                    fields[col].setValidator(QDoubleValidator(0.0, 9999999.99, 2))
                    fields[col].setText(str(record[idx]) if record[idx] is not None else "")
                else:
                    # Обычное текстовое поле
                    fields[col] = QLineEdit(str(record[idx]) if record[idx] is not None else "")

                layout.addWidget(fields[col])

            # Кнопка "Сохранить"
            btn_save = QPushButton("Сохранить")
            btn_save.clicked.connect(dialog.accept)
            layout.addWidget(btn_save)

            dialog.setLayout(layout)

            # Если пользователь нажал "Сохранить"
            if dialog.exec():
                data = {}
                for col, field in fields.items():
                    if isinstance(field, QComboBox):
                        data[col] = field.currentText()
                    elif isinstance(field, QDateEdit):
                        data[col] = field.date().toString("yyyy-MM-dd")
                    else:
                        data[col] = field.text()

                try:
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cursor:
                            # Формируем SQL-запрос для обновления записи
                            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
                            query = f"UPDATE {table} SET {set_clause} WHERE {id_col} = %s"
                            cursor.execute(query, list(data.values()) + [id_value])
                            conn.commit()
                            self.load_data()  # Обновляем таблицу после редактирования
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные о записи: {str(e)}")

    def delete_record(self):
        """Удаляет выбранную запись и обновляет последовательность"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранную запись?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        # Удаляем запись
                        cursor.execute(f"DELETE FROM {table} WHERE {id_col} = %s", (id_value,))

                        # Обновляем последовательность
                        sequence_name = f"{table}_{id_col}_seq"
                        cursor.execute(f"""
                            SELECT setval('{sequence_name}', (SELECT COALESCE(MAX({id_col}), 0) + 1 FROM {table}));
                        """)

                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
class MarketerWindow(QMainWindow):
    def __init__(self, marketer_id):
        super().__init__()
        self.marketer_id = marketer_id  # ID текущего маркетолога
        self.setWindowTitle("Маркетолог")
        self.setGeometry(200, 200, 800, 600)

        # Центральный виджет и layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Панель управления (toolbar)
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.addItems(["campaigns", "marketing_materials"])
        self.toolbar_layout.addWidget(QLabel("Таблица:"))
        self.toolbar_layout.addWidget(self.table_combo)

        # Кнопки управления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        self.toolbar_layout.addWidget(self.btn_refresh)
        self.toolbar_layout.addWidget(self.btn_add)
        self.toolbar_layout.addWidget(self.btn_edit)
        self.toolbar_layout.addWidget(self.btn_delete)

        # Установка layout для панели инструментов
        self.toolbar.setLayout(self.toolbar_layout)
        self.layout.addWidget(self.toolbar)

        # Таблица данных
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Установка layout в центральный виджет
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Привязка событий
        self.table_combo.currentTextChanged.connect(self.load_data)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        # Загрузка данных при старте
        self.load_data()

    def load_data(self):
        """Загружает данные из выбранной таблицы"""
        table = self.table_combo.currentText()
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    if table == "marketing_materials":
                        query = """
                            SELECT m.material_id, c.campaign_name, m.material_type, m.content, m.distribution_date
                            FROM marketing_materials m
                            JOIN campaigns c ON m.campaign_id = c.campaign_id
                            WHERE c.marketer_id = %s
                        """
                        cursor.execute(query, (self.marketer_id,))
                    elif table == "campaigns":
                        query = """
                            SELECT campaign_id, campaign_name, start_date, end_date, budget, description
                            FROM campaigns
                            WHERE marketer_id = %s
                        """
                        cursor.execute(query, (self.marketer_id,))
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

            # Настройка таблицы
            self.table.setColumnCount(len(col_names))
            self.table.setHorizontalHeaderLabels(col_names)
            self.table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def add_record(self):
        """Добавляет новую запись в выбранную таблицу"""
        table = self.table_combo.currentText()
        if table == "campaigns":
            # Диалоговое окно для добавления кампании
            dialog = AddDialog("campaigns", ["campaign_name", "budget", "description"])
        elif table == "marketing_materials":
            # Диалоговое окно для добавления маркетинговых материалов
            dialog = AddDialog("marketing_materials", ["campaign_id", "material_type", "content"])
            dialog.fields["campaign_id"].addItems(self.get_marketer_campaigns())  # Загружаем доступные кампании

        if dialog.exec():
            data = dialog.get_data()

            # Автоматическое добавление временных данных
            if table == "campaigns":
                data["start_date"] = datetime.now().strftime("%Y-%m-%d")
                data["end_date"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                data["marketer_id"] = self.marketer_id  # Привязываем кампанию к текущему маркетологу
            elif table == "marketing_materials":
                data["distribution_date"] = datetime.now().strftime("%Y-%m-%d")

            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        # Формируем SQL-запрос
                        columns = ', '.join(data.keys())
                        placeholders = ', '.join(['%s'] * len(data))
                        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                        cursor.execute(query, list(data.values()))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def edit_record(self):
        """Редактирует выбранную запись"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected_row, 0).text()

        if table == "campaigns":
            dialog = AddDialog("campaigns", ["campaign_name", "start_date", "end_date", "budget", "description"])
        elif table == "marketing_materials":
            dialog = AddDialog("marketing_materials", ["campaign_id", "material_type", "content"])
            dialog.fields["campaign_id"].addItems(self.get_marketer_campaigns())

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table} WHERE {id_col} = %s", (id_value,))
                    record = cursor.fetchone()

            for idx, col in enumerate(dialog.fields):
                if isinstance(col, QLineEdit):
                    col.setText(str(record[idx]))
                elif isinstance(col, QComboBox):
                    col.setCurrentText(str(record[idx]))

            if dialog.exec():
                data = dialog.get_data()

                try:
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cursor:
                            if table == "campaigns":
                                query = """
                                    UPDATE campaigns 
                                    SET campaign_name = %s, start_date = %s, end_date = %s, budget = %s, description = %s
                                    WHERE campaign_id = %s
                                """
                                cursor.execute(query, (
                                    data['campaign_name'], data['start_date'], data['end_date'],
                                    data['budget'], data['description'], id_value
                                ))
                            elif table == "marketing_materials":
                                query = """
                                    UPDATE marketing_materials 
                                    SET campaign_id = %s, material_type = %s, content = %s
                                    WHERE material_id = %s
                                """
                                cursor.execute(query, (
                                    data['campaign_id'], data['material_type'], data['content'], id_value
                                ))
                            conn.commit()
                            self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_record(self):
        """Удаляет выбранную запись"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранную запись?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(f"DELETE FROM {table} WHERE {id_col} = %s", (id_value,))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def get_marketer_campaigns(self):
        """Возвращает список кампаний текущего маркетолога"""
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT campaign_id, campaign_name
                        FROM campaigns
                        WHERE marketer_id = %s
                    """
                    cursor.execute(query, (self.marketer_id,))
                    campaigns = cursor.fetchall()
                    return [f"{name} ({id})" for id, name in campaigns]
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить кампании: {str(e)}")
            return []


class CustomerWindow(QMainWindow):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id  # ID текущего клиента
        self.setWindowTitle("Клиент")
        self.setGeometry(200, 200, 800, 600)

        # Центральный виджет и layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Панель управления (toolbar)
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.addItems(["orders", "books", "authors"])
        self.toolbar_layout.addWidget(QLabel("Таблица:"))
        self.toolbar_layout.addWidget(self.table_combo)

        # Кнопки управления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        self.toolbar_layout.addWidget(self.btn_refresh)
        self.toolbar_layout.addWidget(self.btn_add)
        self.toolbar_layout.addWidget(self.btn_edit)
        self.toolbar_layout.addWidget(self.btn_delete)

        # Установка layout для панели инструментов
        self.toolbar.setLayout(self.toolbar_layout)
        self.layout.addWidget(self.toolbar)

        # Таблица данных
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Установка layout в центральный виджет
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Привязка событий
        self.table_combo.currentTextChanged.connect(self.load_data)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        # Загрузка данных при старте
        self.load_data()

    def load_data(self):
        """Загружает данные из выбранной таблицы"""
        table = self.table_combo.currentText()
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    if table == "orders":
                        query = """
                            SELECT order_id, order_date, total_amount, title, genre
                            FROM orders
                            WHERE customer_id = %s
                        """
                        cursor.execute(query, (self.customer_id,))
                    elif table == "books":
                        query = """
                            SELECT book_id, title, author_id, genre, published_date, price, stock
                            FROM books
                        """
                        cursor.execute(query)
                    elif table == "authors":
                        query = """
                            SELECT author_id, first_name, last_name, bio
                            FROM authors
                        """
                        cursor.execute(query)
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

            # Настройка таблицы
            self.table.setColumnCount(len(col_names))
            self.table.setHorizontalHeaderLabels(col_names)
            self.table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def add_record(self):
        """Добавляет новую запись в выбранную таблицу"""
        table = self.table_combo.currentText()
        if table == "orders":
            dialog = AddDialog("orders", ["book_id", "title", "genre", "total_amount"])

        else:
            QMessageBox.warning(self, "Ошибка", f"Добавление данных в таблицу '{table}' недоступно.")
            return

        if dialog.exec():
            data = dialog.get_data()
            data["customer_id"] = self.customer_id  # Привязываем запись к текущему клиенту

            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        columns = ', '.join(data.keys())
                        placeholders = ', '.join(['%s'] * len(data))
                        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                        cursor.execute(query, list(data.values()))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def edit_record(self):
        """Редактирует выбранную запись"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected_row, 0).text()

        if table == "orders":
            dialog = AddDialog("orders", ["book_id", "quantity"])
        else:
            QMessageBox.warning(self, "Ошибка", f"Редактирование данных в таблице '{table}' недоступно.")
            return

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table} WHERE {id_col} = %s", (id_value,))
                    record = cursor.fetchone()

            for idx, col in enumerate(dialog.fields):
                if isinstance(col, QLineEdit):
                    col.setText(str(record[idx]))
                elif isinstance(col, QComboBox):
                    col.setCurrentText(str(record[idx]))

            if dialog.exec():
                data = dialog.get_data()

                try:
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cursor:
                            query = f"UPDATE {table} SET "
                            updates = []
                            for key, value in data.items():
                                updates.append(f"{key} = %s")
                            query += ", ".join(updates)
                            query += f" WHERE {id_col} = %s"
                            cursor.execute(query, list(data.values()) + [id_value])
                            conn.commit()
                            self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_record(self):
        """Удаляет выбранную запись"""
        table = self.table_combo.currentText()
        if table == "orders":
            dialog = AddDialog("orders", ["book_id", "title", "genre", "total_amount"])

        else:
            QMessageBox.warning(self, "Ошибка", f"Удаление данных в таблицу '{table}' недоступно.")
            return
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        table = self.table_combo.currentText()
        id_col = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранную запись?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(f"DELETE FROM {table} WHERE {id_col} = %s", (id_value,))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())