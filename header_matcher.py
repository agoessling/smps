import csv
import sys
from typing import Callable, Optional, Sequence

import PySide6.QtCore as qc
import PySide6.QtWidgets as qw
import PySide6.QtGui as qg


class MatcherWindow(qw.QWidget):
  def __init__(self, parent: Optional[qw.QWidget] = None):
    super().__init__(parent)

    self.update_header_row_callback = None
    self.match_callback = None

    self.setWindowTitle('Header Matching')

    self.root_layout = qw.QVBoxLayout()
    self.setLayout(self.root_layout)
    self.table_layout = qw.QHBoxLayout()
    self.button_layout = qw.QHBoxLayout()
    self.root_layout.addLayout(self.table_layout)
    self.root_layout.addLayout(self.button_layout)

    self.selection_table = qw.QTableWidget(self)
    self.selection_table.verticalHeader().setVisible(False)
    self.selection_table.horizontalHeader().setVisible(False)
    self.selection_table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
    self.selection_table.itemDoubleClicked.connect(self.selection_made)
    self.table_layout.addWidget(self.selection_table)

    self.result_table = qw.QTableWidget(self)
    self.result_table.verticalHeader().setVisible(False)
    self.result_table.horizontalHeader().setVisible(False)
    self.result_table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
    self.result_table.setSelectionBehavior(qw.QTableWidget.SelectRows)
    self.table_layout.addWidget(self.result_table)

    self.header_spinbox = qw.QSpinBox()
    self.header_spinbox.setMinimum(0)
    self.header_spinbox.setRange(0, 99)
    self.header_spinbox.valueChanged.connect(self.update_header_row)
    self.match_button = qw.QPushButton('Match')
    self.match_button.clicked.connect(self.match_clicked)

    self.button_layout.addWidget(qw.QLabel('Header Row:'))
    self.button_layout.addWidget(self.header_spinbox)
    self.button_layout.addStretch()
    self.button_layout.addWidget(self.match_button)

  def add_match_callback(self, func: Callable[[], None]):
    self.match_callback = func

  def match_clicked(self):
    if self.match_callback:
      self.match_callback()

  def add_update_header_row_callback(self, func: Callable[[int], None]):
    self.update_header_row_callback = func

  def update_header_row(self, row: int):
    if self.update_header_row_callback:
      self.update_header_row_callback(row)

  def selection_made(self, item: qw.QTableWidgetItem):
    result_item = self.result_table.selectedItems()[1]
    result_item.setText(item.text())

    next_row = (result_item.row() + 1) % self.result_table.rowCount()
    self.result_table.setCurrentItem(self.result_table.item(next_row, 0))

  def populate_tables(self, actual: Sequence[str], desired: Sequence[str]):
    self.selection_table.clear()
    self.result_table.clear()

    self.selection_table.setColumnCount(1)
    self.selection_table.setRowCount(len(actual))

    for i, name in enumerate(actual):
      item = qw.QTableWidgetItem(name)
      item.setFlags(item.flags() & ~(qc.Qt.ItemIsEditable | qc.Qt.ItemIsSelectable))
      self.selection_table.setItem(i, 0, item)

    self.result_table.setColumnCount(2)
    self.result_table.setRowCount(len(desired))

    for i, name in enumerate(actual):
      item = qw.QTableWidgetItem(name)
      item.setFlags(item.flags() & ~qc.Qt.ItemIsEditable)
      self.result_table.setItem(i, 0, item)

      item = qw.QTableWidgetItem()
      item.setFlags(item.flags() & ~qc.Qt.ItemIsEditable)
      self.result_table.setItem(i, 1, item)

    self.result_table.setCurrentItem(self.result_table.item(0, 0))


def get_header_row(path: str, row: int):
  with open(path, 'r', newline='') as f:
    reader = csv.reader(f)
    for i, header in enumerate(reader):
      if row == i:
        return header


def main():
  app = qw.QApplication(sys.argv)

  window = MatcherWindow()
  window.populate_tables(['Part Number', 'Ciss', 'Price'], ['Ciss', 'Part'])
  window.show()

  sys.exit(app.exec())


if __name__ == '__main__':
  main()
