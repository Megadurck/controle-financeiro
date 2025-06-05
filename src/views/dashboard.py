from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from src.utils.constantes import CORES_GRAFICO

class Dashboard(QWidget):
    def __init__(self, controle_caixa, tema_atual, temas):
        super().__init__()
        self.controle_caixa = controle_caixa
        self.tema_atual = tema_atual
        self.temas = temas
        self.saldo_valor = None
        self.entrada_valor = None
        self.saida_valor = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
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

        # Container dos Gráficos
        charts_container = QFrame()
        charts_container.setObjectName("charts_container")
        charts_container.setStyleSheet("""
            QFrame#charts_container {
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
        pie_container.setObjectName("pie_container")
        pie_container.setStyleSheet("""
            QFrame#pie_container {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-width: 300px;
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
        bar_container.setObjectName("bar_container")
        bar_container.setStyleSheet("""
            QFrame#bar_container {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-width: 300px;
            }
        """)
        bar_layout = QVBoxLayout(bar_container)
        bar_title = QLabel("Comparativo Entradas vs Saídas")
        bar_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px; color: #333;")
        bar_layout.addWidget(bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        bar_chart = self.criar_grafico_entradas_saidas(stats)
        bar_layout.addWidget(bar_chart)

        # Adicionar os containers com proporções iguais
        charts_layout.addWidget(pie_container, 1)
        charts_layout.addWidget(bar_container, 1)

        layout.addWidget(charts_container)

    def criar_grafico_categorias(self, categorias):
        series = QPieSeries()
        
        for categoria, valor in categorias.items():
            fatia = series.append(categoria, valor)
            if categoria in CORES_GRAFICO:
                fatia.setBrush(QColor(CORES_GRAFICO[categoria]))
            fatia.setLabelVisible(True)
            percentual = (valor / (sum(categorias.values()) or 1) * 100)
            fatia.setLabel(f"{categoria}\n{percentual:.1f}%")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Gastos por Categoria")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        
        tema = self.temas[self.tema_atual]
        
        chart.setBackgroundBrush(QColor(tema["surface"]))
        chart.setTitleBrush(QColor(tema["text"]))
        chart.legend().setLabelColor(QColor(tema["text"]))

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        chartview.setMinimumSize(250, 250)
        chartview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        return chartview

    def criar_grafico_entradas_saidas(self, stats):
        series = QBarSeries()
        
        entradas = QBarSet("Entradas")
        saidas = QBarSet("Saídas")
        
        entradas.setColor(QColor("#4CAF50"))
        saidas.setColor(QColor("#F44336"))
        
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
        axis_y.setRange(0, max_valor * 1.2)
        axis_y.setTitleText("Valor (R$)")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        chartview.setMinimumSize(250, 250)
        chartview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        return chartview

    def atualizar_dados(self):
        stats = self.controle_caixa.obter_estatisticas()
        
        # Atualizar os valores
        if self.saldo_valor:
            self.saldo_valor.setText(f"R$ {stats['saldo']:.2f}")
        if self.entrada_valor:
            self.entrada_valor.setText(f"R$ {stats['total_entradas']:.2f}")
        if self.saida_valor:
            self.saida_valor.setText(f"R$ {stats['total_saidas']:.2f}")
        
        # Atualizar os gráficos
        charts_container = self.findChild(QFrame, "charts_container")
        if charts_container:
            # Encontrar os containers dos gráficos
            pie_container = charts_container.findChild(QFrame, "pie_container")
            bar_container = charts_container.findChild(QFrame, "bar_container")
            
            if pie_container and bar_container:
                # Encontrar os ChartViews existentes
                pie_chart_view = pie_container.findChild(QChartView)
                bar_chart_view = bar_container.findChild(QChartView)
                
                if pie_chart_view:
                    # Atualizar o gráfico de pizza
                    series = QPieSeries()
                    for categoria, valor in stats['categorias'].items():
                        fatia = series.append(categoria, valor)
                        if categoria in CORES_GRAFICO:
                            fatia.setBrush(QColor(CORES_GRAFICO[categoria]))
                        fatia.setLabelVisible(True)
                        percentual = (valor / (sum(stats['categorias'].values()) or 1) * 100)
                        fatia.setLabel(f"{categoria}\n{percentual:.1f}%")
                    
                    pie_chart_view.chart().removeAllSeries()
                    pie_chart_view.chart().addSeries(series)
                
                if bar_chart_view:
                    # Atualizar o gráfico de barras
                    series = QBarSeries()
                    entradas = QBarSet("Entradas")
                    saidas = QBarSet("Saídas")
                    
                    entradas.setColor(QColor("#4CAF50"))
                    saidas.setColor(QColor("#F44336"))
                    
                    entradas.append(stats['total_entradas'])
                    saidas.append(stats['total_saidas'])
                    
                    series.append(entradas)
                    series.append(saidas)
                    
                    bar_chart_view.chart().removeAllSeries()
                    bar_chart_view.chart().addSeries(series)
                    
                    # Atualizar o eixo Y
                    axis_y = bar_chart_view.chart().axes(Qt.Orientation.Vertical)[0]
                    max_valor = max(stats['total_entradas'], stats['total_saidas'])
                    axis_y.setRange(0, max_valor * 1.2) 