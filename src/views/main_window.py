from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget
from src.views.dashboard import Dashboard
from src.views.transacoes import Transacoes
from src.views.relatorios import Relatorios
from src.views.backup_tab import BackupTab
from src.utils.temas import TEMAS, obter_proximo_tema



class MainWindow(QMainWindow):
    def __init__(self, controle_caixa):
        super().__init__()
        self.controle_caixa = controle_caixa
        self.tema_atual = "dark"
        self.temas = TEMAS
        self.initUI()

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

        # Criando as tabs
        self.dashboard = Dashboard(self.controle_caixa, self.tema_atual, self.temas)
        self.transacoes = Transacoes(self.controle_caixa, self.tema_atual, self.temas)
        self.relatorios = Relatorios(self.controle_caixa, self.tema_atual, self.temas)
        self.backups = BackupTab(self.controle_caixa, self.tema_atual, self.temas)


        # Conectando o signal de atualização
        self.transacoes.atualizar_signal.connect(self.atualizar_tudo)

        self.tab_widget.addTab(self.dashboard, "Dashboard")
        self.tab_widget.addTab(self.transacoes, "Transações")
        self.tab_widget.addTab(self.relatorios, "Relatórios")
        self.tab_widget.addTab(self.backups, "Backups")

        
        layout.addWidget(self.tab_widget)

        # Barra de controles
        controles_layout = QHBoxLayout()
        
        tema_btn = QPushButton("Alternar Tema")
        tema_btn.clicked.connect(self.alternar_tema)
        
        controles_layout.addWidget(tema_btn)
        
        layout.addLayout(controles_layout)

        self.aplicar_tema()

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
            
            QTabBar::tab:!selected {{
                border-bottom: 2px solid {tema["surface"]};
            }}
            
            QTabBar::tab:selected {{
                border-bottom: none;
            }}
        """)

        # Atualizando o tema em todos os componentes
        self.dashboard.tema_atual = self.tema_atual
        self.transacoes.tema_atual = self.tema_atual
        self.relatorios.tema_atual = self.tema_atual
        self.backups.tema_atual = self.tema_atual

        # Recriando as tabs para atualizar o tema
        self.tab_widget.clear()
        self.tab_widget.addTab(self.dashboard, "Dashboard")
        self.tab_widget.addTab(self.transacoes, "Transações")
        self.tab_widget.addTab(self.relatorios, "Relatórios")
        self.tab_widget.addTab(self.backups, "Backups")

    def alternar_tema(self):
        self.tema_atual = obter_proximo_tema(self.tema_atual)
        self.aplicar_tema()

    def atualizar_tudo(self):
        self.dashboard.atualizar_dados()
        self.relatorios.atualizar_dados() 