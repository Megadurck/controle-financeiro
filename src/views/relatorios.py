from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QFileDialog, QMessageBox)

class Relatorios(QWidget):
    def __init__(self, controle_caixa, tema_atual, temas):
        super().__init__()
        self.controle_caixa = controle_caixa
        self.tema_atual = tema_atual
        self.temas = temas
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Botões de exportação
        export_frame = QFrame()
        export_layout = QHBoxLayout(export_frame)

        export_csv_btn = QPushButton("Exportar CSV")
        export_csv_btn.clicked.connect(self.exportar_csv)
        export_layout.addWidget(export_csv_btn)

        layout.addWidget(export_frame)

        # Estatísticas detalhadas
        stats = self.controle_caixa.obter_estatisticas()
        
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)

        self.label_entradas = QLabel(f"Total de Entradas: R$ {stats['total_entradas']:.2f}")
        self.label_saidas = QLabel(f"Total de Saídas: R$ {stats['total_saidas']:.2f}")
        self.label_saldo = QLabel(f"Saldo Atual: R$ {stats['saldo']:.2f}")
        stats_layout.addWidget(self.label_entradas)
        stats_layout.addWidget(self.label_saidas)
        stats_layout.addWidget(self.label_saldo)

        # Gastos por categoria
        stats_layout.addWidget(QLabel("\nGastos por Categoria:"))
        self.categoria_labels = []
        for categoria, valor in stats['categorias'].items():
            lbl = QLabel(f"{categoria}: R$ {valor:.2f}")
            stats_layout.addWidget(lbl)
            self.categoria_labels.append(lbl)

        layout.addWidget(stats_frame)

    def exportar_csv(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            try:
                self.controle_caixa.exportar_csv(filename)
                QMessageBox.information(self, "Sucesso", "Dados exportados com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao exportar: {str(e)}")

    def atualizar_dados(self):
        stats = self.controle_caixa.obter_estatisticas()
        self.label_entradas.setText(f"Total de Entradas: R$ {stats['total_entradas']:.2f}")
        self.label_saidas.setText(f"Total de Saídas: R$ {stats['total_saidas']:.2f}")
        self.label_saldo.setText(f"Saldo Atual: R$ {stats['saldo']:.2f}")
        # Atualizar os labels de categoria
        for lbl in self.categoria_labels:
            lbl.deleteLater()
        self.categoria_labels = []
        for categoria, valor in stats['categorias'].items():
            lbl = QLabel(f"{categoria}: R$ {valor:.2f}")
            self.layout().itemAt(1).widget().layout().addWidget(lbl)
            self.categoria_labels.append(lbl) 