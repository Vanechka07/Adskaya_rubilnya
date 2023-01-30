import sys


import sqlite3

from PyQt5.QtWidgets import QApplication, QLabel, QTabWidget, QTableView  #, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QComboBox, QHeaderView
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 80, 1000, 700)
        self.setWindowTitle('Квадрокоптер')

        # Графическая заставка на главной форме
        self.pixmap = QPixmap('resources/pic/fon.jpg')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.move(0, 0)
        self.image.resize(1200, 700)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        # Заголовок легенды на главной форме
        self.title = QLabel(self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont()
        font1.setPointSize(20)
        self.title.setFont(font1)
        self.title.setTextFormat(QtCore.Qt.AutoText)
        self.title.setText('По мотивам задачи проходного этапа профиля "БПЛА" конкурса ИнтЭРА.')

        # Легенда
        self.legend = QLabel(self)
        self.legend.setAlignment(QtCore.Qt.AlignHCenter)
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.legend.setFont(font2)
        self.legend.setText('В мире зародился опасный вирус. Жители города постепенно заболевают этой болезнью. Но к '
                            'счастью ученые быстро\nизобрели вакцину, и она оказалась очень успешная!\nДля того чтобы '
                            'врачи не контактировали с больными, на помощь приходят беспилотники!\nОни могут доставить '
                            'вакцину в городе прямо из больницы пациенту домой по воздуху.\nВ каждом из домов болеет по'
                            ' одному человеку.\nВ центре района – больница со взлётной площадкой, откуда вылетает '
                            'беспилотник.\nГрузоподъемность БВС – 3 вакцины за один полет.')

    # Кнопка Начать исследование
        self.button = QPushButton('Начнём!', self)
        self.button.clicked.connect(self.open_form1)

    # Компановка всех элементов главной формы в вертикальный бокс
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.legend)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)

    def open_form1(self):
        self.first_form = FirstForm(self, None)
        self.first_form.show()
        self.close()


class FirstForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(200, 100, 400, 480)
        self.setWindowTitle('Исследование')
        self.setFixedSize(400, 480)

        self.pixmap = QPixmap('resources/pic/fon0.png')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.resize(900, 1900)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        self.button1 = QPushButton('пример работы', self)
        self.button1.setGeometry(QtCore.QRect(30, 30, 340, 90))
        self.button1.clicked.connect(self.open_form_example)

        self.button2 = QPushButton('история', self)
        self.button2.setGeometry(QtCore.QRect(30, 140, 340, 90))
        self.button2.clicked.connect(self.open_form_history)

        self.button3 = QPushButton('расчет полета', self)
        self.button3.setGeometry(QtCore.QRect(30, 250, 340, 90))
        self.button3.clicked.connect(self.open_form_calculation)

        self.button4 = QPushButton('завершение работы', self)
        self.button4.setGeometry(QtCore.QRect(30, 360, 340, 90))
        self.button4.clicked.connect(sys.exit)

    def open_form_example(self):
        self.second_form = ExampleForm(self)
        self.second_form.show()

    def open_form_history(self):
        self.third_form = HistoryForm(self)
        self.third_form.show()

    def open_form_calculation(self):
        self.fourth_form = CalculationForm(self)
        self.fourth_form.show()


class ExampleForm(FirstForm):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(500, 100, 1100, 900)
        self.setWindowTitle('Пример работы')
        self.setFixedSize(1100, 900)

        self.pixmap = QPixmap('resources/pic/fon.jpg')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.resize(1900, 1000)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        font1 = QtGui.QFont()
        font1.setPointSize(12)
        font2 = QtGui.QFont()
        font2.setPointSize(15)
        font3 = QtGui.QFont()
        font3.setUnderline(True)
        font3.setPointSize(12)

        self.heading = QLabel('Для примера рассмотрим ситуацию.\nВ городе находится 9 домов с координатами: 1-(1;3) 2-'
                            '(-4;1) 3-(-1;3) 4-(-3;5) 5-(2;5) 6(0;2) 7-(1;5) 8-(4;-2) 9-(3;-4)\nВ каждый дом нужно до'
                            'ставить вакцину и вычислить минимальный путь, а также узнать траекторию его полета.\n'
                              'максимальный путь который может пролететь квадракоптер 12 км', self)
        self.heading.setAlignment(QtCore.Qt.AlignHCenter)
        self.heading.setFont(font1)
        self.heading.move(10, 10)
        self.label = QLabel('Координаты вводятся через пробел и между числами должно стоять двоеточие!', self)
        self.label.setFont(font3)
        self.label.move(20, 110)

        self.pixmap = QPixmap('resources/pic/houses.png')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.move(50, 150)
        self.image.resize(1000, 550)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        self.label1 = QLabel('Таким образом мы получили вот такую траекторию как на фото.', self)
        self.label1.setFont(font2)
        self.label1.move(200, 710)

        self.label2 = QLabel('Минимальное расстояние для доставки всех вакцин: 53.80848475074288.', self)
        self.label2.setFont(font2)
        self.label2.move(150, 740)


class HistoryForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(400, 200, 600, 750)
        self.setWindowTitle('История')
        self.setFixedSize(600, 750)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 550, 650)
        self.table.setColumnCount(3)
        self.table.setRowCount(20)
        self.table.setHorizontalHeaderLabels(['Траектория', "Путь", "Координаты"])
        self.table.setColumnWidth(0, 300)
        self.btn = QPushButton('Очистить', self)
        self.btn.setFont(font)
        self.btn.move(280, 700)
        self.btn.clicked.connect(self.udalenie)

        con = sqlite3.connect('resources/bd/book.db')
        cur = con.cursor()
        res1 = cur.execute("""SELECT length FROM coordinates""").fetchall()
        res2 = cur.execute("""SELECT trajectory FROM coordinates""").fetchall()
        res3 = cur.execute("""SELECT coordinate FROM coordinates""").fetchall()
        for i, row in enumerate(res1):
            self.table.setItem(i, 1, QTableWidgetItem(res1[i][0]))
        for i, row in enumerate(res2):
            self.table.setItem(i, 0, QTableWidgetItem(res2[i][0]))
        for i, row in enumerate(res3):
            self.table.setItem(i, 2, QTableWidgetItem(res3[i][0]))

    def udalenie(self):
        con = sqlite3.connect('resources/bd/book.db')
        cur = con.cursor()
        cur.execute("""DELETE FROM coordinates""")
        con.commit()


