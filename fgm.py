import sys

import math
import numpy as np
import plotly
import plotly.graph_objects as go
import sqlite3

from PyQt5.QtWidgets import QApplication, QLabel, QTabWidget, QTableView  #, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QComboBox, QHeaderView
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


# Главная форма приложения
class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

# Настройка интерфейса главной формы
    def initUI(self):
        self.setGeometry(200, 80, 1000, 700)
        self.setWindowTitle('Исследование неизведанных планет')
        self.setWindowIcon(QIcon('resources/pic/promo.jpg'))

    # Заголовок легенды на главной форме
        self.title_0 = QLabel(self)
        self.title_0.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont()
        font1.setPointSize(20)
        self.title_0.setFont(font1)
        self.title_0.setTextFormat(QtCore.Qt.AutoText)
        self.title_0.setText('Исследование неизведанных планет')

        self.title = QLabel(self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont()
        font1.setPointSize(12)
        self.title.setFont(font1)
        self.title.setTextFormat(QtCore.Qt.AutoText)
        self.title.setText('По мотивам задачи второго этапа профиля "Большие данные" '
                           'Национальной технологической олимпиады')

    # Графическая заставка на главной форме
        self.pixmap = QPixmap('resources/pic/promo.jpg')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.resize(800, 450)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

    # Легенда
        self.legend = QLabel(self)
        self.legend.setAlignment(QtCore.Qt.AlignHCenter)
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.legend.setFont(font2)
        self.legend.setText('Совсем недавно была открыта новая система планет, '
                           'к которой было принято решение направить\nкосмические аппараты '
                            'с необходимым исследовательским оборудоваением.\n\n'
                            'Сначала на каждую планету для разведки отправляется множество '
                            'простых космических аппаратов.\nКаждый такой аппарат приземляется '
                            'в случайную точку планеты и сообщает свои координаты на Землю,\n'
                            'если посадка была успешной. Аппараты просты и надёжны, успешность '
                            'посадки зависит только от особенностей\nландшафта в месте посадки. '
                            'Все аппараты используют для позиционирования единую систему '
                            'координат.\nПосле сбора статистики принято решение отправить '
                            'более продвинутые космические аппараты.\nПроанализируйте данные '
                            'с тем, чтобы для выбранных координат определить успешность посадки.')

    # Кнопка Начать исследование
        self.button = QPushButton('Начать исследование', self)
        self.button.clicked.connect(self.open_form1)

    # Компановка всех элементов главной формы в вертикальный бокс
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title_0)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.image)
        self.vbox.addWidget(self.legend)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)

    def open_form1(self):
        self.first_form = FirstForm(self, None)
        self.first_form.show()
        self.close()


# Форма основного меню приложения (Исследование)
class FirstForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(200, 100, 260, 360)
        self.setWindowTitle('Исследование')
        self.setWindowIcon(QIcon('resources/pic/01.png'))
        self.setFixedSize(260, 360)

        self.button1 = QPushButton('Работа с данными', self)
        self.button1.setGeometry(QtCore.QRect(30, 30, 200, 60))
        self.button1.clicked.connect(self.open_form_tables)

        self.button2 = QPushButton('Визулизация\nрезультатов миссий', self)
        self.button2.setGeometry(QtCore.QRect(30, 110, 200, 60))
        self.button2.clicked.connect(self.open_form_visual)

        self.button3 = QPushButton('Определение\nуспешности посадки', self)
        self.button3.setGeometry(QtCore.QRect(30, 190, 200, 60))
        self.button3.clicked.connect(self.open_form_predict)

        self.button4 = QPushButton('Завершить\nисследование', self)
        self.button4.setGeometry(QtCore.QRect(30, 270, 200, 60))
        self.button4.clicked.connect(sys.exit)

    def open_form_visual(self):
        self.second_form = VisualForm(self)
        self.second_form.show()

    def open_form_tables(self):
        self.third_form = TabsForm(self)
        self.third_form.show()

    def open_form_predict(self):
        self.fourth_form = PredictForm(self)
        self.fourth_form.show()


