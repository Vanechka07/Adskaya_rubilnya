import sys

import pygame
from pygame import mixer
import time
import sqlite3
import random
from PyQt5.QtWidgets import QApplication, QLabel, QTabWidget, QTableView, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QComboBox, QHeaderView
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QTableWidget, QPushButton, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QListWidget, QScrollArea, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QSize
import datetime

pygame.init()

username = ''
count = 0
flag = True
trues = 0


# Стартовое окно прриложения
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Английский алфавит')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.registr_button = QPushButton(self)
        self.registr_button.setText('РЕГИСТРАЦИЯ')
        self.registr_button.setFont(font)
        self.registr_button.move(340, 186)
        self.registr_button.resize(600, 200)
        self.registr_button.clicked.connect(self.registration)

        self.vhod_button = QPushButton(self)
        self.vhod_button.setText('ВХОД')
        self.vhod_button.setFont(font)
        self.vhod_button.move(340, 572)
        self.vhod_button.resize(600, 200)
        self.vhod_button.clicked.connect(self.vhod)

    def registration(self):
        self.reg = RegistrationWindow()
        self.reg.show()
        self.close()

    def vhod(self):
        self.vh = VhodWindow()
        self.vh.show()
        self.close()


# Окно регистрации
class RegistrationWindow(QWidget):
    def __init__(self):
        super(RegistrationWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.name = QLineEdit(self)
        self.name.setFont(font)
        self.name.move(340, 165)
        self.name.resize(600, 100)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setPlaceholderText(QCoreApplication.translate("Form", "Имя Пользователя"))

        self.password = QLineEdit(self)
        self.password.setFont(font)
        self.password.move(340, 330)
        self.password.resize(600, 100)
        self.password.setFont(font)
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setPlaceholderText(QCoreApplication.translate("Form", "Пароль"))

        self.reistration_button = QPushButton(self)
        self.reistration_button.setFont(font)
        self.reistration_button.setText('ЗАРЕГИСТРИРОВАТЬСЯ')
        self.reistration_button.move(340, 570)
        self.reistration_button.resize(600, 250)
        self.reistration_button.clicked.connect(self.registrate)

    def registrate(self):
        nam = self.name.text()
        pas = self.password.text()
        if pas and nam:
            global username
            username = self.name.text()
            self.con = sqlite3.connect('name_base.db')
            cur = self.con.cursor()
            cur.execute('''INSERT INTO user_data (username, password) VALUES(?, ?)''', (self.name.text(), self.password.text()))
            self.con.commit()
            self.next = ModeSelectionWindow()
            self.next.show()
            self.close()
        if not pas and nam:
            QtWidgets.QMessageBox.information(self, 'Пустой пароль',
                                              'Введите пароль', buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)
        if not nam and pas:
            QtWidgets.QMessageBox.information(self, 'Пустое имя пользователя',
                                              'Введите имя пользователя', buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)
        if not pas and not nam:
            QtWidgets.QMessageBox.information(self, 'Пустые пароль и имя пользователя',
                                              'Введите имя пароль и имя пользователя', buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)


# Окно входа
class VhodWindow(QWidget):
    def __init__(self):
        super(VhodWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вход')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.name = QComboBox(self)
        self.name.setFont(font)
        self.name.move(340, 165)
        self.name.resize(600, 100)
        self.con = sqlite3.connect('name_base.db')
        cur = self.con.cursor()
        self.name.addItems([x[0] for x in cur.execute("""SELECT username FROM user_data""").fetchall()])
        self.con.commit()

        self.password = QLineEdit(self)
        self.password.setFont(font)
        self.password.move(340, 330)
        self.password.resize(600, 100)
        self.password.setFont(font)
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setPlaceholderText(QCoreApplication.translate("Form", "Пароль"))

        self.reistration_button = QPushButton(self)
        self.reistration_button.setFont(font)
        self.reistration_button.setText('ВОЙТИ')
        self.reistration_button.move(340, 570)
        self.reistration_button.resize(600, 250)
        self.reistration_button.clicked.connect(self.vhod)

        #сделать функцию проверки пароля

    def vhod(self):
        nam = self.name.currentText()
        pas = self.password.text()
        print(nam, pas)
        global username
        if pas and nam:
            con = sqlite3.connect('name_base.db')
            cur = con.cursor()
            if cur.execute("""SELECT password FROM user_data WHERE username = ?""", (nam,)).fetchone()[0] == pas:
                username = nam
                self.next = ModeSelectionWindow()
                self.next.show()
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, 'Неверный пароль',
                                                  'Введите правильный пароль', buttons=QtWidgets.QMessageBox.Ok,
                                                  defaultButton=QtWidgets.QMessageBox.Ok)
                self.password.setText('')
        else:
            QtWidgets.QMessageBox.information(self, 'Пустой пароль',
                                              'Введите пароль', buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)


# Окно выбора режима работы
class ModeSelectionWindow(QWidget):
    def __init__(self):
        super(ModeSelectionWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор режима')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.education_button = QPushButton(self)
        self.education_button.setFont(font)
        self.education_button.setText('ОБУЧЕНИЕ')
        self.education_button.move(340, 70)
        self.education_button.resize(600, 250)
        self.education_button.clicked.connect(self.education)


        self.test_button = QPushButton(self)
        self.test_button.setFont(font)
        self.test_button.setText('ТЕСТ')
        self.test_button.move(340, 370)
        self.test_button.resize(600, 250)
        self.test_button.clicked.connect(self.test)

        self.statist_button = QPushButton(self)
        self.statist_button.setFont(font)
        self.statist_button.setText('СТАТИСТИКА')
        self.statist_button.move(340, 670)
        self.statist_button.resize(600, 250)
        self.statist_button.clicked.connect(self.statistic)

    def education(self):
        self.educ = EducationWindow()
        self.educ.show()
        self.close()

    def test(self):
        self.test = TestWindow()
        self.test.show()
        self.close()

    def statistic(self):
        self.stat = StatisticWindow()
        self.stat.show()
        self.close()


# Окно обучения
class EducationWindow(QWidget):
    def __init__(self):
        super(EducationWindow, self).__init__()
        self.initUI()

    def plsnd(self):
        mixer.init()
        fname = self.sender().text().lower()
        mixer.music.load('alpha/' + fname + '.mp3')
        mixer.music.play()
        pygame.time.delay(200)

    def end_education(self):
        mixer.music.stop()
        self.end = ModeSelectionWindow()
        self.end.show()
        self.close()

    def initUI(self):
        texts = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.setWindowTitle('Обучение')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1)")
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(20)
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self.buttons = [QPushButton(self) for i in range(26)]
        for i in range(26):
            self.buttons[i].resize(200, 150)
            self.buttons[i].setFont(font)
            self.buttons[i].setText(alphabet[i])
            self.buttons[i].setStyleSheet("color : rgba(0, 0, 0, 0)")
            self.buttons[i].setIcon(QIcon('alpha/' + texts[i].lower() + '_picture.png'))
            self.buttons[i].setIconSize(QSize(200, 150))
            self.buttons[i].clicked.connect(self.plsnd)
            if i < 25:
                self.buttons[i].move(i % 6 * 216, i // 6 * 166)
            else:
                self.buttons[i].move(1080, 664)

        self.pushButton_close = QPushButton(self)
        self.pushButton_close.move(432, 740)
        self.pushButton_close.resize(416, 220)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setText("ЗАВЕРШИТЬ ОБУЧЕНИЕ")
        self.pushButton_close.clicked.connect(self.end_education)


class TestWindow(QWidget):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.initUI()

    def statistic(self):
        mixer.music.stop()
        self.statist = StatisticWindow()
        self.statist.show()
        self.close()

    def initUI(self):
        global count
        self.setWindowTitle('Тест')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.start = QPushButton(self)
        self.start.setFont(font)
        self.start.setText('НАЧАТЬ')
        self.start.move(340, 155)
        self.start.resize(600, 250)
        self.start.clicked.connect(self.test_1)

        self.stat = QPushButton(self)
        self.stat.setFont(font)
        self.stat.setText('СТАТИСТИКА')
        self.stat.resize(600, 250)
        self.stat.move(340, 560)
        self.stat.clicked.connect(self.statistic)



    def test_1(self):
        global count
        count = 0
        self.a = SoloTest()
        self.a.show()


class SoloTest(QWidget):
    def __init__(self):
        super().__init__()
        self.texts = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.alpha = {1: 'a.mp3', 2: 'b.mp3', 3: 'c.mp3', 4: 'd.mp3', 5: 'e.mp3', 6: 'f.mp3', 7: 'g.mp3',
                      8: 'h.mp3', 9: 'i.mp3', 10: 'j.mp3', 11: 'k.mp3', 12: 'l.mp3', 13: 'm.mp3', 14: 'n.mp3',
                      15: 'o.mp3', 16: 'p.mp3', 17: 'q.mp3', 18: 'r.mp3', 19: 's.mp3', 20: 't.mp3',
                      21: 'u.mp3', 22: 'v.mp3', 23: 'w.mp3', 24: 'x.mp3', 25: 'y.mp3', 26: 'z.mp3'}
        self.initUI()
        self.generation()

    def initUI(self):
        global trues
        trues = 0
        self.setWindowTitle('Тест')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)
        self.btn1 = QPushButton(self)
        self.btn1.setFont(font)
        self.btn1.move(20, 355)
        self.btn1.resize(400, 250)

        self.btn2 = QPushButton(self)
        self.btn2.setFont(font)
        self.btn2.move(440, 355)
        self.btn2.resize(400, 250)

        self.btn3 = QPushButton(self)
        self.btn3.setFont(font)
        self.btn3.move(860, 355)
        self.btn3.resize(400, 250)

        self.numbers_of_letters = list(range(26))
        pos_true, n_1, n_2, n_3 = 0, 0, 0, 0
        numbs = []
        self.args = []
        for i in range(26):
            n_1 = random.choice(self.numbers_of_letters)
            if n_1 >= 15:
                n_2 = n_1 - random.randint(1, 7)
                n_3 = n_2 - random.randint(1, 8)
            elif n_1 <= 15:
                n_2 = n_1 + random.randint(1, 5)
                n_3 = n_2 + random.randint(1, 5)
            pos_true = random.randint(1, 3)
            if pos_true == 1:
                numbs = [n_1, n_2, n_3, n_1]
            elif pos_true == 2:
                numbs = [n_2, n_1, n_3, n_1]
            elif pos_true == 3:
                numbs = [n_2, n_3, n_1, n_1]
            self.args.append(numbs)
            self.numbers_of_letters.remove(n_1)
        print('1---', self.args)
        self.btn1.clicked.connect(self.proverka)
        self.btn2.clicked.connect(self.proverka)
        self.btn3.clicked.connect(self.proverka)



    def generation(self):
        global count
        global trues
        if count == 26:
            self.con = sqlite3.connect('name_base.db')
            cur = self.con.cursor()
            if len(cur.execute("""SELECT passed FROM tryes WHERE user_id = ?""",
                               (cur.execute("""SELECT id FROM user_data WHERE username = ?""",
                                            (username,)).fetchone()[0],)).fetchall()) <= 1:
                cur.execute('''INSERT INTO tryes (date, passed, user_id, best) VALUES(?, ?, ?, ?)''',
                        ((datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                          round(trues / 26 * 100, 2),
                          cur.execute("""SELECT id FROM user_data WHERE username = ?""", (username,)).fetchone()[0],
                          (round(trues / 26 * 100, 2)))))
            else:
                cur.execute('''INSERT INTO tryes (date, passed, user_id) VALUES(?, ?, ?)''',
                            ((datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                              round(trues / 26 * 100, 2),
                              cur.execute("""SELECT id FROM user_data WHERE username = ?""", (username,)).fetchone()[0],)))
                if cur.execute('''SELECT best FROM tryes WHERE user_id = ?''',
                               (cur.execute("""SELECT id FROM user_data WHERE username = ?""",
                                            (username,)).fetchone()[0],)).fetchone()[0] <= 1:
                    cur.execute('''UPDATE tryes SET best = round(trues / 26 * 100, 2) WHERE username = ?''', (cur.execute("""SELECT id FROM user_data WHERE username = ?""",
                                  (username,)).fetchone()[0]))
            count = 0
            self.con.commit()
            self.close()
        else:
            self.btn1.setText(self.texts[self.args[count][0]])
            self.btn2.setText(self.texts[self.args[count][1]])
            self.btn3.setText(self.texts[self.args[count][2]])
            mixer.music.pause()
            time.sleep(1)
            mixer.music.unpause()
            mixer.music.load('alpha/' + self.texts[self.args[count][3]].lower() + '.mp3')
            mixer.music.play()
            pygame.time.delay(200)

    def proverka(self):
        global trues
        global count
        if count < 26:
            if self.sender().text() == self.texts[self.args[count][3]]:
                trues += 1
        print(trues)
        print(count, '2---', self.args[count])
        print('текст с кнопки:', self.sender().text())
        print('правильный ответ:', self.texts[self.args[count][3]])
        count += 1
        self.generation()


class StatisticWindow(QWidget):
    def __init__(self):
        super(StatisticWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Статистика')
        self.setFixedSize(1280, 960)
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        self.since = QLineEdit(self)
        self.since.setFont(font)
        self.since.move(140, 65)
        self.since.resize(200, 80)
        self.since.setAlignment(QtCore.Qt.AlignCenter)
        self.since.setPlaceholderText(QCoreApplication.translate("Form", "С"))

        self.to = QLineEdit(self)
        self.to.setFont(font)
        self.to.move(440, 65)
        self.to.resize(200, 80)
        self.to.setAlignment(QtCore.Qt.AlignCenter)
        self.to.setPlaceholderText(QCoreApplication.translate("Form", "До"))

        self.leave = QPushButton(self)
        self.leave.move(936, 65)
        self.leave.resize(200, 80)
        self.leave.setText('Выход')
        self.leave.setFont(font)
        self.leave.clicked.connect(self.lv)

        self.btn = QPushButton(self)
        self.btn.move(686, 65)
        self.btn.resize(200, 80)
        self.btn.setText('Посмотреть')
        self.btn.setFont(font)
        self.btn.clicked.connect(self.res)

        self.con = sqlite3.connect('name_base.db')
        cur = self.con.cursor()
        self.con.commit()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)

        arr = []
        global username
        dates = cur.execute("""SELECT date FROM tryes WHERE user_id = ?""", (cur.execute("""SELECT id FROM user_data WHERE username = ?""", (username,)).fetchone()[0],)).fetchall()
        passeds = cur.execute("""SELECT passed FROM tryes WHERE user_id = ?""",
                               (cur.execute("""SELECT id FROM user_data WHERE username = ?""",
                                            (username,)).fetchone()[0],)).fetchall()

        self.table = QTableWidget(self)
        self.table.move(139, 200)
        self.table.resize(1000, 680)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Дата", "% Правильности"])
        self.table.setColumnWidth(0, 480)
        self.table.setColumnWidth(1, 480)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowCount(len(dates))
        for i, row in enumerate(dates):
            self.table.setItem(i, 0, QTableWidgetItem(str(dates[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(round(passeds[i][0], 2))))

        print(dates)
        print(passeds)


    def lv(self):
        self.next = ModeSelectionWindow()
        self.next.show()
        self.close()

    def res(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())