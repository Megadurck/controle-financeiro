from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox

class BackupTab(QWidget):
    def __init__(self, controle_caixa, tema_atual, temas):
        super().__init__()

        self.controle_caixa = controle_caixa
        self.tema_atual = tema_atual
        self.temas = temas

        self.layout = QVBoxLayout(self)

        self.lista_backups = QListWidget()
        self.botao_restaurar = QPushButton("Restaurar Backup")

        self.layout.addWidget(self.lista_backups)
        self.layout.addWidget(self.botao_restaurar)

        self.carregar_backups()
        self.botao_restaurar.clicked.connect(self.restaurar_backup)

    def carregar_backups(self):
        self.lista_backups.clear()
        backups = self.controle_caixa.listar_backups()
        self.lista_backups.addItems(backups)

    def restaurar_backup(self):
        item = self.lista_backups.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um backup")
            return

        nome_backup = item.text()
        self.controle_caixa.restaurar_backup(nome_backup)

        QMessageBox.information(self, "Sucesso", "Backup restaurado com sucesso")
