#    Copyright (C) 2018 by Bitonic B.V.
#
#    This file is part of Fireworks.
#
#    Fireworks is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Fireworks is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Fireworks. If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

from .. import formatting



class AmountInput(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.input = QLineEdit(self)
        self.input.setText('0.00000000 000')
        layout.addWidget(self.input, 1)

        self.unit = QLabel('BTC', self) #TODO: default unit setting; drop-down for units
        layout.addWidget(self.unit, 0)

        self.setLayout(layout)


    def getValue(self):
        amountText = self.input.text() + ' ' + self.unit.text()
        return formatting.unformatAmount(amountText)

