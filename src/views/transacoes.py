from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton, QTableWidget,
                            QTableWidgetItem, QFrame, QMessageBox, QDateEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from src.utils.constantes import CATEGORIAS_ENTRADA, CATEGORIAS_SAIDA

class Transacoes(QWidget):
    atualizar_signal = pyqtSignal()
    def __init__(self, controle_caixa, tema_atual, temas):
        super().__init__()
        self.controle_caixa = controle_caixa
        self.tema_atual = tema_atual
        self.temas = temas
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Frame de entrada
        input_frame = QFrame()
        input_layout = QVBoxLayout(input_frame)

        # Campos de entrada
        form_layout = QHBoxLayout()

        # Valor
        valor_layout = QVBoxLayout()
        valor_label = QLabel("Valor:")
        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("R$ 0,00")
        valor_layout.addWidget(valor_label)
        valor_layout.addWidget(self.valor_input)
        form_layout.addLayout(valor_layout)

        # Descrição
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Descrição:")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Digite a descrição")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        form_layout.addLayout(desc_layout)

        # Tipo
        tipo_layout = QVBoxLayout()
        tipo_label = QLabel("Tipo:")
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Entrada", "Saída"])
        self.tipo_combo.currentTextChanged.connect(self.atualizar_categorias)
        tipo_layout.addWidget(tipo_label)
        tipo_layout.addWidget(self.tipo_combo)
        form_layout.addLayout(tipo_layout)

        # Categoria
        cat_layout = QVBoxLayout()
        cat_label = QLabel("Categoria:")
        self.cat_combo = QComboBox()
        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self.cat_combo)
        form_layout.addLayout(cat_layout)

        input_layout.addLayout(form_layout)

        # Botão adicionar
        add_btn = QPushButton("Adicionar Transação")
        add_btn.clicked.connect(self.registrar_transacao)
        input_layout.addWidget(add_btn)

        layout.addWidget(input_frame)

        # Filtros
        filtro_frame = QFrame()
        filtro_layout = QHBoxLayout(filtro_frame)

        self.data_inicial = QDateEdit()
        self.data_inicial.setCalendarPopup(True)
        filtro_layout.addWidget(QLabel("De:"))
        filtro_layout.addWidget(self.data_inicial)

        self.data_final = QDateEdit()
        self.data_final.setCalendarPopup(True)
        filtro_layout.addWidget(QLabel("Até:"))
        filtro_layout.addWidget(self.data_final)

        filtrar_btn = QPushButton("Filtrar")
        filtrar_btn.clicked.connect(self.filtrar_transacoes)
        filtro_layout.addWidget(filtrar_btn)

        layout.addWidget(filtro_frame)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Tipo", "Valor", "Descrição", "Categoria", "Data", "Ações"])
        self.tabela.horizontalHeader().setStretchLastSection(True)
        
        self.tabela.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.temas[self.tema_atual]["error"]};
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FF5252;
            }}
        """)
        
        layout.addWidget(self.tabela)
        self.atualizar_tabela()

        # Inicializa as categorias
        self.atualizar_categorias("Entrada")

    def atualizar_categorias(self, tipo):
        self.cat_combo.clear()
        if tipo == "Entrada":
            self.cat_combo.addItems(CATEGORIAS_ENTRADA)
        else:
            self.cat_combo.addItems(CATEGORIAS_SAIDA)

    def registrar_transacao(self):
        try:
            valor = float(self.valor_input.text().replace("R$", "").strip())
            if valor <= 0:
                QMessageBox.warning(self, "Erro", "O valor deve ser maior que zero!")
                return

            descricao = self.desc_input.text().strip()
            if not descricao:
                QMessageBox.warning(self, "Erro", "A descrição não pode estar vazia!")
                return

            categoria = self.cat_combo.currentText()
            tipo = self.tipo_combo.currentText()

            if tipo == "Entrada":
                self.controle_caixa.adicionar_entrada(valor, descricao, categoria)
            else:
                self.controle_caixa.adicionar_saida(valor, descricao, categoria)

            self.limpar_campos()
            self.atualizar_tabela()
            self.atualizar_signal.emit()
            QMessageBox.information(self, "Sucesso", "Transação registrada com sucesso!")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def filtrar_transacoes(self):
        # Implementação do filtro
        pass

    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        for i, transacao in enumerate(self.controle_caixa.transacoes):
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            
            # Tipo
            tipo_item = QTableWidgetItem(transacao['tipo'])
            self.tabela.setItem(row, 0, tipo_item)
            
            # Valor
            valor_item = QTableWidgetItem(f"R$ {transacao['valor']:.2f}")
            self.tabela.setItem(row, 1, valor_item)
            
            # Descrição
            desc_item = QTableWidgetItem(transacao['descricao'])
            self.tabela.setItem(row, 2, desc_item)
            
            # Categoria
            cat_item = QTableWidgetItem(transacao.get('categoria', 'Outros'))
            self.tabela.setItem(row, 3, cat_item)
            
            # Data
            data_item = QTableWidgetItem(transacao['data'])
            self.tabela.setItem(row, 4, data_item)
            
            # Container para centralizar o botão
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Botão Excluir
            btn_excluir = QPushButton("Excluir")
            btn_excluir.setFixedSize(24, 24)
            btn_excluir.setToolTip("Excluir transação")
            btn_excluir.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.temas[self.tema_atual]["error"]};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 0px;
                }}
                QPushButton:hover {{
                    background-color: #FF5252;
                }}
            """)
            btn_excluir.clicked.connect(lambda checked, index=i: self.confirmar_exclusao(index))
            
            layout.addWidget(btn_excluir)
            self.tabela.setCellWidget(row, 5, container)

        # Ajustar o tamanho das colunas
        self.tabela.setColumnWidth(5, 50)

    def confirmar_exclusao(self, index):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Confirmar exclusão")
        msg.setInformativeText("Tem certeza que deseja excluir esta transação?")
        msg.setWindowTitle("Confirmar Exclusão")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.controle_caixa.excluir_transacao(index)
            self.atualizar_tabela()
            self.atualizar_signal.emit()
            QMessageBox.information(self, "Sucesso", "Transação excluída com sucesso!")

    def limpar_campos(self):
        self.valor_input.clear()
        self.desc_input.clear()
        self.cat_combo.setCurrentIndex(0)
        self.tipo_combo.setCurrentIndex(0) 