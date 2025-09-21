import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QDateEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import QDate, Qt


class GastosApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Gastos Personales")
        self.resize(720, 500)

        # ---------- Widgets de entrada ----------
        self.lblCategoria = QLabel("Categoría:")
        self.cmbCategoria = QComboBox()
        self.cmbCategoria.addItems([
            "Alimentación", "Transporte", "Servicios", "Hogar",
            "Salud", "Educación", "Ocio", "Otros"
        ])

        self.lblDescripcion = QLabel("Descripción:")
        self.txtDescripcion = QLineEdit()
        self.txtDescripcion.setPlaceholderText("Ej: Almuerzo, Uber, Recarga...")

        self.lblMonto = QLabel("Monto ($):")
        self.txtMonto = QLineEdit()
        self.txtMonto.setPlaceholderText("Ej: 5.75")
        self.txtMonto.setMaxLength(12)

        self.lblFecha = QLabel("Fecha:")
        self.dateFecha = QDateEdit()
        self.dateFecha.setCalendarPopup(True)
        self.dateFecha.setDate(QDate.currentDate())

        self.btnAgregar = QPushButton("Agregar")
        self.btnEliminar = QPushButton("Eliminar seleccionado")

        # ---------- Filtros ----------
        self.lblFiltro = QLabel("Filtrar por categoría:")
        self.cmbFiltro = QComboBox()
        self.cmbFiltro.addItem("Todas")
        self.cmbFiltro.addItems(self.cmbCategoria.itemText(i) for i in range(self.cmbCategoria.count()))
        self.btnLimpiarFiltros = QPushButton("Limpiar filtros")