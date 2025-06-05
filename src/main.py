import sys
from PyQt6.QtWidgets import QApplication
from models.controle_caixa import ControleDeCaixa
from views.main_window import ModernControleDeCaixa

def main():
    app = QApplication(sys.argv)
    controle = ControleDeCaixa()
    window = ModernControleDeCaixa(controle)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 