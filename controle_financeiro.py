from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, 
                            QTableWidget, QTableWidgetItem, QFrame, QMessageBox,
                            QDateEdit, QFileDialog, QTabWidget, QStackedWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon, QPainter, QColor, QPalette
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import sys
from datetime import datetime
import json
import os
import csv

class ControleDeCaixa:
    def __init__(self):
        self.saldo = 0.0
        self.transacoes = []
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        self.carregar_transacoes()

    def carregar_transacoes(self):
        try:
            if os.path.exists("transacoes.json"):
                with open("transacoes.json", "r", encoding='utf-8') as f:
                    dados = json.load(f)
                    if self.validar_dados(dados):
                        # Adiciona categoria 'Outros' para transações antigas
                        self.transacoes = [
                            {**t, "categoria": t.get("categoria", "Outros")} 
                            for t in dados.get("transacoes", [])
                        ]
                        self.saldo = dados.get("saldo", 0.0)
                    else:
                        raise ValueError("Arquivo de dados corrompido")
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            self.transacoes = []
            self.saldo = 0.0

    def validar_dados(self, dados):
        if not isinstance(dados, dict):
            return False
        if "transacoes" not in dados or "saldo" not in dados:
            return False
        if not isinstance(dados["transacoes"], list):
            return False
        return True

    def salvar_transacoes(self):
        with open("transacoes.json", "w", encoding='utf-8') as f:
            json.dump({"transacoes": self.transacoes, "saldo": self.saldo}, f, ensure_ascii=False)
        self.fazer_backup()

    def fazer_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"transacoes_backup_{timestamp}.json")
        with open(backup_file, "w", encoding='utf-8') as f:
            json.dump({"transacoes": self.transacoes, "saldo": self.saldo}, f, ensure_ascii=False)

    def adicionar_entrada(self, valor, descricao, categoria):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        data = datetime.now()
        self.saldo += valor
        self.transacoes.append({
            "tipo": "entrada",
            "valor": valor,
            "descricao": descricao,
            "categoria": categoria,
            "data": data.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.salvar_transacoes()

    def adicionar_saida(self, valor, descricao, categoria):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        data = datetime.now()
        self.saldo -= valor
        self.transacoes.append({
            "tipo": "saida",
            "valor": valor,
            "descricao": descricao,
            "categoria": categoria,
            "data": data.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.salvar_transacoes()

    def excluir_transacao(self, index):
        if 0 <= index < len(self.transacoes):
            transacao = self.transacoes[index]
            if transacao["tipo"] == "entrada":
                self.saldo -= transacao["valor"]
            else:
                self.saldo += transacao["valor"]
            self.transacoes.pop(index)
            self.salvar_transacoes()

    def exportar_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["tipo", "valor", "descricao", "categoria", "data"])
            writer.writeheader()
            writer.writerows(self.transacoes)

    def obter_estatisticas(self):
        total_entradas = sum(t["valor"] for t in self.transacoes if t["tipo"] == "entrada")
        total_saidas = sum(t["valor"] for t in self.transacoes if t["tipo"] == "saida")
        
        categorias = {}
        for t in self.transacoes:
            # Usa 'Outros' como categoria padrão se não existir
            categoria = t.get("categoria", "Outros")
            if categoria not in categorias:
                categorias[categoria] = 0
            if t["tipo"] == "saida":
                categorias[categoria] += t["valor"]

        return {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": self.saldo,
            "categorias": categorias
        }

class ModernControleDeCaixa(QMainWindow):
    def __init__(self, controle_caixa):
        super().__init__()
        self.controle_caixa = controle_caixa
        self.tema_atual = "dark"
        # Definindo os temas como propriedade da classe
        self.temas = {
            "dark": {
                "background": "#121212",
                "surface": "#1E1E1E",
                "primary": "#BB86FC",
                "secondary": "#03DAC6",
                "text": "#FFFFFF",
                "error": "#CF6679",
                "frame": "#252525",
                "card": "#2D2D2D",
                "tab_unselected": "#333333",
                "text_secondary": "#B3B3B3"
            },
            "blue": {
                "background": "#1A1B1E",
                "surface": "#202225",
                "primary": "#2196F3",
                "secondary": "#64B5F6",
                "text": "#FFFFFF",
                "error": "#F44336",
                "frame": "#252830",
                "card": "#2F3037",
                "tab_unselected": "#2A2D35",
                "text_secondary": "#B3B3B3"
            },
            "material": {
                "background": "#0A1929",
                "surface": "#132F4C",
                "primary": "#007FFF",
                "secondary": "#3399FF",
                "text": "#FFFFFF",
                "error": "#EB0014",
                "frame": "#1A3B57",
                "card": "#173A5E",
                "tab_unselected": "#1E3A54",
                "text_secondary": "#B3B3B3"
            },
            "cyber": {
                "background": "#000000",
                "surface": "#1A1A1A",
                "primary": "#00FF9C",
                "secondary": "#00F0FF",
                "text": "#FFFFFF",
                "error": "#FF0055",
                "frame": "#202020",
                "card": "#252525",
                "tab_unselected": "#1A1A1A",
                "text_secondary": "#B3B3B3"
            }
        }
        
        # Adicionando referências para os labels
        self.saldo_valor = None
        self.entrada_valor = None
        self.saida_valor = None
        
        self.initUI()
        self.aplicar_tema()

    def initUI(self):
        self.setWindowTitle("Controle Financeiro")
        self.setMinimumSize(1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Tabs principais
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #ECEFF1;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background: #e0e0e0;
                border: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
            }
        """)

        self.tab_widget.addTab(self.criar_tab_dashboard(), "Dashboard")
        self.tab_widget.addTab(self.criar_tab_transacoes(), "Transações")
        self.tab_widget.addTab(self.criar_tab_relatorios(), "Relatórios")
        
        layout.addWidget(self.tab_widget)

        # Barra de controles
        controles_layout = QHBoxLayout()
        
        tema_btn = QPushButton("Alternar Tema")
        tema_btn.clicked.connect(self.alternar_tema)
        
        controles_layout.addWidget(tema_btn)
        
        layout.addLayout(controles_layout)

    def criar_tab_dashboard(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Container principal do saldo e cards
        info_container = QFrame()
        info_container.setObjectName("info_container")
        info_container.setStyleSheet(f"""
            QFrame#info_container {{
                background-color: {self.temas[self.tema_atual]["surface"]};
                border-radius: 15px;
                margin: 5px;
                padding: 15px;
                border: 1px solid {self.temas[self.tema_atual]["primary"]};
            }}
            QLabel {{
                color: {self.temas[self.tema_atual]["text"]};
                background: transparent;
            }}
            QLabel#titulo_saldo {{
                font-size: 16px;
                font-weight: bold;
                color: {self.temas[self.tema_atual]["text"]};
            }}
            QLabel#valor_saldo {{
                font-size: 28px;
                font-weight: bold;
                color: {self.temas[self.tema_atual]["primary"]};
            }}
            QLabel#titulo_card {{
                font-size: 14px;
                font-weight: bold;
                color: {self.temas[self.tema_atual]["text"]};
            }}
            QLabel#valor_card {{
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        
        # Saldo
        saldo_label = QLabel("Saldo Atual")
        saldo_label.setObjectName("titulo_saldo")
        info_layout.addWidget(saldo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        stats = self.controle_caixa.obter_estatisticas()
        self.saldo_valor = QLabel(f"R$ {stats['saldo']:.2f}")
        self.saldo_valor.setObjectName("valor_saldo")
        info_layout.addWidget(self.saldo_valor, alignment=Qt.AlignmentFlag.AlignCenter)

        # Cards de Entrada e Saída
        cards_layout = QHBoxLayout()
        
        # Card de Entradas
        entrada_frame = QFrame()
        entrada_frame.setObjectName("card_entrada")
        entrada_frame.setStyleSheet(f"""
            QFrame#card_entrada {{
                background-color: {self.temas[self.tema_atual]["card"]};
                border: 1px solid #4CAF50;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        entrada_layout = QVBoxLayout(entrada_frame)
        
        entrada_titulo = QLabel("ENTRADAS")
        entrada_titulo.setObjectName("titulo_card")
        entrada_layout.addWidget(entrada_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.entrada_valor = QLabel(f"R$ {stats['total_entradas']:.2f}")
        self.entrada_valor.setObjectName("valor_card")
        self.entrada_valor.setStyleSheet("color: #4CAF50;")
        entrada_layout.addWidget(self.entrada_valor, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Card de Saídas
        saida_frame = QFrame()
        saida_frame.setObjectName("card_saida")
        saida_frame.setStyleSheet(f"""
            QFrame#card_saida {{
                background-color: {self.temas[self.tema_atual]["card"]};
                border: 1px solid #F44336;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        saida_layout = QVBoxLayout(saida_frame)
        
        saida_titulo = QLabel("SAÍDAS")
        saida_titulo.setObjectName("titulo_card")
        saida_layout.addWidget(saida_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.saida_valor = QLabel(f"R$ {stats['total_saidas']:.2f}")
        self.saida_valor.setObjectName("valor_card")
        self.saida_valor.setStyleSheet("color: #F44336;")
        saida_layout.addWidget(self.saida_valor, alignment=Qt.AlignmentFlag.AlignCenter)

        cards_layout.addWidget(entrada_frame)
        cards_layout.addWidget(saida_frame)
        info_layout.addLayout(cards_layout)
        
        layout.addWidget(info_container)

        # Container dos Gráficos (mantendo o estilo original)
        charts_container = QFrame()
        charts_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                margin: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        charts_layout = QHBoxLayout(charts_container)
        charts_layout.setSpacing(10)
        
        # Container do Gráfico de Pizza
        pie_container = QFrame()
        pie_container.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
        """)
        pie_layout = QVBoxLayout(pie_container)
        pie_title = QLabel("Distribuição de Gastos por Categoria")
        pie_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px; color: #333;")
        pie_layout.addWidget(pie_title, alignment=Qt.AlignmentFlag.AlignCenter)
        pie_chart = self.criar_grafico_categorias(stats['categorias'])
        pie_layout.addWidget(pie_chart)
        
        # Container do Gráfico de Barras
        bar_container = QFrame()
        bar_container.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
        """)
        bar_layout = QVBoxLayout(bar_container)
        bar_title = QLabel("Comparativo Entradas vs Saídas")
        bar_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px; color: #333;")
        bar_layout.addWidget(bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        bar_chart = self.criar_grafico_entradas_saidas(stats)
        bar_layout.addWidget(bar_chart)

        charts_layout.addWidget(pie_container)
        charts_layout.addWidget(bar_container)

        layout.addWidget(charts_container)

        return widget

    def criar_grafico_categorias(self, categorias):
        series = QPieSeries()
        
        # Cores para tema escuro
        cores = {
            "Alimentação": "#FF9800",
            "Transporte": "#2196F3",
            "Moradia": "#4CAF50",
            "Lazer": "#9C27B0",
            "Saúde": "#F44336",
            "Outros": "#607D8B"
        }
        
        for categoria, valor in categorias.items():
            fatia = series.append(categoria, valor)
            if categoria in cores:
                fatia.setBrush(QColor(cores[categoria]))
            fatia.setLabelVisible(True)
            percentual = (valor / (sum(categorias.values()) or 1) * 100)
            fatia.setLabel(f"{categoria}\n{percentual:.1f}%")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Gastos por Categoria")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Aplicando tema ao gráfico
        tema = self.temas[self.tema_atual]
        
        chart.setBackgroundBrush(QColor(tema["surface"]))
        chart.setTitleBrush(QColor(tema["text"]))
        chart.legend().setLabelColor(QColor(tema["text"]))

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        chartview.setMinimumSize(350, 300)
        
        return chartview

    def criar_grafico_entradas_saidas(self, stats):
        series = QBarSeries()
        
        entradas = QBarSet("Entradas")
        saidas = QBarSet("Saídas")
        
        # Configurando cores
        entradas.setColor(QColor("#4CAF50"))  # Verde
        saidas.setColor(QColor("#F44336"))    # Vermelho
        
        entradas.append(stats['total_entradas'])
        saidas.append(stats['total_saidas'])
        
        series.append(entradas)
        series.append(saidas)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Entradas vs Saídas")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        categories = ["Movimentações"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_valor = max(stats['total_entradas'], stats['total_saidas'])
        axis_y.setRange(0, max_valor * 1.2)  # Adiciona 20% de margem
        axis_y.setTitleText("Valor (R$)")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        chartview.setMinimumSize(400, 300)  # Definindo um tamanho mínimo
        
        return chartview

    def criar_tab_transacoes(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

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

        # Tipo (colocando antes da categoria para poder influenciar as opções)
        tipo_layout = QVBoxLayout()
        tipo_label = QLabel("Tipo:")
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Entrada", "Saída"])
        self.tipo_combo.currentTextChanged.connect(self.atualizar_categorias)  # Conecta o sinal
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
        self.tabela.setColumnCount(6)  # Adicionando uma coluna para o botão excluir
        self.tabela.setHorizontalHeaderLabels(["Tipo", "Valor", "Descrição", "Categoria", "Data", "Ações"])
        self.tabela.horizontalHeader().setStretchLastSection(True)
        
        # Estilo para os botões de excluir na tabela
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

        return widget

    def atualizar_categorias(self, tipo):
        self.cat_combo.clear()
        if tipo == "Entrada":
            self.cat_combo.addItems([
                "Salário",
                "Freelance",
                "Investimentos",
                "Vendas",
                "Outros Ganhos"
            ])
        else:  # Saída
            self.cat_combo.addItems([
                "Alimentação",
                "Transporte",
                "Moradia",
                "Lazer",
                "Saúde",
                "Educação",
                "Contas",
                "Compras",
                "Outros Gastos"
            ])

    def criar_tab_relatorios(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

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

        stats_layout.addWidget(QLabel(f"Total de Entradas: R$ {stats['total_entradas']:.2f}"))
        stats_layout.addWidget(QLabel(f"Total de Saídas: R$ {stats['total_saidas']:.2f}"))
        stats_layout.addWidget(QLabel(f"Saldo Atual: R$ {stats['saldo']:.2f}"))

        # Gastos por categoria
        stats_layout.addWidget(QLabel("\nGastos por Categoria:"))
        for categoria, valor in stats['categorias'].items():
            stats_layout.addWidget(QLabel(f"{categoria}: R$ {valor:.2f}"))

        layout.addWidget(stats_frame)
        return widget

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
            self.atualizar_interface()
            QMessageBox.information(self, "Sucesso", "Transação registrada com sucesso!")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def filtrar_transacoes(self):
        # Implementação do filtro
        pass

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
            layout.setContentsMargins(2, 2, 2, 2)  # Margens pequenas
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza o botão
            
            # Botão Excluir com tamanho reduzido
            btn_excluir = QPushButton("Excluir")  # Usando × como ícone de exclusão
            btn_excluir.setFixedSize(24, 24)  # Tamanho fixo pequeno
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
        self.tabela.setColumnWidth(5, 50)  # Largura fixa para coluna de ações

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
            self.atualizar_interface()
            QMessageBox.information(self, "Sucesso", "Transação excluída com sucesso!")

    def atualizar_interface(self):
        self.atualizar_tabela()
        stats = self.controle_caixa.obter_estatisticas()
        
        # Atualiza os valores no dashboard
        if self.saldo_valor:
            self.saldo_valor.setText(f"R$ {stats['saldo']:.2f}")
        if self.entrada_valor:
            self.entrada_valor.setText(f"R$ {stats['total_entradas']:.2f}")
        if self.saida_valor:
            self.saida_valor.setText(f"R$ {stats['total_saidas']:.2f}")
        
        # Atualiza os gráficos recriando a tab do dashboard
        if hasattr(self, 'tab_widget'):
            self.tab_widget.removeTab(0)
            self.tab_widget.insertTab(0, self.criar_tab_dashboard(), "Dashboard")

    def limpar_campos(self):
        self.valor_input.clear()
        self.desc_input.clear()
        self.cat_combo.setCurrentIndex(0)
        self.tipo_combo.setCurrentIndex(0)

    def aplicar_tema(self):
        tema = self.temas[self.tema_atual]
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {tema["background"]};
            }}
            QWidget {{
                background-color: transparent;
                color: {tema["text"]};
            }}
            QFrame {{
                background-color: {tema["frame"]};
                border-radius: 10px;
                padding: 15px;
                border: 1px solid {tema["surface"]};
            }}
            QPushButton {{
                background-color: {tema["primary"]};
                color: {tema["text"]};
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {tema["secondary"]};
                border: 1px solid {tema["primary"]};
            }}
            QLineEdit, QComboBox, QDateEdit {{
                padding: 8px;
                border: 1px solid {tema["surface"]};
                border-radius: 5px;
                background-color: {tema["surface"]};
                color: {tema["text"]};
                min-width: 150px;
            }}
            QTableWidget {{
                background-color: {tema["surface"]};
                border: none;
                gridline-color: {tema["frame"]};
                color: {tema["text"]};
                border-radius: 10px;
            }}
            QHeaderView::section {{
                background-color: {tema["primary"]};
                color: {tema["text"]};
                padding: 8px;
                border: none;
            }}
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            
            QTabBar {{
                background: transparent;
            }}
            
            QTabBar::tab {{
                padding: 10px 20px;
                background: {tema["tab_unselected"]};
                color: {tema["text_secondary"]};
                border: none;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}
            
            QTabBar::tab:hover {{
                background: {tema["surface"]};
                color: {tema["text"]};
            }}
            
            QTabBar::tab:selected {{
                background: {tema["primary"]};
                color: {tema["text"]};
                font-weight: bold;
            }}
            
            /* Adiciona uma linha sutil embaixo das tabs não selecionadas */
            QTabBar::tab:!selected {{
                border-bottom: 2px solid {tema["surface"]};
            }}
            
            /* Remove a linha da tab selecionada */
            QTabBar::tab:selected {{
                border-bottom: none;
            }}
        """)

        # Configurando a paleta de cores para os gráficos
        if hasattr(self, 'tab_widget'):
            self.tab_widget.clear()
            self.tab_widget.addTab(self.criar_tab_dashboard(), "Dashboard")
            self.tab_widget.addTab(self.criar_tab_transacoes(), "Transações")
            self.tab_widget.addTab(self.criar_tab_relatorios(), "Relatórios")

    def alternar_tema(self):
        temas = ["dark", "blue", "material", "cyber"]
        atual = temas.index(self.tema_atual)
        self.tema_atual = temas[(atual + 1) % len(temas)]
        self.aplicar_tema()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controle = ControleDeCaixa()
    window = ModernControleDeCaixa(controle)
    window.show()
    sys.exit(app.exec())