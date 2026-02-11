import sys
from PyQt6.QtWidgets import QApplication
from src.models.controle_caixa import ControleDeCaixa
from src.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    controle = ControleDeCaixa()
    window = MainWindow(controle)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