# Форма для предсказания успешности посадки на планету по введенным координатам
class PredictForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
    # Подключение к БД
        con = sqlite3.connect('resources/bd/uncharted_planets.db')
    # Создание курсора
        cur = con.cursor()
    # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT title FROM planets""").fetchall()
        con.close()
        lst = [x[0] for x in result]

        self.setGeometry(500, 100, 500, 200)
        self.setWindowTitle('Предсказание успешности посадки на плвнету')
        self.setWindowIcon(QIcon('resources/pic/05.png'))

        self.setFixedSize(500, 200)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.form = QFormLayout()

    # Выбор планеты из списка
        self.label_1 = QLabel()
        self.label_1.setText('Выберите планету для вычислительного эксперимента')
        self.hbox.addWidget(self.label_1, alignment=QtCore.Qt.AlignTop)
        self.box = QComboBox()
        self.box.addItems(lst)
        self.box.setCurrentIndex(0)
        self.form.addRow(self.hbox)

        self.hbox.addWidget(self.box, alignment=QtCore.Qt.AlignTop)
        self.hbox.setContentsMargins(40, 30, 100, 30)

    # Задать долготу и широту возможного места посадки
        self.input_value_1 = QLineEdit(self)
        self.input_value_2 = QLineEdit(self)
        self.form.addRow('Введите долготу места посадки (целое значение в диапазоне от -180 до 180):',
                         self.input_value_1)
        self.form.addRow('Введите широту места посадки (целое значение в диапазоне от -90 до 90):',
                         self.input_value_2)
        self.input_value_1.setText('0')
        self.input_value_2.setText('0')
        self.input_value_1.setValidator(QtGui.QIntValidator(-180, 180))
        self.input_value_2.setValidator(QtGui.QIntValidator(-90, 90))

        self.button = QPushButton('Предсказать успешность посадки')
        self.hbox2 = QHBoxLayout()
        self.hbox.addWidget(self.button)
        self.form.addRow(self.button)
        self.button.clicked.connect(self.predict)

        self.setLayout(self.form)

    def predict(self):

        def dist(a, b):
            return math.acos(round(math.sin(a[0] * math.pi / 180) * math.sin(b[0] * math.pi / 180) +
                                   math.cos(a[0] * math.pi / 180) * math.cos(b[0] * math.pi / 180) *
                                   math.cos((a[1] - b[1]) * math.pi / 180), 4))

        def ray_tracing_method(x, y, poly):
            n = len(poly)
            inside = False

            p1x, p1y = poly[0]
            for i in range(n + 1):
                p2x, p2y = poly[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= xints:
                                inside = not inside
                p1x, p1y = p2x, p2y
            if inside:
                return 1
            else:
                return 0

        def ans(n):
            triang = []
            for i in range(1000):
                if dist(n, coor[i]) <= 0.08:
                    triang.append(coor[i])
            if len(triang) == 0:
                return 0
            for i in range(len(triang)):
                if dist(n, triang[i]) <= 0.56:
                    return 1
            return ray_tracing_method(n[0], n[1], triang)

        if (not self.input_value_1.hasAcceptableInput() or
            not self.input_value_2.hasAcceptableInput()):
            QMessageBox.information(self, 'Предупреждение', 'Неверный формат введенных данных',
                                    buttons=QMessageBox.Close)
        else:
            # чтение данных об успешных посадках на планету n
            n = self.box.currentIndex()
            fname = 'resources/data/' + str(n + 1) + '.txt'
            coor = np.genfromtxt(fname)
            x = y = 0
            x = int(self.input_value_1.text())
            y = int(self.input_value_2.text())
#            print(x, y, ans([x, y]))
            if ans([x, y]) == 1:
                res = 'успешна'
                QMessageBox.information(self, 'Результат', 'Посадка аппарата в данной точке планеты' +
                                        ' будет ' + res, buttons=QMessageBox.Ok)
            else:
                res = 'неуспешна'
                QMessageBox.critical(self, 'Результат', 'Посадка аппарата в данной точке планеты' +
                                        ' будет ' + res, buttons=QMessageBox.Ok)



# Форма для работы с базой данных о неизведанных планетах
class TabsForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
    # Зададим тип базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
    # Укажем имя базы данных
        self.db.setDatabaseName('resources/bd/uncharted_planets.db')
    # И откроем подключение
        self.db.open()

    # Создадим объект QSqlTableModel,
    # зададим таблицу, с которой он будет работать, и выберем все данные
    # для данных о планетах
        self.model_planets = QSqlTableModel(self, self.db)
        self.model_planets.setTable('planets')
        self.model_planets.select()

    # для данных о миссиях
        self.model_missions = QSqlTableModel(self, self.db)
        self.model_missions.setTable('missions')
        self.model_missions.select()

    # для данных о посадках на планеты
        self.model_landings = QSqlTableModel(self, self.db)
        self.model_landings.setTable('landings')
        self.model_landings.select()

        self.setGeometry(500, 100, 730, 700)
        self.setWindowTitle('База данных о неизведанных планетах')
        self.setWindowIcon(QIcon('resources/pic/02.png'))

    # QTableView - виджет для отображения данных из базы
        self.view_planets = QTableView()
        self.view_missions = QTableView()
        self.view_landings = QTableView()

        self.model_planets.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        self.model_planets.setHeaderData(1, QtCore.Qt.Horizontal, 'Название\nпланеты')
        self.model_planets.setHeaderData(2, QtCore.Qt.Horizontal, 'Среднее расстояние\nот звезды планетарной\nсистемы, а.е.')
        self.model_planets.setHeaderData(3, QtCore.Qt.Horizontal, 'Средняя скорость\nорбитального\nдвижения, км/с')
        self.model_planets.setHeaderData(4, QtCore.Qt.Horizontal, 'Период обращения\nвокруг звезды, сут.')
        self.model_planets.setHeaderData(5, QtCore.Qt.Horizontal, 'Период вращения\nвокруг оси, дней')
        self.model_planets.setHeaderData(6, QtCore.Qt.Horizontal, 'Наклон экватора\nк орбите, град.')

    # Горизонтальная метка расширяет остальную часть окна и заполняет форму
        self.view_planets.horizontalHeader().setStretchLastSection(True)
    # Горизонтальное направление, размер таблицы увеличивается до соответствующего размера
        self.view_planets.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view_planets.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    # Для отображения данных на виджете свяжем его и нашу модель данных
        self.view_planets.setModel(self.model_planets)
    # разрешим сортировку по столбцам
        self.view_planets.setSortingEnabled(True)
        self.view_planets.hideColumn(0)

        self.model_missions.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        self.model_missions.setHeaderData(1, QtCore.Qt.Horizontal, 'Название миссии')
        self.model_missions.setHeaderData(2, QtCore.Qt.Horizontal, 'Дата старта\nмиссии')
        self.model_missions.setHeaderData(3, QtCore.Qt.Horizontal, 'Дата окончания\nмиссии')
        self.model_missions.setHeaderData(4, QtCore.Qt.Horizontal, 'Примечания')
        self.view_missions.setModel(self.model_missions)
        self.view_missions.horizontalHeader().setStretchLastSection(True)
        self.view_missions.setColumnWidth(1, 220)
        self.view_missions.setSortingEnabled(True)
        self.view_missions.hideColumn(0)

        self.model_landings.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        self.model_landings.setHeaderData(1, QtCore.Qt.Horizontal, 'ID планеты')
        self.model_landings.setHeaderData(2, QtCore.Qt.Horizontal, 'ID миссии')
        self.model_landings.setHeaderData(3, QtCore.Qt.Horizontal, 'Долгота\nместа посадки')
        self.model_landings.setHeaderData(4, QtCore.Qt.Horizontal, 'Широта\nместа посадки')
        self.model_landings.setHeaderData(5, QtCore.Qt.Horizontal, 'Примечания')
        self.view_landings.horizontalHeader().setStretchLastSection(True)
        self.view_landings.setModel(self.model_landings)
        self.view_landings.setSortingEnabled(True)
        self.view_landings.hideColumn(0)

        self.vbox = QVBoxLayout()

        self.btnAdd = QPushButton('Добавить запись')
        self.btnAdd.clicked.connect(self.addRecord)
        self.vbox.addWidget(self.btnAdd)
        self.btnDel = QPushButton('Удалить запись')
        self.btnDel.clicked.connect(self.delRecord)
        self.vbox.addWidget(self.btnDel)
        self.btnSave = QPushButton('Сохранить')
        self.btnSave.clicked.connect(self.save)
        self.vbox.addWidget(self.btnSave)

        self.tab = QTabWidget()
        self.tab.addTab(self.view_planets, "Данные о планетах")
        self.tab.addTab(self.view_missions, "Данные о миссиях")
        self.tab.addTab(self.view_landings, "Данные о посадках на планеты")
        self.tab.setCurrentIndex(0)
        self.vbox.addWidget(self.tab)

        self.setLayout(self.vbox)

    def addRecord(self):
        # Вставляем пустую запись, в которую можно ввести нужные данные
        if self.tab.currentIndex() == 0:
            self.model_planets.insertRow(self.model_planets.rowCount())
        elif self.tab.currentIndex() == 1:
            self.model_missions.insertRow(self.model_missions.rowCount())
        elif self.tab.currentIndex() == 2:
            self.model_landings.insertRow(self.model_landings.rowCount())

    def delRecord(self):
    # Спрашиваем у пользователя подтверждение на удаление элементов
        valid = QMessageBox.question(
            self, 'Подтвердите', 'Действительно удалить запись',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
    # Удаляем запись из модели
    # Выполняем повторное считывание данных в модель, чтобы убрать пустую "мусорную" запись
            if self.tab.currentIndex() == 0:
                self.model_planets.removeRow(self.view_planets.currentIndex().row())
                self.model_planets.select()
            elif self.tab.currentIndex() == 1:
                self.model_missions.removeRow(self.view_missions.currentIndex().row())
                self.model_missions.select()
            elif self.tab.currentIndex() == 2:
                self.model_landings.removeRow(self.view_landings.currentIndex().row())
                self.model_landings.select()

    def save(self):
        if self.tab.currentIndex() == 0:
            self.model_planets.submitAll()
        elif self.tab.currentIndex() == 1:
            self.model_missions.submitAll()
        elif self.tab.currentIndex() == 1:
            self.model_landings.submitAll()


# Форма визуализации успешных посадок на планету
class VisualForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        # Выбор файла с данными об успешных посадках на планету
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выберите файл с данными об успешных посадках на планету', 'resources/data',
            'данные (*.txt);;Все файлы (*)')[0]
        self.setWindowIcon(QIcon('resources/pic/04.png'))
        try:
            self.data = np.genfromtxt(self.fname)

        except ValueError:
            res = QMessageBox.information(self, 'Предупреждение', 'Неверный формат данных',
                                          buttons=QMessageBox.Close)
        except FileNotFoundError:
            self.close()

        else:
            self.setGeometry(500, 100, 700, 730)
            self.setWindowTitle('Визуальный анализ успешных посадок')
            self.setWindowIcon(QIcon('resources/pic/03.png'))

        # Сфера
            t, ph = np.mgrid[0:np.pi:100j, 0:2 * np.pi:100j]
            x1 = np.sin(t) * np.cos(ph)
            y1 = np.sin(t) * np.sin(ph)
            z1 = np.cos(t)

        # Точки посадки на планету
            theta, phi = np.hsplit(self.data, 2)
            theta = theta * np.pi / 180.0
            phi = phi * np.pi / 90.0
            xx = (np.sin(phi) * np.cos(theta)).reshape(1, 1000)[0]
            yy = (np.sin(phi) * np.sin(theta)).reshape(1, 1000)[0]
            zz = (np.cos(phi)).reshape(1, 1000)[0]

            fig = go.Figure(data=[go.Surface(x=x1, y=y1, z=z1, opacity=0.3, showscale=False),
                                    go.Scatter3d(x=xx, y=yy, z=zz, mode='markers',
                                                marker=dict(size=3, opacity=0.7))
                                    ])

        # html-код для  plotly 3D объекта
            html = '<html><body>'
            html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
            html += '</body></html>'

        # Подключение к БД
            con = sqlite3.connect('resources/bd/uncharted_planets.db')
        # Создание курсора
            cur = con.cursor()
        # Выполнение запроса данных о выбранной планете
            f = self.fname[self.fname.rfind('/')  + 1:]
            result1 = cur.execute("""SELECT * FROM planets
                                    WHERE id = (SELECT id_planet
                                    FROM files
                                    WHERE file_name = ?)""", (f, )).fetchall()[0]
#            print(f, result1)
            id = result1[0]
        # Определение количества успешных посадок на выбранную планету в последней миссии
            cur = con.cursor()
            result2 = cur.execute("""SELECT count(*) FROM planets
                                    INNER JOIN landings ON
                                    planets.id = landings.id_planet
                                    GROUP BY landings.id_planet
                                    HAVING landings.id_planet = ?""", (id, )).fetchall()[0]
            con.close()
 #           print(result2)

            self.form = QFormLayout(self)
            self.hbox_1 = QHBoxLayout(self)
            self.label_1 = QLabel(self)
            font2 = QtGui.QFont()
            font2.setPointSize(16)
            self.label_1.setFont(font2)
            self.label_1.setText('Данные о планете и миссиях')
            self.hbox_1.addWidget(self.label_1, alignment=QtCore.Qt.AlignCenter)
            self.form.addRow(self.hbox_1)

            self.label_2 = QLabel(self)
            self.label_3 = QLabel(self)
            self.label_4 = QLabel(self)
            self.label_5 = QLabel(self)
            self.label_6 = QLabel(self)
            self.label_7 = QLabel(self)
            self.label_8 = QLabel(self)
            font2.setPointSize(11)
            self.label_2.setFont(font2)
            self.label_3.setFont(font2)
            self.label_4.setFont(font2)
            self.label_5.setFont(font2)
            self.label_6.setFont(font2)
            self.label_7.setFont(font2)
            self.label_8.setFont(font2)
            self.hbox_2 = QHBoxLayout(self)
            self.hbox_3 = QHBoxLayout(self)
            self.hbox_4 = QHBoxLayout(self)
            self.hbox_5 = QHBoxLayout(self)

            self.label_2.setText('Название: ' + result1[1])
            self.label_3.setText('Среднее расстояние от звезды планетарной системы: ' + str(result1[2]) + ' а.е.')
            self.label_4.setText('Средняя орбитальная скорость: ' + str(result1[3]) + ' км/с')
            self.label_5.setText('Период обращени вокруг звезды: ' + str(result1[4]) + ' сут.')
            self.label_6.setText('Период вращения вокруг оси: ' + str(result1[5]) + ' дней')
            self.label_7.setText('Наклон экватора к орбите: ' + str(result1[6]) + ' град.')
            self.label_8.setText('Количество успешных посадок в последней миссии: ' + str(result2[0]))
            self.hbox_2.addWidget(self.label_2)
            self.hbox_2.addWidget(self.label_3)
            self.hbox_3.addWidget(self.label_4)
            self.hbox_3.addWidget(self.label_7)
            self.hbox_4.addWidget(self.label_5)
            self.hbox_4.addWidget(self.label_6)
            self.hbox_5.addWidget(self.label_8)
            self.form.addRow(self.hbox_2)
            self.form.addRow(self.hbox_3)
            self.form.addRow(self.hbox_4)
            self.form.addRow(self.hbox_5)

        # Экземпляр QWebEngineView с установкой html-кода
            self.plot_widget = QWebEngineView(self)
            self.plot_widget.setHtml(html)
            self.plot_widget.move(50, 150)
            self.plot_widget.resize(600, 600)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainForm()
    Main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
