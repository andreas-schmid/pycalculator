#!/usr/bin/env python3

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from functools import partial


ERROR_MSG = 'ERROR'
__version__ = '0.1'
__author__ = 'Andreas Schmid'


class PyCalcUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyCalc')
        self.setFixedSize(235, 235)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget()
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        self._createMenuBar()
        self._createDisplay()
        self._createButtons()

    def _createMenuBar(self):
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction('&Exit', self.close)
        self.aboutMenu = self.menubar.addMenu('&Help')
        self.aboutMenu.addAction('&About', self._about)
        self.menubar.setNativeMenuBar(False)

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(35)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        btnLayout = QGridLayout()
        self.btns = {}
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                   }
        for btnText, position in buttons.items():
            self.btns[btnText] = QPushButton(btnText)
            self.btns[btnText].setFixedSize(40, 35)
            btnLayout.addWidget(self.btns[btnText], position[0], position[1])
        self.generalLayout.addLayout(btnLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getDisplayText(self):
        value = self.display.text()
        return value

    def clearDisplay(self):
        self.display.setText('')

    def _about(self):
        QMessageBox.about(self, 'About PyCalc', '''
            <h2>About PyCalc</h2>
            <p style="font-style: italic">
            <p>
              A simple calculator.
            </p>
            <p><a href="mailto:andreas.josef.schmid@rwth-aachen.de">
            Andreas Schmid</a></p>
            <p>
              This software is published under the
              <a href="http://www.gnu.org/licenses/gpl.html">GPL
                (GNU General Public License)</a>
            </p>
            <p style="font-weight: bold">
              Version: %s
            </p>
            ''' % __version__)


class CalculatorCtrl(object):
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _buildExpression(self, expr):
        expression = self._view.getDisplayText() + expr
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnText, btn in self._view.btns.items():
            if btnText == 'C':
                btn.clicked.connect(self._view.clearDisplay)
            elif btnText == '=':
                btn.clicked.connect(self._calcResult)
            else:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        self._view.display.returnPressed.connect(self._calcResult)

    def _calcResult(self):

        def evaluateExpression(expression):
            try:
                result = str(eval(expression, {}, {}))
            except Exception:
                result = ERROR_MSG
            return result

        result = evaluateExpression(self._view.getDisplayText())
        self._view.setDisplayText(result)


def main():
    app = QApplication(sys.argv)
    pycalculator = PyCalcUi()
    pycalculator.show()
    ctrl = CalculatorCtrl(view=pycalculator)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
