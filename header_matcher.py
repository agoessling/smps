import sys
from typing import Optional, Sequence

import PySide6.QtCore as qc
import PySide6.QtWidgets as qw
import PySide6.QtGui as qg


class MatcherWindow(qw.QWidget):
  def __init__(self, parent: Optional[qw.QWidget] = None):
    super().__init__(parent)

    self.setWindowTitle('Header Matching')

    self.root_layout = qw.QVBoxLayout()
    self.setLayout(self.root_layout)
    self.table_layout = qw.QHBoxLayout()
    self.root_layout.addLayout(self.table_layout)

    self.selection_table = qw.QTableWidget(self)
    self.selection_table.verticalHeader().setVisible(False)
    self.selection_table.horizontalHeader().setVisible(False)
    self.selection_table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
    self.table_layout.addWidget(self.selection_table)

    self.result_table = qw.QTableWidget(self)
    self.result_table.verticalHeader().setVisible(False)
    self.result_table.horizontalHeader().setVisible(False)
    self.result_table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
    self.table_layout.addWidget(self.result_table)

  def populate_tables(self, actual: Sequence[str], desired: Sequence[str]):
    self.selection_table.clear()
    self.result_table.clear()

    self.selection_table.setColumnCount(1)
    self.selection_table.setRowCount(len(actual))

    for i, name in enumerate(actual):
      item = qw.QTableWidgetItem(name)
      item.setFlags(item.flags() & ~qc.Qt.ItemIsEditable)
      self.selection_table.setItem(i, 0, item)

    self.result_table.setColumnCount(2)
    self.result_table.setRowCount(len(desired))

    for i, name in enumerate(actual):
      item = qw.QTableWidgetItem(name)
      item.setFlags(qc.Qt.NoItemFlags)
      self.result_table.setItem(i, 0, item)


def main():
  app = qw.QApplication(sys.argv)

  window = MatcherWindow()
  window.populate_tables(['Part Number', 'Ciss', 'Price'], ['Ciss', 'Part'])
  window.show()

  sys.exit(app.exec())


if __name__ == '__main__':
  main()
