"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets
from ui.d_eventfilter_settings import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUi()
        self.initSignals()

    def initUi(self):

        self.ui.comboBox.addItems(["oct", "hex", "bin", "dec"])
        self.ui.horizontalSlider.setRange(0, 100)
        self.ui.dial.setRange(0, 100)
        self.ui.dial.setWrapping(True)
        self.ui.dial.setSingleStep(5)
        self.ui.dial.setNotchesVisible(True)


    def initSignals(self):

        self.ui.dial.valueChanged.connect(self.onDialValueChanged)
        self.ui.horizontalSlider.valueChanged.connect(self.onHSValueChanged)
        self.ui.comboBox.currentTextChanged.connect(self.onCBCurrentTextChanged)
        self.ui.lcdNumber.overflow.connect(lambda: self.ui.lcdNumber.display("Error"))

    def onDialValueChanged(self):

        self.ui.horizontalSlider.setValue(self.ui.dial.value())
        self.ui.lcdNumber.display(self.ui.dial.value())

    def onHSValueChanged(self):

        self.ui.dial.setValue(self.ui.horizontalSlider.value())
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())

    def onCBCurrentTextChanged(self):
        match self.ui.comboBox.currentText():
            case "dec":
                self.ui.lcdNumber.setDecMode()
            case "hex":
                self.ui.lcdNumber.setHexMode()
            case "oct":
                self.ui.lcdNumber.setOctMode()
            case "bin":
                self.ui.lcdNumber.setBinMode()
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
