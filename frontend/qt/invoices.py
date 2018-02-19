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

import copy

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QLabel, QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel

from . import updatesignal
from .. import formatting



class InvoiceTable(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = \
            ['Expiration date', 'Label', 'Amount', 'Status']
        self.dataList = []


    def rowCount(self, parent):
        return len(self.dataList)


    def columnCount(self, parent):
        return len(self.header)


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        invoice = self.dataList[index.row()]
        col = index.column()
        if col == 0:
            return formatting.formatTimestamp(invoice.expirationTime)
        elif col == 1:
            return invoice.label
        elif col == 2:
            return formatting.formatAmount(invoice.amount)
        elif col == 3:
            return invoice.status

        return None


    def update(self, invoices):
        oldDataList = self.dataList

        newDataList = copy.deepcopy(invoices)
        newDataList.sort(key=lambda x: x.expirationTime)
        newDataList.reverse()

        if newDataList != oldDataList:
            self.beginResetModel()
            self.dataList = newDataList
            self.endResetModel()



class Invoices(QWidget):
    def __init__(self, parent, backend):
        super().__init__(parent)
        self.backend = backend

        layout = QHBoxLayout(self)

        self.invoiceTable = InvoiceTable(self)
        tableView = QTableView(self)
        tableView.setModel(self.invoiceTable)
        tableView.setSelectionBehavior(QTableView.SelectRows)
        tableView.setSelectionMode(QTableView.SingleSelection)
        for i in range(tableView.horizontalHeader().count()):
            tableView.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeToContents)
        layout.addWidget(tableView, 0)

        detailLayout = QGridLayout(self)
        layout.addLayout(detailLayout, 0)

        labels = ['Expiration date:', 'Label:', 'Amount:', 'Status:']
        for i, txt in enumerate(labels):
            label = QLabel(self)
            label.setText(txt)
            detailLayout.addWidget(label, i, 0)

        self.expirationLabel = QLabel(self)
        self.labelLabel = QLabel(self)
        self.amountLabel = QLabel(self)
        self.statusLabel = QLabel(self)
        detailLayout.addWidget(self.expirationLabel, 0, 1)
        detailLayout.addWidget(self.labelLabel, 1, 1)
        detailLayout.addWidget(self.amountLabel, 2, 1)
        detailLayout.addWidget(self.statusLabel, 3, 1)

        self.setLayout(layout)

        updatesignal.connect(self.update)
        tableView.selectionModel().selectionChanged.connect(self.onSelectInvoice)


    def update(self):
        invoices = self.backend.getInvoices()
        self.invoiceTable.update(invoices)


    def onSelectInvoice(self, selected, deselected):
        rows = set()
        for index in selected.indexes():
            rows.add(index.row())
        if len(rows) != 1:
            self.expirationLabel.setText('')
            self.labelLabel.setText('')
            self.amountLabel.setText('')
            self.statusLabel.setText('')
            return
        row = tuple(rows)[0]
        print(row)

