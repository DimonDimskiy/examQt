"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtCore, QtGui

from ui.c_signals_events import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()
        self.screen = QtWidgets.QApplication.screenAt(self.pos())

    def initSignals(self):
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetData)
        self.ui.pushButtonLT.clicked.connect(self.moveLeftTop)
        self.ui.pushButtonLB.clicked.connect(self.moveLeftBottom)
        self.ui.pushButtonRT.clicked.connect(self.moveRightTop)
        self.ui.pushButtonRB.clicked.connect(self.moveRightBottom)
        self.ui.pushButtonCenter.clicked.connect(self.moveCenter)
        self.ui.pushButtonMoveCoords.clicked.connect(self.moveCoords)

    def resizeEvent(self, event: QtCore.QEvent) -> None:
        self.ui.plainTextEdit.appendPlainText(f"Старый размер {QtGui.QResizeEvent.oldSize(event).toTuple()}")
        self.ui.plainTextEdit.appendPlainText(f"Новый размер {QtGui.QResizeEvent.size(event).toTuple()}")

    def moveEvent(self, event: QtCore.QEvent) -> None:
        self.ui.plainTextEdit.appendPlainText(f"Старая позиция {QtGui.QMoveEvent.oldPos(event).toTuple()}")
        self.ui.plainTextEdit.appendPlainText(f"Новая позиция {QtGui.QMoveEvent.pos(event).toTuple()}")
        self.screen = QtWidgets.QApplication.screenAt(self.pos())

    def hideEvent(self, event: QtCore.QEvent) -> None:
        self.ui.plainTextEdit.appendPlainText("Окно свернуто")

    def showEvent(self, event: QtCore.QEvent) -> None:
        self.ui.plainTextEdit.appendPlainText("Окно развернуто")



    def onPushButtonGetData(self):
        self.ui.plainTextEdit.appendPlainText(str(len(QtWidgets.QApplication.screens())))
        self.ui.plainTextEdit.appendPlainText(str(QtWidgets.QApplication.activeWindow()))
        self.ui.plainTextEdit.appendPlainText(str(QtWidgets.QApplication.screenAt(self.pos()).geometry()))
        self.ui.plainTextEdit.appendPlainText(str(QtWidgets.QApplication.screenAt(self.pos())))
        self.ui.plainTextEdit.appendPlainText(str(QtWidgets.QApplication.activeWindow().size()))
        self.ui.plainTextEdit.appendPlainText(str(QtWidgets.QApplication.activeWindow().minimumSize()))
        self.ui.plainTextEdit.appendPlainText(str(self.pos()))
        self.ui.plainTextEdit.appendPlainText(f"{self.pos().x() + self.height() / 2}, {self.pos().y() + self.width() / 2}")

    def moveLeftTop(self):
        self.move(0, 0)

    def moveLeftBottom(self):
        y = self.screen.size().height() - self.size().height()
        self.move(0, y)

    def moveRightTop(self):
        x = self.screen.size().width() - self.size().width()
        self.move(x, 0)

    def moveRightBottom(self):
        x, y = self.screen.size().width() - self.size().width(), self.screen.size().height() - self.size().height()
        self.move(x, y)

    def moveCenter(self):
        x, y = (self.screen.size().width() - self.size().width()) / 2, (self.screen.size().height() - self.size().height()) / 2
        self.move(x, y)

    def moveCoords(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
