import json
import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

class ControleDeCaixa:
    def __init__(self):
        self.saldo = 0.0
        self.transacoes = []

        self.backup_dir = os.path.join(DATA_DIR, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

        self.carregar_transacoes()

    def carregar_transacoes(self):
        try:
            arquivo_transacoes = os.path.join(DATA_DIR, "transacoes.json")
            if os.path.exists(arquivo_transacoes):
                with open(arquivo_transacoes, "r", encoding='utf-8') as f:
                    dados = json.load(f)
                    if self.validar_dados(dados):
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
        arquivo_transacoes = os.path.join(DATA_DIR, "transacoes.json")
        with open(arquivo_transacoes, "w", encoding='utf-8') as f:
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

    def listar_backups(self):
        arquivos = []
        if os.path.exists(self.backup_dir):
            for arquivo in os.listdir(self.backup_dir):
                if arquivo.endswith(".json"):
                    arquivos.append(arquivo)
        return sorted(arquivos, reverse=True)

    def restaurar_backup(self, nome_arquivo):
        caminho_backup = os.path.join(self.backup_dir, nome_arquivo)

        if not os.path.exists(caminho_backup):
            raise FileNotFoundError("Arquivo de backup não encontrado")
        
        with open(caminho_backup, "r", encoding='utf-8') as f:
            dados = json.load(f)

            if not self.validar_dados(dados):
                raise ValueError("Arquivo de backup invalido ou corrompido")
            
            self.transacoes = dados.get("transacoes", [])
            self.saldo = dados.get("saldo", 0.0)
        
        self.salvar_transacoes()