class CalculationForm(FirstForm):
    def __init__(self, *args):
        self.passed_points = []
        self.All_points = {}
        self.distance_2_point = dict()
        self.distance_3_point = dict()
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(500, 100, 1100, 600)
        self.setWindowTitle('Основной расчет')
        self.setFixedSize(1100, 600)

        self.pixmap = QPixmap('resources/pic/fon1.jpg')
        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignHCenter)
        self.image.resize(1900, 1000)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        font = QtGui.QFont()
        font.setWeight(True)
        font.setPointSize(30)
        font1 = QtGui.QFont()
        font1.setUnderline(True)
        font1.setPointSize(12)
        font2 = QtGui.QFont()
        font2.setPointSize(12)

        self.label0 = QLabel('Расчет полета', self)
        self.label0.setFont(font)
        self.label0.move(350, 10)
        self.label1 = QLabel('Введите количество точек:', self)
        self.label1.setFont(font2)
        self.label1.move(10, 90)
        # вводится одно число
        self.input1 = QLineEdit(self)
        self.input1.setFont(font2)
        self.input1.move(215, 87)
        self.input1.resize(30, 30)
        self.label2 = QLabel('Введите их координаты (c учетом координаты 0:0 к примеру(0:0 1:1 2:2 3:3 и тд.):', self)
        self.label2.setFont(font2)
        self.label2.move(10, 150)
        self.btn1 = QPushButton('Ввести готовые координаты', self)
        self.btn1.move(650, 150)
        self.btn1.clicked.connect(self.dialog)
        # вводятся координаты точек
        self.input2 = QLineEdit(self)
        self.input2.setFont(font2)
        self.input2.move(10, 177)
        self.input2.resize(800, 30)
        self.label3 = QLabel('Введите ограничитель пути:', self)
        self.label3.setFont(font2)
        self.label3.move(10, 230)
        # вводится ограничитель пути
        self.input3 = QLineEdit(self)
        self.input3.setFont(font2)
        self.input3.move(225, 230)
        self.input3.resize(30, 30)
        self.label4 = QLabel('Важно! вводите координаты с учетом того чтоб ограничитель пути был больше,\nчем '
                             'двойное расстояние от введенной координаты до точки 0:0', self)
        self.label4.setFont(font1)
        self.label4.move(10, 260)
        self.btn = QPushButton('Загрузить', self)
        self.btn.setFont(font2)
        self.btn.move(460, 370)
        self.btn.clicked.connect(self.main_work)
        # после нажатия на кнопку запускается функция main_work
        self.label5 = QLabel('Минимальный путь:', self)
        self.label5.setFont(font2)
        self.label5.move(10, 450)
        self.out = QLineEdit(self)
        self.out.setFont(font2)
        self.out.move(165, 450)
        self.out.resize(100, 30)
        self.label6 = QLabel('Минимальная траектория:', self)
        self.label6.setFont(font2)
        self.label6.move(10, 490)
        self.out1 = QLineEdit(self)
        self.out1.setFont(font2)
        self.out1.move(210, 490)
        self.out1.resize(200, 30)

    def dialog(self):
        fname = QFileDialog.getOpenFileName(self)
        s = open(fname[0]).read().strip()
        self.input2.setText(s)

    def coordinate_calculation(self):  # добавление координат введеных в окно в словарь
        num = self.input1.text()
        coordinates = self.input2.text().split()
        a = list(map(lambda i: i.replace(':', ' '), coordinates))  # добавление в список значения координат
        for i in range(int(num)):
            self.All_points[i] = list(map(int, a[i].split()))  # добавление в словарь точек с их координатами
        return self.All_points

    def get_distance_between_any_points(self, point1=0, point2=0, point3=0):  # функция рассчета расстояния между двумя или тремя точками
        if point3 == 0:
            if point2 == 0:
                distance = ((([point1][0] - 0) ** 2 + (self.All_points[point1][1] - 0) ** 2) ** 0.5) * 2
            else:
                distance = ((self.All_points[point1][0] - 0) ** 2 + (self.All_points[point1][1] - 0) ** 2) ** 0.5 + \
                           ((self.All_points[point2][0] - self.All_points[point1][0]) ** 2 +
                            (self.All_points[point2][1] - self.All_points[point1][1]) ** 2) ** 0.5 + \
                      ((0 - self.All_points[point2][0]) ** 2 + (0 - self.All_points[point2][1]) ** 2) ** 0.5
        else:
            distance = ((self.All_points[point1][0] - 0) ** 2 + (self.All_points[point1][1] - 0) ** 2) ** 0.5 + \
                  ((self.All_points[point2][0] - self.All_points[point1][0]) ** 2 +
                   (self.All_points[point2][1] - self.All_points[point1][1]) ** 2) ** 0.5 + \
                  ((self.All_points[point3][0] - self.All_points[point2][0]) ** 2 +
                   (self.All_points[point3][1] - self.All_points[point2][1]) ** 2) ** 0.5 + \
                  ((0 - self.All_points[point3][0]) ** 2 + (0 - self.All_points[point3][1]) ** 2) ** 0.5
        return distance

    def get_distance(self, point_1, point_2):  # расчет расстояния между двумя точками
        distance = (((self.All_points[point_2][0] - self.All_points[point_1][0]) ** 2 +
                               (self.All_points[point_2][1] - self.All_points[point_1][1]) ** 2) ** 0.5)
        return distance

    def finding_ways(self):  # поиск возможных вариантов полета по двум и трем точкам
        mileage = int(self.input3.text())  # запас хода квадрокоптера
        for x in self.All_points.keys():
            if x != 0:  # пропуск 0 точки
                if self.get_distance(0, x) + self.get_distance(x, 0) < mileage:  # проверяем, возможно ли долететь от базы до точки x и вернуться обратно
                    quad_pos = x
                    mileage -= self.get_distance(0, x)
                    self.passed_points.append(x)
                    for i in self.All_points.keys():  # поиск 2й точки
                        if i != 0:  # пропуск 0 точки
                            if i not in self.passed_points:  # проверяем, посетили ли мы точку i
                                if self.get_distance(x, i) + self.get_distance(i, 0) < mileage:  # проверяем, возможно ли долететь от точки x до точки i и вернуться на базу
                                    self.passed_points.append(i)
                                    self.distance_2_point[str(
                                        x) + '-' + str(i)] = self.get_distance(x, 0) + self.get_distance(x, i) \
                                                             + self.get_distance(i, 0)
                                    for j in self.All_points.keys():  # поиск 3й точки
                                        if j != 0:
                                            if j not in self.passed_points:  # проверяем, посетили ли мы точку
                                                if self.get_distance(quad_pos, i) + self.get_distance(i, j) + \
                                                        self.get_distance(j, 0) < mileage:
                                                    self.distance_3_point[str(x) + '-' + str(i) + '-' + str(j)] = \
                                                        self.get_distance(x, 0) + self.get_distance(x, i) + \
                                                        self.get_distance(i, j) + self.get_distance(j, 0)
                                    self.passed_points.pop(-1)  # удаляем последний элемент
                # вернулись на базу
                mileage = 12
                self.passed_points.clear()

    def anti_palindrome3(self):  # исключение повторений из списка путей, состоящих из 3х точек
        lsk = []
        lsk1 = []
        for i in self.distance_3_point.keys():
            lsk.append(i)
        for i in lsk:
            for j in lsk:
                if i == j[::-1]:
                    lsk.remove(i)
        for i in lsk:
            for j in lsk:
                if i == j[::-1]:
                    lsk.remove(i)
        for i in lsk:
            lsk1.append(i.replace('-', ''))
        return lsk1

    def anti_palindrome2(self):  # исключение повторений из списка путей, состоящих из 2х точек
        lsk = []
        lsk1 = []
        for i in self.distance_2_point.keys():
            lsk.append(i)
        for i in lsk:
            for j in lsk:
                if i == j[::-1]:
                    lsk.remove(i)
        for i in lsk:
            for j in lsk:
                if i == j[::-1]:
                    lsk.remove(i)
        for i in lsk:
            lsk1.append(i.replace('-', ''))
        return lsk1

    def main_work(self):
        self.coordinate_calculation() #  вызов функции добавляющей координаты в словарь
        self.finding_ways() #  вызов функции ищущей варианты полета по двум и трем точкам
        way = ''
        ways_with_triplepoint = []
        ways_without_triplepoint = []
        single_points = []
        for i in range(1, int(self.input1.text())):
            single_points.append(str(i))

        for triple_point in self.anti_palindrome3():
            way += triple_point + ' '
            for double_point in self.anti_palindrome2():
                if double_point[0] not in way and double_point[1] not in way:
                    way += double_point + ' '
            for single_point in single_points:
                if single_point not in way:
                    way += single_point + ' '
            ways_with_triplepoint.append(way)
            way = ''

        for i in self.anti_palindrome2():
            way += i + ' '
            for j in self.anti_palindrome2():
                if j[0] not in way and j[1] not in way:
                    way += j + ' '
            for single_point in single_points:
                if single_point not in way:
                    way += single_point + ' '
            ways_without_triplepoint.append(way)
            way = ''

        way = 0
        D1 = {}  # словарь с расстояниями для путей с тремя точками
        for i in ways_with_triplepoint:
            for j in i.split():
                if len(j) == 1:
                    way += self.get_distance_between_any_points(int(j))
                if len(j) == 2:
                    way += self.get_distance_between_any_points(int(j[0]), int(j[1]))
                if len(j) == 3:
                    way += self.get_distance_between_any_points(int(j[0]), int(j[1]), int(j[2]))
            D1[i] = way
            way = 0

        way = 0
        D2 = {}  # словарь с расстояниями для путей без трех точек

        for i in ways_without_triplepoint:
            for j in i.split():
                if len(j) == 1:
                    way += self.get_distance_between_any_points(int(j))
                if len(j) == 2:
                    way += self.get_distance_between_any_points(int(j[0]), int(j[1]))
            D2[i] = way
            way = 0
        self.out.setText(str(min(D1.values()))[:5])
        self.out1.setText(str(min(D1, key=D1.get)))
        self.con = sqlite3.connect('resources/bd/book.db')
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO coordinates (trajectory, length, coordinate) VALUES('{str(min(D1, key=D1.get))}', '{str(round(min(D1.values()), 2))}', '{self.input2.text()}')""")
        cur.execute(f"""INSERT INTO cvadrocopters (limiter) VALUES('{self.input3.text()}')""")

        self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
