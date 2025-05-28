# tabs.py - Placeholder file (currently minimal usage)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

def create_table_tab(columns, rows=10):
    tab = QWidget()
    layout = QVBoxLayout(tab)
    table = QTableWidget(rows, len(columns))
    table.setHorizontalHeaderLabels(columns)
    layout.addWidget(table)
    return tab
