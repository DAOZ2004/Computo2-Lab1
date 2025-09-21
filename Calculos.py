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

          # ---------- Tabla ----------
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Categoría", "Descripción", "Monto ($)", "Fecha"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setSelectionBehavior(self.tabla.SelectRows)
        self.tabla.setEditTriggers(self.tabla.NoEditTriggers)

        # ---------- Total ----------
        self.lblTotal = QLabel("Total: $0.00")
        self.lblTotal.setStyleSheet("font-weight: bold; font-size: 14px;")

        # ---------- Layouts ----------
        fila1 = QHBoxLayout()
        fila1.addWidget(self.lblCategoria)
        fila1.addWidget(self.cmbCategoria)
        fila1.addWidget(self.lblDescripcion)
        fila1.addWidget(self.txtDescripcion)

        fila2 = QHBoxLayout()
        fila2.addWidget(self.lblMonto)
        fila2.addWidget(self.txtMonto)
        fila2.addWidget(self.lblFecha)
        fila2.addWidget(self.dateFecha)
        fila2.addWidget(self.btnAgregar)
        fila2.addWidget(self.btnEliminar)

        filaFiltros = QHBoxLayout()
        filaFiltros.addWidget(self.lblFiltro)
        filaFiltros.addWidget(self.cmbFiltro)
        filaFiltros.addWidget(self.btnLimpiarFiltros)
        filaFiltros.addStretch()
        filaFiltros.addWidget(self.lblTotal)

        principal = QVBoxLayout()
        principal.addLayout(fila1)
        principal.addLayout(fila2)
        principal.addLayout(filaFiltros)
        principal.addWidget(self.tabla)

        self.setLayout(principal)

        # ---------- Conexiones ----------
        self.btnAgregar.clicked.connect(self.agregar_gasto)
        self.btnEliminar.clicked.connect(self.eliminar_seleccionado)
        self.cmbFiltro.currentTextChanged.connect(self.aplicar_filtro)
        self.btnLimpiarFiltros.clicked.connect(self.limpiar_filtros)

        # Datos en memoria (lista de dicts)
        self.gastos = []

    # ---------- Lógica ----------
    def agregar_gasto(self):
        categoria = self.cmbCategoria.currentText()
        desc = self.txtDescripcion.text().strip()
        monto_str = self.txtMonto.text().strip().replace(",", ".")
        fecha = self.dateFecha.date().toString("yyyy-MM-dd")

        # Validaciones simples
        if not desc:
            QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validación", "Ingresa un monto válido mayor que 0 (ej: 5.75).")
            return

        # Guardar
        item = {"categoria": categoria, "descripcion": desc, "monto": monto, "fecha": fecha}
        self.gastos.append(item)

        # Refrescar vista
        self.refrescar_tabla()
        self.txtDescripcion.clear()
        self.txtMonto.clear()
        self.txtDescripcion.setFocus()

    def eliminar_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Info", "Selecciona una fila para eliminar.")
            return

        # Encontrar registro equivalente en self.gastos según la fila visible (respetando filtros)
        visible = self.obtener_gastos_visibles()
        if 0 <= fila < len(visible):
            registro = visible[fila]
            # Eliminar el primero que coincida (por simplicidad)
            for i, g in enumerate(self.gastos):
                if (g["categoria"] == registro["categoria"] and
                    g["descripcion"] == registro["descripcion"] and
                    abs(g["monto"] - registro["monto"]) < 1e-9 and
                    g["fecha"] == registro["fecha"]):
                    del self.gastos[i]
                    break
            self.refrescar_tabla()

    def aplicar_filtro(self):
        self.refrescar_tabla()

    def limpiar_filtros(self):
        self.cmbFiltro.setCurrentIndex(0)  # "Todas"

    def obtener_gastos_visibles(self):
        categoria = self.cmbFiltro.currentText()
        if categoria == "Todas":
            return self.gastos
        return [g for g in self.gastos if g["categoria"] == categoria]

    def refrescar_tabla(self):
        data = self.obtener_gastos_visibles()
        self.tabla.setRowCount(0)

        total = 0.0
        for g in data:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(g["categoria"]))
            self.tabla.setItem(fila, 1, QTableWidgetItem(g["descripcion"]))
            monto_item = QTableWidgetItem(f"{g['monto']:.2f}")
            monto_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla.setItem(fila, 2, monto_item)
            self.tabla.setItem(fila, 3, QTableWidgetItem(g["fecha"]))
            total += g["monto"]

        self.lblTotal.setText(f"Total: ${total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GastosApp()
    ventana.show()
    sys.exit(app.exec_())